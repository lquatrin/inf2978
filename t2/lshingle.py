import numpy as np
import msvcrt as m
import re
from collections import defaultdict
from multiprocessing import Process
from datasketch import MinHash, MinHashLSH


#list_coef = [27**3, 27**2, 27**1, 27**0]
def CreateShingle(ngram_size, filename, max_hash_val = None):
  ret_set = set()

  if max_hash_val is None:
    max_hash_val = 24**ngram_size
  
  list_coef = [27**3, 27**2, 27**1, 27**0]

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

    # ? ! ' . - " … : ; ,
    content = re.sub("[\\?\\!\\'\\.\\-\"…:;,\\[\\]\\(\\)\\{\\}]", ' ', content)
    content = re.sub("[1234567890]", ' ', content)

    #trocar ' ' por '`' para facilitar o hash depois
    content = re.sub(' ', chr(96), content)

    print(content)

  #Get a slice: s[start:end], starts in 0
  assert(len(content) >= ngram_size)

  #[' '.join(tokens[i:i+ngram_size]) for i in range(0, len(tokens) - ngram_size + 1)]
  for i in range(ngram_size, len(content)):
    #old ret_set.add(content[i-ngram_size:i])
    ret_set.add(sum([a*b for a,b in zip(list_coef, [ord(i)-96 for i in content[i-ngram_size:i]])]) % max_hash_val)

    #utilizando hash ' ' para '`'
    #[ord(i)-96 for i in a]

  return ret_set 
