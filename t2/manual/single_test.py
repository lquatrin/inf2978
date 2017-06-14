import sys, os, mlsh_test

root = ""
#root = "F:/"
root = "D:/inf2978t2dataset/"

path = os.path.join(root, "TRAIN_DATASET3/")

#######################
# Parametros
#######################
shingle_gram = int(sys.argv[1])
number_of_signatures = int(sys.argv[2])
rows = int(sys.argv[3])
bands = int(sys.argv[4])
similarity_threshold = float(sys.argv[5])

mlsh_test.ManualLSHTest(path, shingle_gram, number_of_signatures, rows, bands, similarity_threshold)