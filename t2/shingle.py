import numpy as np
import msvcrt as m
import re, os
from collections import defaultdict
from multiprocessing import Process
from datasketch import MinHash, MinHashLSH
 
def CreateShingle(finput, ngram_size):

  tokens = None
  with open(finput, "rb") as f:
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

    tokens = content

  if ngram_size > len(tokens):
      return ''.join(tokens)
  
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
      print(filename)
      d_shingles = CreateShingle(filename, n_gram)
      print(d_shingles)

      #-------------> MinHash
      #mhash = build_minhash(n_gram, num_perm=hash_signatures)
        
      #to do -> insert key and hash to build lsh
      #lsh.insert(....)
        
      input("Press Enter to continue...")
  return d_shingles, d_names  
