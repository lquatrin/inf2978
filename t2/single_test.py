import sys, os, lsh_test

root = ""
#root = "F:/"
#root = "D:/inf2978t2dataset/"

path = os.path.join(root, "TRAIN_DATASET/")

#######################
# Parametros
#######################
shingle_gram = int(sys.argv[1])
number_of_signatures = int(sys.argv[2])
rows = int(sys.argv[3])
bands = int(sys.argv[4])
similarity_threshold = float(sys.argv[5])

lsh_test.LSHTest(path, shingle_gram, number_of_signatures, similarity_threshold, rows = rows, bands = bands)