import sys,os

import shingle

root = ""
#root = "F:/"
#root = "D:/inf2978t2dataset/"

path = os.path.join(root, "TRAIN_DATASET/")

n_shingle = 4
red_sequences = 27**n_shingle #alphabet(26) + white space(1)

similarity_threshold = 0.9
# r * b = hash_functions
r_rows = 5
b_bands = 10

#Read Songs and Create Shingle sets
d_shingles, d_minhash, lsh = shingle.ReadSongFiles(path, n_gram = n_shingle, max_documents = 5000, hash_signatures = r_rows*b_bands, lsh_threshold = similarity_threshold)

#LSH discutido em aula
added_songs = dict()
for key, v_minhash in d_minhash.items():
  if not key in added_songs:
    result = lsh.query(v_minhash)

    for i in range(len(result)):
      added_songs[result[i]] = True
    
    if len(result) > 1:
      input(str(len(result)) + ': ' + (';'.join(map(str,result))))

#Aspectos da implementação
#Plataforma de execução e desempenho computacional do método
#Discussão de como os parâmetros foram escolhidos
#Análise do desempenho do método em relação as medidas de recall e precision para o conjunto de teste
