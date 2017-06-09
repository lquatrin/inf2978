import sys, os, time
import serialization
import shingle

root = ""
#root = "F:/"
#root = "D:/inf2978t2dataset/"

path = os.path.join(root, "TRAIN_DATASET/")


#######################
# Parametros
#######################
shingle_gram = int(sys.argv[1])
number_of_signatures = int(sys.argv[2])
rows = int(sys.argv[3])
bands = int(sys.argv[4])
similarity_threshold = float(sys.argv[5])

assert(rows*bands == number_of_signatures)	
max_docs = None # 200

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

#########################
# MinHash
d_results = serialization.LoadPickleObject('data/' + 'songdata_' + str(shingle_gram) + '_' + str(number_of_signatures))
if d_results is None:
  start = time.clock()
  d_results = shingle.ReadSongFiles(path, shingle_gram, number_of_signatures, max_docs)
  d_results['creation_time'] = time.clock() - start

  print(str(shingle_gram) + '_' + str(number_of_signatures) + ": " + str(d_results['creation_time']))

  serialization.SavePickleObject('data/' + 'songdata_' + str(shingle_gram) + '_' + str(number_of_signatures), d_results)

#########################
# LSH
assert(rows*bands == number_of_signatures)	

# Define "weights = (r*b / r, r*b / b)" or "params = (r, b)"
# Create LSH
lsh = MinHashLSH(threshold = similarity_threshold, num_perm = rows*bands, params = (rows, bands))
for k,v in d_results['minhash'].items():
  lsh.insert(k, v)

# Criando o arquivo csv
ret_file = open('data/' + 'resfile_' + str(shingle_gram) + '_' + str(number_of_signatures) + '_' + str(rows) + '_' + str(bands) + '_' + str(similarity_threshold).replace('.','') + '.csv','w')

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