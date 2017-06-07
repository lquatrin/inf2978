import sys, os, time

######################################
# 'lshingle' para implementacao manual
# 'shingle' para implementacao utiilizando a biblioteca datasketch
import shingle as shinglegen

root = ""
#root = "F:/"
root = "D:/inf2978t2dataset/"

path = os.path.join(root, "TRAIN_DATASET/")

from datasketch import MinHash, MinHashLSH 
def duplicates(lsh_index):

  possible_duplicates = []
  for bucket in lsh_index.hashtables:
      for elem in bucket.values():
          if len(elem) > 1:
              possible_duplicates.append(elem)
  
  return possible_duplicates

#######################################
# Parametros
shingle_gram = 4
similarity_threshold = 0.8
rows = 5
bands = 10
max_docs = 100 #None
# tamanho de cada assinatura hash = r_band * b_band

start = time.clock()
# Creating minhashs
d_shingles, d_minhash = shinglegen.ReadSongFiles(path, shingle_gram, rows*bands, max_docs)
print("Read Songs", time.clock() - start)

start = time.clock()
# https://github.com/ekzhu/datasketch
# https://ekzhu.github.io/datasketch/lsh.html
# Define "weights = (r*b / r, r*b / b)" or "params = (r, b)"
lsh = MinHashLSH(threshold = similarity_threshold, num_perm = rows*bands, params = (rows, bands))
for k,v in d_minhash.items():
  lsh.insert(k, v)
print("Create LSH", time.clock() - start)

# Criando o arquivo csv
ret_file = open('resfile.csv','w')

# Checar letras parecidas baseado no valor de 'similarity_threshold'
added_songs = dict()
for key, v_minhash in d_minhash.items():
  if not key in added_songs:
    result = lsh.query(v_minhash)

    for i in range(len(result)):
      added_songs[result[i]] = True
    
    if len(result) > 1:
      ret_file.write(';'.join(result))
      ret_file.write('\n')
      #input(str(len(result)) + ': ' + (';'.join(map(str,result))))

# Fechando arquivo CSV
ret_file.close()
