import numpy as np
import msvcrt as m
import re
from collections import defaultdict
from multiprocessing import Process
from datasketch import MinHash, MinHashLSH


def CreateShingle(ngram_size, filename):
  ret_set = set()

  with open(filename, "rb") as f:
    content = f.read().decode("UTF-8")

    #Concatenate each line and replace '\n' by ' '
    content = ''.join(content).replace('\n',' ').lower()
    
    #TODO: Remove not used characters: é, ã, ê, ., ;, :, ...
    content = content.replace('ç', 'c')
    
    content = content.replace('â', 'a').replace('á', 'a').replace('à', 'a').replace('ã', 'a')
    content = content.replace('ê', 'e').replace('é', 'e').replace('è', 'e')
    content = content.replace('î', 'i').replace('í', 'i').replace('ì', 'i')
    content = content.replace('ô', 'o').replace('ó', 'o').replace('ò', 'o').replace('õ', 'o')
    content = content.replace('û', 'u').replace('ú', 'u').replace('ù', 'u')

    content = content.replace('!', ' ').replace('?', ' ').replace('.', ' ')
    
    content = content.replace('-', ' ').replace("'", ' ').replace('…', ' ').replace('\"', ' ')
    content = content.replace(';', ' ').replace(':', ' ').replace(',', ' ')

    content = content.replace('(', ' ').replace('[', ' ').replace('{', ' ')
    content = content.replace(')', ' ').replace(']', ' ').replace('}', ' ')

    print(content)

  #Get a slice: s[start:end], starts in 0
  assert(len(content) >= ngram_size)

  #[' '.join(tokens[i:i+ngram_size]) for i in range(0, len(tokens) - ngram_size + 1)]
  for i in range(ngram_size, len(content)):
    ret_set.add(content[i-ngram_size:i])

  return ret_set

#with open("file.txt", "r") as ins:
#    array = []
#    for line in ins:
#        array.append(line)
 
def CreateShingle2(input,ngram_size):
  
  with open(input, "rb") as f:
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

  
