import sys,os, time

######################################
# 'lshingle' para implementacao manual
# 'shingle' para implementacao utiilizando a biblioteca datasketch
import mp_lshingle as shinglegen

root = ""
root = "F:/"
#root = "D:/inf2978t2dataset/"

path = os.path.join(root, "TRAIN_DATASET2/")
  
#https://docs.python.org/2/library/multiprocessing.html
#https://pymotw.com/2/multiprocessing/basics.html
if __name__ == '__main__':  
  #######################################
  # Parametros
  n_shingle_gram = 4
  n_alphabet = 27 #alphabet(26) + white space(1)
  similarity_threshold = 0.8
  r_rows = 5
  b_bands = 10
  max_docs = 100
  # tamanho de cada assinatura hash = r_band * b_band
   
  #Adicionar Pickle

  #LoadPickleObject(pf_name):
	
  start = time.clock()
  
  #print("Lendo arquivos de musica")
  d_shingles, d_minhash, lsh, times = shinglegen.ReadSongFiles(path, n_gram = n_shingle_gram, max_documents = None, hash_signatures = r_rows*b_bands, lsh_threshold = similarity_threshold, shingle_max_size = n_alphabet**n_shingle_gram, alphabet = n_alphabet)

  print(time.clock() - start)
  #SavePickleObject(pf_name, s_obj):

  
  # Criando o arquivo csv
  ret_file = open('resfile.csv','w')
  
  # Checar letras parecidas baseado no valor de 'similarity_threshold'
  added_songs = dict()
  for key, v_minhash in d_minhash.items():
    if not key in added_songs:
      result = lsh.query(v_minhash)
  
      for i in range(len(result)):
        added_songs[result[i]] = True
      
      if len(result) > 1:
        ret_file.write(';'.join(result))
        ret_file.write('\n')
        #input(str(len(result)) + ': ' + (';'.join(map(str,result))))
  
  # Fechando arquivo CSV
  ret_file.close()
