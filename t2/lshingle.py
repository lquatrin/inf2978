import numpy as np
import msvcrt as m

import sys,os

import re
from collections import defaultdict
from multiprocessing import Process
from datasketch import MinHash, MinHashLSH

#http://www.bogotobogo.com/Algorithms/minHash_Jaccard_Similarity_Locality_sensitive_hashing_LSH.php
#http://maciejkula.github.io/2015/02/01/minhash/
#http://mccormickml.com/2015/06/12/minhash-tutorial-with-python-code/
#https://stackoverflow.com/questions/14533420/can-you-suggest-a-good-minhash-implementation

#list_coef = [27**3, 27**2, 27**1, 27**0]
def CreateShingle(ngram_size, filename, max_hash_val = None):
  ret_set = set()

  if max_hash_val is None:
    max_hash_val = 24**ngram_size
  
  list_coef = [27**3, 27**2, 27**1, 27**0]

  with open(filename, "rb") as f:
    content = f.read().decode("UTF-8")

    if len(content) == 0:
      return ret_set
    
    #Concatenate each line and replace '\n' by ' '
    content = ''.join(content).replace('\n',' ').lower()
    
    #TODO: Remove not used characters: é, ã, ê, ., ;, :, ...

    # ç
    content = re.sub("[ç]"   , 'c', content)  
    # â á à ã
    content = re.sub("[âáàã]", 'a', content)
    # ê é è
    content = re.sub("[êéè]" , 'e', content)
    # î í ì
    content = re.sub("[îíì]" , 'i', content)
    # ô ó ò õ
    content = re.sub("[ôóòõ]", 'o', content)
    # û ú ù
    content = re.sub("[ûúù]" , 'u', content)

    # ? ! ' . - " … : ; , [ ] ( ) { }
    content = re.sub("[\\?\\!\\'\\.\\-\"…:;,\\[\\]\\(\\)\\{\\}]", ' ', content)
    
    # 1 2 3 4 5 6 7 8 9 0
    content = re.sub("[1234567890]", ' ', content)

    #trocar ' ' por '`' para facilitar o hash depois
    content = re.sub(' ', chr(96), content)

    #print(content)

  #Get a slice: s[start:end], starts in 0
  #print(len(content))
  assert(len(content) >= ngram_size)

  #[' '.join(tokens[i:i+ngram_size]) for i in range(0, len(tokens) - ngram_size + 1)]
  for i in range(ngram_size, len(content)):
    #old ret_set.add(content[i-ngram_size:i])
    ret_set.add(sum([a*b for a,b in zip(list_coef, [ord(i)-96 for i in content[i-ngram_size:i]])]) % max_hash_val)

    #utilizando hash ' ' para '`'
    #[ord(i)-96 for i in a]

  return ret_set 

#To Calculate LSH similarity
#sum([u==v for u,v in zip(a,b)])/len(a)

#https://stackoverflow.com/questions/14533420/can-you-suggest-a-good-minhash-implementation
def ReadSongFiles(path, n_gram = 4, max_documents = None, hash_signatures = 10):
  d_names = dict()
  d_shingles = dict()

  # MinHash Permutations
  # Já Criar as permutações aqui para usar diretamente em cada doc
  #d_permutations = dict()
  #for i in range(hash_functions):
  #  d_permutations[i] = np.random.permutation(red_sequences)
   
  if max_documents is None:
    max_documents = sys.maxsize

  n_count = 0
  for r,d,f in os.walk(path):
    for file in f:
      filename = r.replace('\\','/') + '/' + file

      #-------------> Shingle
      #s = time.clock()
      d_names[n_count] = filename
      d_shingles[n_count] = CreateShingle(n_gram,filename)
      #e = time.clock()
      #print(d_shingles, (e - s))
      
      #-------------> MinHash
      #mhash = build_minhash(d_shingles, num_perm=hash_functions)
      
      #to do -> insert key and hash to build lsh
      #lsh.insert(....)

      n_count = n_count + 1

      if n_count >= max_documents:
          return d_shingles, d_names
      #input("Press Enter to continue...")

  return d_shingles, d_names 
