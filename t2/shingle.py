import numpy as np
import msvcrt as m

import re, time, sys, os

from collections import defaultdict
from multiprocessing import Process
from datasketch import MinHash, MinHashLSH
 
import sutils
 
def CreateShingle(finput, ngram_size):

  tokens = None
  with open(finput, "rb") as f:
    content = f.read().decode("UTF-8")
    if len(content) == 0:
      return None
    
    tokens = sutils.FormatContent(content)

  if ngram_size > len(tokens):
      return set(''.join(tokens))
  
  return set([''.join(tokens[i:i+ngram_size]) for i in range(0, len(tokens) - ngram_size + 1)])

def buildMinHash(shingle_list,num_perm=128):
  mhash = MinHash(num_perm=num_perm)
  for shingle in shingle_list:
      try:
          mhash.update(shingle.encode('utf8'))
      except UnicodeEncodeError:
          continue
  return mhash


#receive minHash LSH https://ekzhu.github.io/datasketch/lsh.html  
def duplicates(lsh_index):

  possible_duplicates = []
  for bucket in lsh_index.hashtables:
      for elem in bucket.values():
          if len(elem) > 1:
              possible_duplicates.append(elem)
  
  return possible_duplicates


def ReadSongFiles(path, n_gram = 4, max_documents = None, hash_signatures = 50, lsh_threshold = 0.9, shingle_max_size = None, alphabet = None):
  d_times = dict()
  d_times["data_creation"] = 0

  d_shingles = dict()
  d_minhash = dict()
  
  # https://ekzhu.github.io/datasketch/lsh.html
  lsh = MinHashLSH(threshold = lsh_threshold, num_perm = hash_signatures)
  
  n_count = 0
  for r,d,f in os.walk(path):
    for file in f:
      start = time.clock()
	
      pathf = r.replace('\\','/')
      filename = pathf + '/' + file

      d_author_name = pathf[pathf[:pathf.rfind('/')].rfind('/')+1:] + '/' + file
      
      #-------------> Shingle
      #print(filename)
      fshingle = CreateShingle(filename, n_gram)

      if fshingle is None:
        continue
      
      d_shingles[d_author_name] = fshingle

      #-------------> MinHash
      d_minhash[d_author_name] = MinHash(num_perm = hash_signatures)
      for d in d_shingles[d_author_name]:
        d_minhash[d_author_name].update(d.encode('utf8'))

      lsh.insert(d_author_name, d_minhash[d_author_name])
	  
      d_times["data_creation"] += time.clock() - start
	  
      n_count = n_count + 1
      if not (max_documents is None):
        if n_count > max_documents:
          return d_shingles, d_minhash, lsh, d_times
  return d_shingles, d_minhash, lsh, d_times
