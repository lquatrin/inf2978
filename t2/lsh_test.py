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
def LSHTest (path, shingle_gram, hash_of_signatures, similarity_threshold, rows = None, bands = None):
  assert(rows*bands == hash_of_signatures)	

  #print("starting")
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
  lsh = None
  if (rows is None) or (bands is None):
    lsh = MinHashLSH(threshold = similarity_threshold, num_perm = rows*bands) 
  else:
    lsh = MinHashLSH(threshold = similarity_threshold, num_perm = rows*bands, params = (rows, bands))
  for k,v in d_songdata['minhash'].items():
    lsh.insert(k, v)
  
  # Criando o arquivo csv
  lsh_time = time.clock() - lsh_time
  
  print("LSH [" + str(shingle_gram) + ", " + str(hash_of_signatures) + ", " + str(rows) + ", " + str(bands) + ", " + str(similarity_threshold) + "]")
  print(". Time: " + str(lsh_time))
  
  precision, recall = sutils.evalutation(lsh)
  print(". Precision: {}".format(precision))
  print(". Recall: {}".format(recall))
  
  ret_file = open('data/' + 'resfile_' + str(shingle_gram) + '_' + str(hash_of_signatures) + '_' + str(rows) + '_' + str(bands) + '_' + str(similarity_threshold).replace('.','') + '_' + str(precision) + '_' + str(recall) + '.csv','w')
  
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
              ret_file.write(key + ';' + s_ret)
              ret_file.write('\n')
  
  print(". LSH Precision: " + str((g_sel / g_total) * 100) + " %" + " [" + str(g_total) + ", " + str(g_sel) + "]")

  ret_file.close()
  
  ret_file = open('tests_results.csv','a')
  ret_file.write(str(shingle_gram) + ';' + str(hash_of_signatures) + ';' + str(rows) + ';' + str(bands) + '; 0.' + str(similarity_threshold) + ';' + str(precision) + ';' + str(recall) + ';' + str((g_sel / g_total) * 100));
  ret_file.close()
  ######################################
