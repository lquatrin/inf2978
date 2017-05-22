import sys,os

import numpy as np

root = "D:/inf2978t2dataset/"
path = os.path.join(root, "TRAIN_DATASET/")

n_count = 0
for r,d,f in os.walk(path):
    for file in f:
        filename = r.replace('\\','/') + '/' + file
        n_count = n_count + 1
        #ler cada documento
        #print(filename)

print(n_count)

n_shingle = 4
red_sequences = 27**n_shingle #alphabet(26) + white space(1)
#Shingles




hash_functions = 50     
#MinHash
for i in range(hash_functions):
  l_permutation = np.random.permutation(red_sequences)
  #get the signature based on shingle





similarity_threshold = 0.6
# r * b = hash_functions
r_rows = 5
b_bands = 10
#LSH discutido em aula



      


#Aspectos da implementação
#Plataforma de execução e desempenho computacional do método
#Discussão de como os parâmetros foram escolhidos
#Análise do desempenho do método em relação as medidas de recall e precision para o conjunto de teste
