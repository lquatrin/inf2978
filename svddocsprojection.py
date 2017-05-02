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
from scipy.spatial.distance import pdist

import os
import gc

def MaxDistortionSVD(original_distance, projected_distance):
    max_distortion = 0.0
    max_strech = 0.0

    n_docs = original_distance.shape[0]
    index = 0
    for x in range(0, n_docs):
        for y in range(x + 1, n_docs):
            if original_distance[x][y] != 0.0:
                curr_distortion = abs((projected_distance[index] / original_distance[x][y]) - 1.0)
                if curr_distortion > max_distortion:
                    max_distortion = curr_distortion
            if projected_distance[index] != 0.0:
                curr_distortion = abs((original_distance[x][y] / projected_distance[index]) - 1.0)
                if curr_distortion > max_strech:
                    max_strech = curr_distortion
            index = index + 1
    return max_distortion, max_strech

def SVDDocsProjection (documents, mtx_original_distance, N, d, number_of_documents, path):
  A = None
  if isinstance(documents, dict):
    # Create DataDocs
    A = np.zeros(shape = (number_of_documents, d))
    for doc_id in range(number_of_documents):
      for word_id, count_w in documents[doc_id].items():
        A[doc_id, word_id] = float(count_w)
  elif isinstance(documents, np.ndarray):
    A = documents.T
        
  print('SVD Case', N, A.shape)
         
  # Call SVD for sparse matrices
  s_clock = time.clock()
  #U, S, Vt = np.linalg.svd(data_doc, full_matrices = False)
  U, vS, Vt = linalg.svds(A, k = N, which = 'LM')
  f_clock = time.clock()

  print('- SVD Time: ', (f_clock - s_clock))

  #Generating A_k
  s_clock = time.clock()
  S = np.diag(vS)
  A_k = np.dot(np.dot(U, S), Vt)
  f_clock = time.clock()
  print('- Ak  Time: ', (f_clock - s_clock))

  #Quality Measure 1:
  # 1 - (||A_k - A|| / ||A||)
  s_clock = time.clock()

  norma_frob = np.linalg.norm(A_k - A)
  norma_frob_orig = np.linalg.norm(A)
  quality_1 = 1.0 - (norma_frob / norma_frob_orig)
  f_clock = time.clock()

  print('- Quality 1: ', (f_clock - s_clock))
  print('  ', quality_1 * 100.0)
  
  #Quality Measure 2
  # 100 * ( (soma_sig)**2 / frob(A)**2)
  s_clock = time.clock()
  quality_2 = 100.0 * (np.sum(vS)**2 / (norma_frob_orig**2))
  f_clock = time.clock()

  print('- Quality 2: ', (f_clock - s_clock))
  print('  ', quality_2)

  #Error Measure  
  s_clock = time.clock()

  f_clock = time.clock()


  #http://scikit-bio.org/docs/0.2.0/generated/skbio.stats.distance.html
  #http://stackoverflow.com/questions/1871536/euclidean-distance-between-points-in-two-different-numpy-arrays-not-within
  #https://docs.scipy.org/doc/scipy-0.19.0/reference/spatial.distance.html
  #http://stackoverflow.com/questions/22720864/efficiently-calculating-a-euclidean-distance-matrix-using-numpy
  #https://docs.scipy.org/doc/scipy-0.19.0/reference/spatial.distance.html
  #print("Euclidean Distance")
  #s_clock = time.clock()
  #projected_distances = sp.distance.pdist(data_doc.T, metric='euclidean')
  #projected_distances, s_time = bwdistance.DoEuclidianDistanceProjDocs(data_doc.T)
  #projected_distances = pdist(data_doc, 'sqeuclidean')

  #print("Distortion")
  #max_distortion = np.linalg.norm(data_doc)
  #max_distortion, mst = MaxDistortionSVD(mtx_original_distance, projected_distances)
  #print(max_distortion, mst)

  #f_clock = time.clock()
  #dist_time = (f_clock - s_clock)

  #text_file = open(path + str(N) + "_svd_docs.txt", "w")
  #text_file.write("%s\t%s\t%s\t%s\n" % ('svd_time', 'proj_time', 'dist_time', 'frobenius'))
  #text_file.write("%f\t%f\t%f\t%f\n" % (svd_time, proj_time, dist_time, max_distortion))
  
  #text_file.close()
