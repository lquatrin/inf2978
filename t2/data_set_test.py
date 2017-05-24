import sys,os

import numpy as np

import shingle
import lshingle
import time


from datasketch import MinHash, MinHashLSH
root = ""
#root = "F:/"
#root = "D:/inf2978t2dataset/"

path = os.path.join(root, "TRAIN_DATASET/")

n_shingle = 4
red_sequences = 27**n_shingle #alphabet(26) + white space(1)
hash_functions = 50

#MinHash P1
# Já Criar as permutações aqui para usar diretamente em cada doc
#d_permutations = dict()
#for i in range(hash_functions):
#  d_permutations[i] = np.random.permutation(red_sequences)
 
#n_count = 0

# https://ekzhu.github.io/datasketch/lsh.html
lsh_threshold = 0.1
lsh = MinHashLSH(threshold=lsh_threshold,num_perm= hash_functions)

#Read Songs and Create Shingle sets
d_shingles, d_names = lshingle.ReadSongFiles(path, n_gram = n_shingle, max_documents = 100)


#https://stackoverflow.com/questions/14533420/can-you-suggest-a-good-minhash-implementation

similarity_threshold = 0.6
# r * b = hash_functions
r_rows = 5
b_bands = 10
assert((r_rows * b_bands) == hash_functions)
#LSH discutido em aula
    


#Aspectos da implementação
#Plataforma de execução e desempenho computacional do método
#Discussão de como os parâmetros foram escolhidos
#Análise do desempenho do método em relação as medidas de recall e precision para o conjunto de teste
