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

import scipy
import numpy as np

import os
import gc

import bwruns

DOCWORD_FILE = "../docword.nytimes.txt"
VOCAB_FILE = "vocab.nytimes.txt"

word_list = bwreaders.ReadVocabulary(VOCAB_FILE)

D_t_work = 3000
table_docs = bwreaders.ReadDocuments(DOCWORD_FILE, D_t_work)

documents = table_docs[0]

D = table_docs[1]
W = table_docs[2]
NNZ = table_docs[3]

# Create DataDocs
data_doc = np.zeros(shape = (D_t_work, W))
for doc_id in range(D_t_work):
  for word_id, count_w in documents[doc_id].items():
    data_doc[doc_id, word_id] = float(count_w)

mtx_original_distance = bwdistance.GenerateOriginalDistanceMatrix(D_t_work, W, documents)

n_cases = [ 4 ]#, 16, 64, 256 ]
for N in n_cases:
  print('Case', N)

  U, s, Vt = linalg.svds(data_doc, k = N, which = 'LM')

  print(U.shape, s.shape, Vt.shape)
  
  # https://stats.stackexchange.com/questions/107533/how-to-use-svd-for-dimensionality-reduction-to-reduce-the-number-of-columns-fea
  projection = np.dot(U, np.diag(s))
  #projection = np.dot(projection, Vt)
    
  #TO DO - Ta estourando a distancia 
  print(projection.shape)
  projected_distances, s_time = bwdistance.DoEuclidianDistanceProjDocs(projection.T)

  print(scipy.linalg.norm(data_doc))
  print(scipy.linalg.norm(projection.T))
  print(scipy.linalg.norm(mtx_original_distance - projected_distances))
 
  max_distortion = bwmath.MaxDistortion(mtx_original_distance, projected_distances)
  print("Distorsão:", max_distortion)  
  
