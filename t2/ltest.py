import sys,os
import lshingle

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
d_shingles, d_minhash, lsh = lshingle.ReadSongFiles(path, n_gram = n_shingle, max_documents = 1000, hash_signatures = r_rows*b_bands, lsh_threshold = similarity_threshold, shingle_max_size = red_sequences)

lsh.EvaluateSimiliarities()

#LSH discutido em aula
added_songs = dict()
for key, v_minhash in d_minhash.items():
  if not key in added_songs:
    result = lsh.query(v_minhash)

    for i in range(len(result)):
      added_songs[result[i]] = True
    
    if len(result) > 1:
      input(str(len(result)) + ': ' + (';'.join(map(str,result))))
