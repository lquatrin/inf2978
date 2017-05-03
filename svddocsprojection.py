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
      if original_distance[x] != 0.0:
        curr_distortion = abs((projected_distance[x] / original_distance[x]) - 1.0)
        if curr_distortion > max_distortion:
          max_distortion = curr_distortion
    return max_distortion


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

  print("SVD", N)

  # Call SVD for sparse matrices
  ##########################################
  s_clock = time.clock()
  U, vS, Vt = linalg.svds(A, k = N, which = 'LM')
  f_clock = time.clock()

  report['time_svd'] = (f_clock - s_clock)

  # Generating A_k
  ##########################################
  s_clock = time.clock()
  S = np.diag(vS)
  A_k = np.dot(U, S)
  f_clock = time.clock()

  report['time_reconstruction'] = (f_clock - s_clock)

  # Max Distortion
  ##########################################
  s_clock = time.clock()
  projected_distances = pdist(A_k, metric='sqeuclidean')
  max_distortion = MaxDistortionSVD(distance_array, projected_distances)
  f_clock = time.clock()

  report['max_distortion'] = max_distortion
  report['time_dist'] = (f_clock - s_clock)

  A_k = np.dot(A_k, Vt)
  A_k = A - A_k
  norma_frob = np.linalg.norm(A_k)
  #Quality Measure 1: % of A
  # 1 - (||A_k - A|| / ||A||)
  norma_frob_orig = np.linalg.norm(A)
  quality_1 = 1.0 - (norma_frob / norma_frob_orig)
 
  report['q1'] = quality_1 * 100.0

  #Quality Measure 2: portion of singular total value
  # 100 * ( (soma_sig)**2 / frob(A)**2)
  quality_2 = 100.0 * (np.linalg.norm(vS)**2 / (norma_frob_orig**2))

  report['q2'] = quality_2
  
  return report
