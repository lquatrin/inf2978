import numpy as np
import msvcrt as m
import re, os
from collections import defaultdict
from multiprocessing import Process
from datasketch import MinHash, MinHashLSH
 
def CreateShingle(finput, ngram_size):
  
  with open(finput, "rb") as f:
    content = f.read()

  tokens = content.split()
  if ngram_size > len(tokens):
      return ' '.join(tokens)
  
  return [' '.join(tokens[i:i+ngram_size]) for i in range(0, len(tokens) - ngram_size + 1)]

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


def ReadSongFiles(path, n_gram = 4, max_documents = None, hash_signatures = 50):
  d_names = dict()
  d_shingles = dict()

  # https://ekzhu.github.io/datasketch/lsh.html
  lsh_threshold = 0.1
  lsh = MinHashLSH(threshold=lsh_threshold,num_perm= hash_signatures)

  for r,d,f in os.walk(path):
    for file in f:
      filename = r.replace('\\','/') + '/' + file
      
      #-------------> Shingle
      d_shingles = CreateShingle(filename, n_gram)
      print(d_shingles)

      #-------------> MinHash
      mhash = build_minhash(n_gram, num_perm=hash_signatures)
        
      #to do -> insert key and hash to build lsh
      #lsh.insert(....)
        
      input("Press Enter to continue...")
  return d_shingles, d_names  
