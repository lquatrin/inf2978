import sys, os, time, sutils
import serialization
import shingle
from datasketch import MinHash, MinHashLSH 

path = str(sys.argv[1])

#######################
# Parametros [a ser definido apos testes]
#######################
shingle_gram = 4
hash_of_signatures = 100
rows = 5
bands = 20
similarity_threshold = 0.9

assert(rows*bands == hash_of_signatures)	

######################################
# MinHash
d_songdata = shingle.ClassShingleAndBuildMinHash(path, shingle_gram, hash_of_signatures)
print(str(shingle_gram) + '_' + str(hash_of_signatures) + ": " + str(d_songdata['time']))
######################################
    
######################################
# LSH
lsh_time = time.clock()
  
# Define "weights = (r*b / r, r*b / b)" or "params = (r, b)"
# Create LSH
lsh = MinHashLSH(threshold = similarity_threshold, num_perm = rows*bands, params = (rows, bands))
for k,v in d_songdata['minhash'].items():
  lsh.insert(k, v)
  
# Criando o arquivo csv
ret_file = open('resfile_' + str(shingle_gram) + '_' + str(hash_of_signatures) + '_' + str(rows) + '_' + str(bands) + '_' + str(similarity_threshold).replace('.','') + '.csv','w')

# Checar letras parecidas baseado no valor de 'similarity_threshold'
added_songs = dict()
for key, v_minhash in d_songdata['minhash'].items():
  if not key in added_songs:
    result = lsh.query(v_minhash)

    for i in range(len(result)):
      added_songs[result[i]] = True
    
    if len(result) > 1:
      ret_file.write(';'.join([str(x) for x in result]))
      ret_file.write('\n')
      #input(str(len(result)) + ': ' + (';'.join(map(str,result))))

lsh_time = time.clock() - lsh_time
  
print("LSH [" + str(shingle_gram) + ", " + str(hash_of_signatures) + ", " + str(rows) + ", " + str(bands) + ", " + str(similarity_threshold) + "]")
print(". Time: " + str(lsh_time))
  
ret_file.close()
######################################