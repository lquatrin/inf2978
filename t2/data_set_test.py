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
shingle_gram = 4
number_of_signatures = 50
max_docs = None #1000

d_results = serialization.LoadPickleObject('songdata')
if d_results is None:
	start = time.clock()
	# Creating minhashs
	d_results = shingle.ReadSongFiles(path, shingle_gram, number_of_signatures, max_docs)
	print("Read Songs", time.clock() - start)
	serialization.SavePickleObject('songdata', d_results)

similarity_threshold = 0.8
rows = 5
bands = 10

assert(rows*bands == d_results['number_of_signatures'])	
	
start = time.clock()
# https://github.com/ekzhu/datasketch
# https://ekzhu.github.io/datasketch/lsh.html
# Define "weights = (r*b / r, r*b / b)" or "params = (r, b)"
lsh = MinHashLSH(threshold = similarity_threshold, num_perm = rows*bands, params = (rows, bands))
for k,v in d_results['minhash'].items():
  lsh.insert(k, v)
print("Create LSH", time.clock() - start)



# Criando o arquivo csv
ret_file = open('resfile.csv','w')

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

# Fechando arquivo CSV
ret_file.close()
