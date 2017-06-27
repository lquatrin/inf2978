import sys, os, time, sutils
import serialization
import shingle
from datasketch import MinHash, MinHashLSH 

path = str(sys.argv[1])
#"D:/inf2978t2dataset/TRAIN_DATASET4" 

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
if rows == None or bands == None:
  lsh = MinHashLSH(threshold = similarity_threshold, num_perm = rows*bands)
else:
  lsh = MinHashLSH(threshold = similarity_threshold, num_perm = rows*bands, params = (rows, bands))
for k,v in d_songdata['minhash'].items():
  lsh.insert(k, v)
  
ret_file = open('data/' + 'resfile_' + str(shingle_gram) + '_' + str(hash_of_signatures) + '_' + str(rows) + '_' + str(bands) + '_' + str(similarity_threshold).replace('.','') + '.csv','w')
  
# Checar letras parecidas baseado no valor de 'similarity_threshold'
g_sel = 0
g_total = 0
added_songs = dict()

for key, v_minhash in d_songdata['minhash'].items():
  result = lsh.query(v_minhash)

  if len(result) > 1:
    for s_ret in result:
      if s_ret is not key:
        if not (((key,s_ret) in added_songs) or ((s_ret,key) in added_songs)):
          g_total = g_total + 1
          added_songs[(key, s_ret)] = True
          if v_minhash.jaccard(d_songdata['minhash'][s_ret]) >= similarity_threshold:
            g_sel = g_sel + 1
            if key < s_ret:
              ret_file.write(str(key) + ';' + str(s_ret))
            else:
              ret_file.write(str(s_ret) + ';' + str(key))
            ret_file.write('\n')

lsh_time = time.clock() - lsh_time

print("LSH [" + str(shingle_gram) + ", " + str(hash_of_signatures) + ", " + str(rows) + ", " + str(bands) + ", " + str(similarity_threshold) + "]")
print(". Time: " + str(lsh_time))
print(". LSH Precision: " + str((g_sel / g_total) * 100) + " %" + " [" + str(g_total) + ", " + str(g_sel) + "]")

ret_file.close()
######################################
