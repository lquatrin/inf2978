import sys, os, lsh_test

root = ""
#root = "F:/"
#root = "D:/inf2978t2dataset/"

path = os.path.join(root, "TRAIN_DATASET/")


#######################
# Parametros
#######################
shingle_gram = [3, 4, 5]
similarity_threshold = [0.7, 0.8, 0.9]

d_r_b = dict()
# baseado no 'number_of_signatures', gerar as configuracoes
number_of_signatures = [30, 40, 50, 60, 70, 100]
d_r_b[30]  = [(3, 10), (5, 6), (6, 5)]
d_r_b[40]  = [(4, 10), (5, 8), (8, 5)]
d_r_b[50]  = [(5, 10), (2, 25)]
d_r_b[60]  = [(6, 10), (5, 12)]
d_r_b[70]  = [(7, 10), (10, 7)]
d_r_b[100] = [(5, 20), (10, 10), (20, 5), (4, 25), (25, 4)]


for s_gram in shingle_gram:
  for hash_sig, signatures in d_r_b.items():
    for rb in signatures:     
      rows = rb[0]
      bands = rb[1]
	  
      for s_threshold in similarity_threshold:
        lsh_test.LSHTest(path, s_gram, hash_sig, rows, bands, s_threshold)
