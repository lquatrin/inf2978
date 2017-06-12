import sys, os, lsh_test

root = ""
#root = "F:/"
#root = "D:/inf2978t2dataset/"

path = os.path.join(root, "TRAIN_DATASET/")


#######################
# Parametros
#######################
shingle_gram = [3, 4, 5]

# baseado no 'number_of_signatures', gerar as configuracoes [30, 50, 75, 100]
d_r_b = dict()
d_r_b[30]  = [(3, 10), (5, 6), (6, 5)]
d_r_b[50]  = [(5, 10), (2, 25)]
d_r_b[75]  = [(7, 10), (10, 7)]
d_r_b[100] = [(5, 20), (10, 10), (20, 5), (4, 25), (25, 4)]

similarity_threshold = [0.5, 0.6, 0.7, 0.8, 0.9]

# for each shingle size
for s_gram in shingle_gram:
  # hash signatures
  for hash_sig, signatures in d_r_b.items():
    # rows + bands configurations
    for rb in signatures:     
      rows = rb[0]
      bands = rb[1]
 
      # each threshold
      for s_threshold in similarity_threshold:
        lsh_test.LSHTest(path, s_gram, hash_sig, rows, bands, s_threshold)
