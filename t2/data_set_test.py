import sys, os, time
import serialization
import shingle

root = ""
#root = "F:/"
#root = "D:/inf2978t2dataset/"

path = os.path.join(root, "TRAIN_DATASET/")

from datasketch import MinHash, MinHashLSH 
def duplicates(lsh_index):

  possible_duplicates = []
  for bucket in lsh_index.hashtables:
      for elem in bucket.values():
          if len(elem) > 1:
              possible_duplicates.append(elem)
  
  return possible_duplicates
  
#######################################
# Parametros
shingle_gram = [3, 4, 5]
number_of_signatures = [30, 40, 50, 60, 70, 100]
max_docs = None #1000

for s_gram in shingle_gram:
  for n_sig in number_of_signatures:

    d_results = serialization.LoadPickleObject('songdata_' + str(s_gram) + '_' + str(n_sig))

    if d_results is None:
      start = time.clock()
      d_results = shingle.ReadSongFiles(path, s_gram, n_sig, max_docs)
      d_results['creation_time'] = time.clock() - start
	  
      print(str(s_gram) + '_' + str(n_sig) + ": " + str(d_results['creation_time']))
	  
      serialization.SavePickleObject('songdata_' + str(s_gram) + '_' + str(n_sig), d_results)



#similarity_threshold = 0.8
#rows = 5
#bands = 10
#
#assert(rows*bands == d_results['number_of_signatures'])	
#	
#start = time.clock()
## https://github.com/ekzhu/datasketch
## https://ekzhu.github.io/datasketch/lsh.html
## Define "weights = (r*b / r, r*b / b)" or "params = (r, b)"
#lsh = MinHashLSH(threshold = similarity_threshold, num_perm = rows*bands, params = (rows, bands))
#for k,v in d_results['minhash'].items():
#  lsh.insert(k, v)
#print("Create LSH", time.clock() - start)
#
#
#
## Criando o arquivo csv
#ret_file = open('resfile.csv','w')
#
## Checar letras parecidas baseado no valor de 'similarity_threshold'
#added_songs = dict()
#for key, v_minhash in d_results['minhash'].items():
#  if not key in added_songs:
#    result = lsh.query(v_minhash)
#
#    for i in range(len(result)):
#      added_songs[result[i]] = True
#    
#    if len(result) > 1:
#      ret_file.write(';'.join(result))
#      ret_file.write('\n')
#      #input(str(len(result)) + ': ' + (';'.join(map(str,result))))
#
## Fechando arquivo CSV
#ret_file.close()
