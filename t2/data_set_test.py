import sys, os, time
import serialization
import shingle

root = ""
#root = "F:/"
root = "D:/inf2978t2dataset/"

path = os.path.join(root, "TRAIN_DATASET/")

# https://github.com/ekzhu/datasketch
# https://ekzhu.github.io/datasketch/lsh.html
from datasketch import MinHash, MinHashLSH 
def duplicates(lsh_index):

  possible_duplicates = []
  for bucket in lsh_index.hashtables:
      for elem in bucket.values():
          if len(elem) > 1:
              possible_duplicates.append(elem)
  
  return possible_duplicates

#######################
# Parametros MinHash
#######################
shingle_gram = [3, 4, 5]
number_of_signatures = [30, 40, 50, 60, 70, 100]
max_docs = 200

for s_gram in shingle_gram:
  for n_sig in number_of_signatures:

    d_results = serialization.LoadPickleObject('data/' + 'songdata_' + str(s_gram) + '_' + str(n_sig))

    if d_results is None:
      start = time.clock()
      d_results = shingle.ReadSongFiles(path, s_gram, n_sig, max_docs)
      d_results['creation_time'] = time.clock() - start

      print(str(s_gram) + '_' + str(n_sig) + ": " + str(d_results['creation_time']))

      serialization.SavePickleObject('data/' + 'songdata_' + str(s_gram) + '_' + str(n_sig), d_results)


###################
# Parametros LSH
###################
similarity_threshold = [0.7, 0.8, 0.9]
d_r_b = dict()
# baseado no 'number_of_signatures', gerar as configuracoes
d_r_b[30]  = [(3, 10), (5, 6), (6, 5)]
d_r_b[40]  = [(4, 10), (5, 8), (8, 5)]
d_r_b[50]  = [(5, 10), (2, 25)]
d_r_b[60]  = [(6, 10), (5, 12)]
d_r_b[70]  = [(7, 10), (10, 7)]
d_r_b[100] = [(5, 20), (10, 10), (20, 5), (4, 25), (25, 4)]

for s_gram in shingle_gram:
  for hash_sig, signatures in d_r_b.items():
    # Carrega dados de letras de musica
    d_results = serialization.LoadPickleObject('data/' + 'songdata_' + str(s_gram) + '_' + str(hash_sig))
    for rb in signatures:
      rows = rb[0]
      bands = rb[1]
  
      assert(rows*bands == d_results['number_of_signatures'])	
  
      for s_threshold in similarity_threshold:
        # Define "weights = (r*b / r, r*b / b)" or "params = (r, b)"
        # Create LSH
        lsh = MinHashLSH(threshold = s_threshold, num_perm = rows*bands, params = (rows, bands))
        for k,v in d_results['minhash'].items():
          lsh.insert(k, v)
        
        # Criando o arquivo csv
        ret_file = open('data/' + 'resfile_' + str(s_gram) + '_' + str(hash_sig) + '_' + str(rows) + '_' + str(bands) + '_' + str(s_threshold).replace('.','') + '.csv','w')
        
        start = time.clock()
        # Onde Imprimir?
        #print("Gerando Duplicatas")

		# Checar letras parecidas baseado no valor de 'similarity_threshold'
        added_songs = dict()
        for key, v_minhash in d_results['minhash'].items():
          if not key in added_songs:
            result = lsh.query(v_minhash)
        
            for i in range(len(result)):
              added_songs[result[i]] = True
            
            if len(result) > 1:
              ret_file.write(';'.join(result))
              ret_file.write('\n')
              #input(str(len(result)) + ': ' + (';'.join(map(str,result))))
        # Onde Imprimir?
        #print(time.clock() - start)
        
        # Fechando arquivo CSV
        ret_file.close()