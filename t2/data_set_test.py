import sys,os

######################################
# 'lshingle' para implementação manual
# 'shingle' para implementação utiilizando a biblioteca datasketch
import shingle as shinglegen

root = ""
#root = "F:/"
root = "D:/inf2978t2dataset/"

path = os.path.join(root, "TRAIN_DATASET/")

n_shingle = 3#4
red_sequences = 27**n_shingle #alphabet(26) + white space(1)

similarity_threshold = 0.8
# r * b = hash_functions
r_rows = 5
b_bands = 10

# Ler arquivos de musica
d_shingles, d_minhash, lsh, times = shinglegen.ReadSongFiles(path, n_gram = n_shingle, max_documents = 100, hash_signatures = r_rows*b_bands, lsh_threshold = similarity_threshold, shingle_max_size = red_sequences)

# Criando o arquivo csv
ret_file = open('resfile.csv','w')

#LSH discutido em aula
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

ret_file.close()
