import msvcrt as m
import sys, os

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

def ReadSongFiles(path, shingle_gram, hash_signatures, max_documents):
  d_shingles = dict()
  d_minhash = dict()
    
  n_count = 0
  for r,d,f in os.walk(path):
    for file in f:
      pathf = r.replace('\\','/')
      filename = pathf + '/' + file

      d_author_name = pathf[pathf[:pathf.rfind('/')].rfind('/')+1:] + '/' + file
      
      #-------------> Shingle
      #print(filename)
      fshingle = CreateShingle(filename, shingle_gram)

      if fshingle is None:
        continue
      
      d_shingles[d_author_name] = fshingle

      #-------------> MinHash
      d_minhash[d_author_name] = MinHash(num_perm = hash_signatures)
      for d in d_shingles[d_author_name]:
        d_minhash[d_author_name].update(d.encode('utf8'))
	  
      n_count = n_count + 1
      if not (max_documents is None):
        if n_count > max_documents:
          return {'shingle' : d_shingles, 'minhash' : d_minhash, 'number_of_signatures' : hash_signatures, 'n_gram' : shingle_gram}

  return {'shingle' : d_shingles, 'minhash' : d_minhash, 'number_of_signatures' : hash_signatures, 'n_gram' : shingle_gram}