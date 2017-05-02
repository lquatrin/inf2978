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

def SVDDocsProjection (documents, distance_array, N, d, number_of_documents, path):
  A = None
  report = dict()
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
  U, vS, Vt = linalg.svds(A, k = N, which = 'LM')
  f_clock = time.clock()

  report['svdtime'] = (f_clock - s_clock)

  #Generating A_k
  s_clock = time.clock()
  S = np.diag(vS)
  A_k = np.dot(np.dot(U, S), Vt)
  f_clock = time.clock()

  report['akbuildtime'] = (f_clock - s_clock)
  
  #Quality Measure 1: % of A
  # 1 - (||A_k - A|| / ||A||)

  A_k = A - A_k
  s_clock = time.clock()
  norma_frob = np.linalg.norm(A_k)
  f_clock = time.clock()

  report['time_espectralnorm'] = (f_clock - s_clock)
  report['espectralnorm'] = norma_frob**2
  
  #s_clock = time.clock()
  norma_frob_orig = np.linalg.norm(A)
  quality_1 = 1.0 - (norma_frob / norma_frob_orig)
  f_clock = time.clock()

  report['time_q1'] = (f_clock - s_clock)
  report['q1'] = quality_1 * 100.0
  
  #Quality Measure 2: portion of singular total value
  # 100 * ( (soma_sig)**2 / frob(A)**2)
  s_clock = time.clock()
  quality_2 = 100.0 * (np.linalg.norm(vS)**2 / (norma_frob_orig**2))
  f_clock = time.clock()

  report['time_q2'] = (f_clock - s_clock)
  report['q2'] = quality_2

  #Error Measure
  max_err = -float(math.inf)
  s_clock = time.clock()
  D = np.dot(A_k, A.T)
  max_err = np.amax(abs(D))
  f_clock = time.clock()

  report['time_maxerr'] = (f_clock - s_clock)
  report['maxerr'] = max_err

  #Approximation error
  # ||A - Ak|| = s_k+1

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

  return report
