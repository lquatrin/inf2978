import sys, os, time

from datasketch import MinHash, MinHashLSH

import sutils
import serialization
import numpy as np

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

#--------------> Shingle
# Create shingle for each song
def BuildShingles(path, shingle_gram):
  fn_time = time.clock()
 
  shingles = dict()
  for r,d,f in os.walk(path):
    for file in f:
      pathf = r.replace('\\','/')
      filename = pathf + '/' + file
  
      d_author_name = pathf[pathf[:pathf.rfind('/')].rfind('/')+1:] + '/' + file
      d_author_name = d_author_name.replace('/', '|')
      
      fshingle = CreateShingle(filename, shingle_gram)
      if fshingle is None:
        continue
  
      shingles[d_author_name] = fshingle
      
  fn_time = time.clock() - fn_time
  return {'data' : shingles, 'time' : fn_time}

#--------------> Minhash
def BuildMinHashCollection(path, shingle_gram, hash_signatures):
  d_minhash = dict()

  # Descomentar linhas para serialização dos shingles
  ############## Load Shingles  
  d_shingles = serialization.LoadPickleObject('data/' + 'shingles_' + str(shingle_gram))
  if d_shingles is None:
    d_shingles = BuildShingles(path, shingle_gram)
    serialization.SavePickleObject('data/' + 'shingles_' + str(shingle_gram), d_shingles)
  ############## Load Shingles
  
  ############## MinHash
  minhash_creation_time = time.clock()
  
  for author, fshingle in d_shingles['data'].items():
    d_minhash[author] = MinHash(num_perm = hash_signatures)
    for d in fshingle:
      d_minhash[author].update(d.encode('utf8'))
  
  minhash_creation_time = (time.clock() -   minhash_creation_time) + d_shingles['time']
  ############## MinHash
  
  return {'minhash' : d_minhash, 'time' : minhash_creation_time}

  
#--------------> Shingle + Minhash
def ReadShingleAndBuildMinHash(path, shingle_gram, hash_signatures):
  d_minhash = dict()
  
  minhash_creation_time = time.clock()
  
  generator = np.random.RandomState(1)
  mersenne_prime = (1 << 61) - 1
  r_permutations = np.array([(generator.randint(1, mersenne_prime, dtype=np.uint64), generator.randint(0, mersenne_prime, dtype=np.uint64)) for _ in range(hash_signatures)], dtype=np.uint64).T
  
  for r,d,f in os.walk(path):
    for file in f:
      pathf = r.replace('\\','/')
      filename = pathf + '/' + file

      d_author_name = pathf[pathf[:pathf.rfind('/')].rfind('/')+1:] + '/' + file
      d_author_name = d_author_name.replace('/', '|')
	  
      #-------------> Read and Create Shingle
      fshingle = CreateShingle(filename, shingle_gram)
      if fshingle is None:
        continue

      #-------------> Create MinHash
      d_minhash[d_author_name] = MinHash(num_perm = hash_signatures, permutations = r_permutations)
      for d in fshingle:
        d_minhash[d_author_name].update(d.encode('utf8'))

  minhash_creation_time = (time.clock() -   minhash_creation_time)
   
  return {'minhash' : d_minhash, 'time' : minhash_creation_time, 'permutations' : r_permutations}
  
def ClassShingleAndBuildMinHash(path, shingle_gram, hash_signatures):
  d_minhash = dict()
  
  minhash_creation_time = time.clock()
  
  generator = np.random.RandomState(1)
  mersenne_prime = (1 << 61) - 1
  r_permutations = np.array([(generator.randint(1, mersenne_prime, dtype=np.uint64), generator.randint(0, mersenne_prime, dtype=np.uint64)) for _ in range(hash_signatures)], dtype=np.uint64).T
  
  for r,d,f in os.walk(path):
    for file in f:
      pathf = r.replace('\\','/')
      filename = pathf + '/' + file
	  
      #print(file[2:file.find('.')])
      d_author_name = int(file[2:file.find('.')])
      #print(file[2:file.find('.')], d_author_name)
	  
      #-------------> Read and Create Shingle
      fshingle = CreateShingle(filename, shingle_gram)
      if fshingle is None:
        continue
      
      #-------------> Create MinHash
      d_minhash[d_author_name] = MinHash(num_perm = hash_signatures, permutations = r_permutations)
      for d in fshingle:
        d_minhash[d_author_name].update(d.encode('utf8'))

  minhash_creation_time = (time.clock() -   minhash_creation_time)
   
  return {'minhash' : d_minhash, 'time' : minhash_creation_time, 'permutations' : r_permutations}
 