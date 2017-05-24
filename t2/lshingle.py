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

	# ? ! ' . - " … : ; ,
    content = re.sub("[\\?\\!\\'\\.\\-\"…:;,\\[\\]\\(\\)\\{\\}]", ' ', content)

    print(content)

  #Get a slice: s[start:end], starts in 0
  assert(len(content) >= ngram_size)

  #[' '.join(tokens[i:i+ngram_size]) for i in range(0, len(tokens) - ngram_size + 1)]
  for i in range(ngram_size, len(content)):
    ret_set.add(content[i-ngram_size:i])

  return ret_set

  
