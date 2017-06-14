import sys, os, time, sutils
import serialization
import lshingle, mlsh

#######################
# Parametros
#######################
def ManualLSHTest (path, shingle_gram, hash_signatures, rows, bands, similarity_threshold):
  assert(rows*bands == hash_signatures)	

  # Gerando lista de coeficientes
  list_coef = []
  n_coef = 27**shingle_gram
  for i in range(shingle_gram):
    n_coef = n_coef / 27 
    list_coef.append(n_coef)
  
  ######################################
  # MinHash
  d_songdata = serialization.LoadPickleObject('data/' + 'manual_songdata_' + str(shingle_gram) + '_' + str(hash_signatures))
  if d_songdata is None:
    d_songdata = lshingle.ManualReadShingleAndBuildMinHash(path, shingle_gram, hash_signatures, list_coef, shingle_max_size = 27**shingle_gram)
  
    print(str(shingle_gram) + '_' + str(hash_signatures) + ": " + str(d_songdata['time']))
  
    serialization.SavePickleObject('data/' + 'manual_songdata_' + str(shingle_gram) + '_' + str(hash_signatures), d_songdata)
  ######################################
    
  ######################################
  # LSH
  lsh_time = time.clock()
  
  # Define "weights = (r*b / r, r*b / b)" or "params = (r, b)"
  # Create LSH
  lsh = mlsh.LSHMinHash(hash_signatures = hash_signatures, threshold = similarity_threshold, params = (rows, bands))
  
  for k,v in d_songdata['minhash'].items():
    lsh.insert(k, v)
  
  # Criando o arquivo csv
  ret_file = open('data/' + 'resfile_' + str(shingle_gram) + '_' + str(hash_signatures) + '_' + str(rows) + '_' + str(bands) + '_' + str(similarity_threshold).replace('.','') + '.csv','w')
  
  # Checar letras parecidas baseado no valor de 'similarity_threshold'
  added_songs = dict()
  for key, v_minhash in d_songdata['minhash'].items():
    if not key in added_songs:
      result = lsh.query(v_minhash)
  
      for i in range(len(result)):
        added_songs[result[i]] = True
      
      if len(result) > 1:
        ret_file.write(';'.join(result))
        ret_file.write('\n')
  
  lsh_time = time.clock() - lsh_time
  
  print("LSH [" + str(shingle_gram) + ", " + str(hash_signatures) + ", " + str(rows) + ", " + str(bands) + ", " + str(similarity_threshold) + "]")
  print(". Time: " + str(lsh_time))
  
  #precision, recall = sutils.evalutation(lsh)
  #print(". Precision: " + precision)
  #print(". Recall: " + recall)
  
  ret_file.close()
  ######################################