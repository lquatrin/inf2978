import numpy as np
import msvcrt as m

import re, time, sys, os

from collections import defaultdict
from multiprocessing import Process
import llsh, lminhash

import sutils

def CreateShingle(filename, ngram_size, max_hash_val = None, list_coef = None):
  assert(not list_coef is None)

  tokens = None
  with open(filename, "rb") as f:
    content = f.read().decode("UTF-8")
    if len(content) == 0:
      return None

    tokens = sutils.FormatContent(content)
    
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
  
  return minhash
 
#https://stackoverflow.com/questions/14533420/can-you-suggest-a-good-minhash-implementation
def ReadSongFiles(path, n_gram = 4, max_documents = None, hash_signatures = 10, lsh_threshold = 0.7, shingle_max_size = None, alphabet = None):
  assert(not shingle_max_size is None)
  assert(not alphabet is None)
  
  d_times = dict()
  d_times["data_creation"] = 0
  
  d_shingles = dict()
  d_minhash = dict()

  # Gerando lista de coeficientes
  list_coef = []
  n_coef = shingle_max_size
  for i in range(n_gram):
    n_coef = n_coef / alphabet 
    list_coef.append(n_coef)
  
  ############# MinHash Permutations
  # Já Criar as permutações aqui para usar diretamente em cada doc
  d_permutations = dict()
  for i in range(hash_signatures):
    d_permutations[i] = np.random.permutation(shingle_max_size)
	
  lsh = llsh.lLSH(hash_signatures, lsh_threshold)  
  
  n_count = 0
  for r,d,f in os.walk(path):
    for file in f:
      start = time.clock()

      pathf = r.replace('\\','/')
      filename = pathf + '/' + file

      d_author_name = pathf[pathf[:pathf.rfind('/')].rfind('/')+1:] + '/' + file
	  
      fshingle = CreateShingle(filename, n_gram, max_hash_val = shingle_max_size, list_coef = list_coef)
	  	  
      if fshingle is None:
        continue
		
      d_shingles[d_author_name] = fshingle
	  
	  # create minhash
      d_minhash[d_author_name] = lminhash.lMinHash(CalculateMinHash(fshingle, hash_signatures, shingle_max_size, d_permutations))
	  	  
	  # insert key and hash to build lsh
      lsh.Insert(d_author_name, d_minhash[d_author_name])
	  
      d_times["data_creation"] += time.clock() - start
	  	  
      n_count = n_count + 1
      if not (max_documents is None):
        if n_count >= max_documents:
          return d_shingles, d_minhash, lsh, d_times
  return d_shingles, d_minhash, lsh, d_times
