import numpy as np
import msvcrt as m

import re, time, sys, os

from collections import defaultdict
from multiprocessing import Process
import lminhash

import sutils

def CreateShingle(filename, ngram_size, max_hash_val = None, list_coef = None):
  assert(not list_coef is None)

  tokens = None
  with open(filename, "rb") as f:
    content = f.read().decode("UTF-8")
    if len(content) == 0:
      return None

    tokens = sutils.FormatContent(content, manual_mode = True)
    
  #Get a slice: s[start:end], starts in 0
  assert(len(tokens) >= ngram_size)
  
  ret_set = set()
  #[' '.join(tokens[i:i+ngram_size]) for i in range(0, len(tokens) - ngram_size + 1)]
  for i in range(ngram_size, len(tokens)):
    #old ret_set.add(tokens[i-ngram_size:i])
    ret_set.add(sum([a*b for a,b in zip(list_coef, [ord(i)-96 for i in tokens[i-ngram_size:i]])]) % max_hash_val)
   
  return ret_set 
  
#http://www.bogotobogo.com/Algorithms/minHash_Jaccard_Similarity_Locality_sensitive_hashing_LSH.php
#http://maciejkula.github.io/2015/02/01/minhash/
#http://mccormickml.com/2015/06/12/minhash-tutorial-with-python-code/
#https://stackoverflow.com/questions/14533420/can-you-suggest-a-good-minhash-implementation
def CalculateMinHash(shingle, n_signatures, shingle_max_size, permutations):
  minhash = np.zeros(n_signatures)
  
  for i in range(n_signatures):
    for j in range(shingle_max_size):
      if permutations[i][j] in shingle:
        minhash[i] = j
        break
  return minhash
 
#https://stackoverflow.com/questions/14533420/can-you-suggest-a-good-minhash-implementation
def ManualReadShingleAndBuildMinHash(path, shingle_gram, hash_signatures, list_coef, shingle_max_size = 2**32 - 1):
  d_minhash = dict()

  minhash_creation_time = time.clock()

  ############# MinHash Permutations
  # Já Criar as permutações aqui para usar diretamente em cada doc
  r_permutations = dict()
  for i in range(hash_signatures):
    r_permutations[i] = np.random.permutation(shingle_max_size)

  for r,d,f in os.walk(path):
    for file in f:
      pathf = r.replace('\\','/')
      filename = pathf + '/' + file

      d_author_name = pathf[pathf[:pathf.rfind('/')].rfind('/')+1:] + '/' + file
	  
	  #-------------> Read and Create Shingle
      fshingle = CreateShingle(filename, shingle_gram, max_hash_val = shingle_max_size, list_coef = list_coef)
      if fshingle is None:
        continue
	  
	  #-------------> Create MinHash
      d_minhash[d_author_name] = lminhash.lMinHash(CalculateMinHash(fshingle, hash_signatures, shingle_max_size, r_permutations))

  minhash_creation_time = (time.clock() -   minhash_creation_time)

  return {'minhash' : d_minhash, 'time' : minhash_creation_time, 'permutations' : r_permutations}
