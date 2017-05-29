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
      return set('')
    
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

    tokens = content

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


def ReadSongFiles(path, n_gram = 4, max_documents = None, hash_signatures = 50, lsh_threshold = 0.9):
  d_shingles = dict()
  d_minhash = dict()

  # https://ekzhu.github.io/datasketch/lsh.html
  lsh = MinHashLSH(threshold = lsh_threshold, num_perm = hash_signatures)


  count = 0
  for r,d,f in os.walk(path):
    for file in f:
      pathf = r.replace('\\','/')
      filename = pathf + '/' + file

      d_author_name = pathf[pathf[:pathf.rfind('/')].rfind('/')+1:] + '/' + file
      
      #-------------> Shingle
      #print(filename)
      d_shingles[d_author_name] = CreateShingle(filename, n_gram)
      #print(d_shingles)

      #-------------> MinHash
      d_minhash[d_author_name] = MinHash(num_perm = hash_signatures)
      for d in d_shingles[d_author_name]:
        d_minhash[d_author_name].update(d.encode('utf8'))

      lsh.insert(d_author_name, d_minhash[d_author_name])
      
      count = count + 1
      if not (max_documents is None):
        if count > max_documents:
          return d_shingles, d_minhash, lsh
      
      #input("Press Enter to continue...")

  return d_shingles, d_minhash, lsh
