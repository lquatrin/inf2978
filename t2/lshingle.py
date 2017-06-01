import numpy as np
import msvcrt as m

import sys,os

import llsh
import lminhash

import re, time

from collections import defaultdict
from multiprocessing import Process
from datasketch import MinHash, MinHashLSH

#http://www.bogotobogo.com/Algorithms/minHash_Jaccard_Similarity_Locality_sensitive_hashing_LSH.php
#http://maciejkula.github.io/2015/02/01/minhash/
#http://mccormickml.com/2015/06/12/minhash-tutorial-with-python-code/
#https://stackoverflow.com/questions/14533420/can-you-suggest-a-good-minhash-implementation

#list_coef = [27**3, 27**2, 27**1, 27**0]
def CreateShingle(filename, ngram_size, max_hash_val = None):

  tokens = None
  with open(filename, "rb") as f:
    content = f.read().decode("UTF-8")

    if len(content) == 0:
      return None
    
    #Concatenate each line and replace '\n' by ' '
    content = ''.join(content).replace('\n',' ').lower()

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
    #content = re.sub("[1234567890]", ' ', content)
    content = re.sub("[1]", 'um', content)
    content = re.sub("[2]", 'dois', content)
    content = re.sub("[3]", 'tres', content)
    content = re.sub("[4]", 'quatro', content)
    content = re.sub("[5]", 'cinco', content)
    content = re.sub("[6]", 'seis', content)
    content = re.sub("[7]", 'sete', content)
    content = re.sub("[8]", 'oito', content)
    content = re.sub("[9]", 'nove', content)
    content = re.sub("[0]", 'zero', content)

    #trocar ' ' por '`' para facilitar o hash depois
    content = re.sub(' ', chr(96), content)
	
    tokens = content
	
  #Get a slice: s[start:end], starts in 0
  #print(len(tokens))
  assert(len(tokens) >= ngram_size)

  list_coef = [27**3, 27**2, 27**1, 27**0]
  
  ret_set = set()
  #[' '.join(tokens[i:i+ngram_size]) for i in range(0, len(tokens) - ngram_size + 1)]
  for i in range(ngram_size, len(tokens)):
    #old ret_set.add(tokens[i-ngram_size:i])
    ret_set.add(sum([a*b for a,b in zip(list_coef, [ord(i)-96 for i in tokens[i-ngram_size:i]])]) % max_hash_val)
   
  return ret_set 
  
def CalculateMinHash(shingle, n_signatures, shingle_max_size, permutations):
  minhash = np.zeros(n_signatures)
  
  for i in range(n_signatures):
    for j in range(shingle_max_size):
      if permutations[i][j] in shingle:
        minhash[i] = j
  
  return minhash
 
#https://stackoverflow.com/questions/14533420/can-you-suggest-a-good-minhash-implementation
def ReadSongFiles(path, n_gram = 4, max_documents = None, hash_signatures = 10, lsh_threshold = 0.7, shingle_max_size = None):
  assert(not shingle_max_size is None)
  
  d_times = dict()
  d_times["data_creation"] = 0
  
  d_shingles = dict()
  d_minhash = dict()

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
	  
      fshingle = CreateShingle(filename, n_gram, max_hash_val = shingle_max_size)
	  	  
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
