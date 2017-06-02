import sys,os

######################################
# 'lshingle' para implementação manual
# 'shingle' para implementação utiilizando a biblioteca datasketch
import shingle as shinglegen

root = ""
#root = "F:/"
#root = "D:/inf2978t2dataset/"

path = os.path.join(root, "TRAIN_DATASET/")

#######################################
# Parametros
n_shingle_gram = 3#4
n_alphabet = 27 #alphabet(26) + white space(1)
similarity_threshold = 0.8
r_rows = 5
b_bands = 10
# tamanho de cada assinatura hash = r_band * b_band

# Ler arquivos de musica
d_shingles, d_minhash, lsh, times = shinglegen.ReadSongFiles(path, n_gram = n_shingle_gram, max_documents = 100, hash_signatures = r_rows*b_bands, lsh_threshold = similarity_threshold, shingle_max_size = n_alphabet**n_shingle_gram, alphabet = n_alphabet)

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
