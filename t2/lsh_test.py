import sys, os, time, sutils
import serialization
import shingle
from datasketch import MinHash, MinHashLSH 

#root = ""
##root = "F:/"
#root = "D:/inf2978t2dataset/"
#path = os.path.join(root, "TRAIN_DATASET2/")

## https://github.com/ekzhu/datasketch
## https://ekzhu.github.io/datasketch/lsh.html

#def duplicates(lsh_index):
#
#  possible_duplicates = []
#  for bucket in lsh_index.hashtables:
#    for elem in bucket.values():
#      if len(elem) > 1:
#        possible_duplicates.append(elem)
#  
#  return possible_duplicates

#######################
# Parametros
#######################
def LSHTest (path, shingle_gram, hash_of_signatures, rows, bands, similarity_threshold):
  assert(rows*bands == hash_of_signatures)	

  ######################################
  # MinHash
  d_songdata = serialization.LoadPickleObject('data/' + 'songdata_' + str(shingle_gram) + '_' + str(hash_of_signatures))
  if d_songdata is None:
    d_songdata = shingle.ReadShingleAndBuildMinHash(path, shingle_gram, hash_of_signatures)
  
    print(str(shingle_gram) + '_' + str(hash_of_signatures) + ": " + str(d_songdata['time']))
  
    serialization.SavePickleObject('data/' + 'songdata_' + str(shingle_gram) + '_' + str(hash_of_signatures), d_songdata)
  ######################################
    
  ######################################
  # LSH
  lsh_time = time.clock()
  
  # Define "weights = (r*b / r, r*b / b)" or "params = (r, b)"
  # Create LSH
  #lsh = MinHashLSH(threshold = similarity_threshold, num_perm = rows*bands, params = (rows, bands))
  #for k,v in d_songdata['minhash'].items():
  #  lsh.insert(k, v)
  #
  ## Criando o arquivo csv
  #ret_file = open('data/' + 'resfile_' + str(shingle_gram) + '_' + str(hash_of_signatures) + '_' + str(rows) + '_' + str(bands) + '_' + str(similarity_threshold).replace('.','') + '.csv','w')
  #
  # Checar letras parecidas baseado no valor de 'similarity_threshold'
  #added_songs = dict()
  #for key, v_minhash in d_songdata['minhash'].items():
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
  #lsh_time = time.clock() - lsh_time
  #
  #print("LSH [" + str(shingle_gram) + ", " + str(hash_of_signatures) + ", " + str(rows) + ", " + str(bands) + ", " + str(similarity_threshold) + "]")
  #print(". Time: " + str(lsh_time))
  #
  ##precision, recall = sutils.evalutation(lsh)
  ##print(". Precision: " + precision)
  ##print(". Recall: " + recall)
  #
  #ret_file.close()
  ######################################