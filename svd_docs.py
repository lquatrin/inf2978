import time
import math
import random
import bwreaders
import bwdistance
import bwnumbergen
import bwserialization
import bwprojection
import bwmath

from scipy.sparse import linalg
from scipy import spatial as sp


import numpy as np

import os
import gc

import bwruns


DOCWORD_FILE = "./docword.nytimes.txt"
VOCAB_FILE = "vocab.nytimes.txt"

# 1 2
# 1. Baixe o dataset Bag of Words da UCI (arquivo NyTimes). Cerca de 300k docs e vocabulario com 102650 termos
# 2. Crie uma bag of words para os 3000 primeiros documentos
word_list = bwreaders.ReadVocabulary(VOCAB_FILE)

D_t_work = 3000
table_docs = bwreaders.ReadDocuments(DOCWORD_FILE, D_t_work)


documents = table_docs[0]

# n documentos
D = table_docs[1]
# n palavras
W = table_docs[2]
# n entradas
NNZ = table_docs[3]


r_mat = np.zeros(shape = (D_t_work,W))

for doc_id in range(D_t_work):
      #for each word
      for word_id, count_w in documents[doc_id].items():
        r_mat[doc_id, word_id] = count_w 

timers = np.zeros(shape = (4))
# 3
# 3. Calcule a distancia entre cada par de pontos atraves da forca bruta e messa o tempo computacional deste procedimento. Armazene estes valores. Utilize dois loops para fazer isso e implemente o calculo da distancia
s_clock = time.clock()
mtx_original_distance = bwdistance.GenerateOriginalDistanceMatrix(D_t_work, W, documents)
f_clock = time.clock()
timers[0] += (f_clock - s_clock)

repeat = 30
n_cases = [ 4, 16, 64, 256, 1024, 4096, 15768 ]

for N in n_cases:
  s_clock = time.clock()
  #svd for the documents 
  U_r,d_r,V_r = linalg.svds(r_mat)
  f_clock = time.clock()
  timers[1] += (f_clock - s_clock)
  
  s_clock = time.clock()
  
  for ith_repeat in range(repeat):
    dim = N
    
    U_r_k = U_r[:,:dim]
    d_r_k = d_r[:dim]
    V_r_k = V_r[:dim,:]
     
    projection = np.matrix(U_r_k) * np.diag(d_r_k) * np.matrix(V_r_k)
    
    f_clock = time.clock()
    
    timers[2] += (f_clock - s_clock)
    
    s_clock = time.clock()
    
    #TO DO - Ta estourando a distancia 
    projected_distances= sp.distance.pdist(projection.T, metric='euclidean')
    #Proj_DistanceMatrix, s_time = bwdistance.DoEuclidianDistanceProjDocs(projection)
    
    f_clock = time.clock()
    timers[3] += (f_clock - s_clock)
    
    max_distortion = bwmath.MaxDistortion(mtx_original_distance, projected_distances)
  
  text_file = open(path + str(N) + "svd.txt", "w")
  for x in range(2, 4):
    timers[x] = timers[x] / (float(repeat))
  text_file.write("%f\n%f\n" % (timers[2], timers[3]))
  text_file.close()

  
  
  