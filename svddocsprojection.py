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
  data_doc = None
  if isinstance(documents, dict):
    # Create DataDocs
    data_doc = np.zeros(shape = (number_of_documents, d))
    for doc_id in range(number_of_documents):
      for word_id, count_w in documents[doc_id].items():
        data_doc[doc_id, word_id] = float(count_w)
  elif isinstance(documents, np.ndarray):
    data_doc = documents.T
        
  print('SVD Case', N, data_doc.shape)
         
  print("SVD")
  # Call SVD for sparse matrices
  s_clock = time.clock()
  #U, S, Vt = np.linalg.svd(data_doc, full_matrices = False)
  U, S, Vt = linalg.svds(data_doc, k = N, which = 'LM')
  f_clock = time.clock()
  svd_time = (f_clock - s_clock)

  s_clock = time.clock()
  S = np.diag(S)

  # https://stats.stackexchange.com/questions/107533/how-to-use-svd-for-dimensionality-reduction-to-reduce-the-number-of-columns-fea
  # Matrix V is used only to map the data from this reduced n-dimensional
  #   space to your original d-dimensional space. If you don't need to map
  #   it back, just leave V out, and done you are.
  # We will not correct the colunm content, because the distance value will be the same.
  #data_doc = np.dot(np.dot(U, S), Vt)
  #data_doc = np.dot(projection, Vt)
  #dunno
  data_doc = data_doc - np.dot(np.dot(U, S), Vt)
  
  #print(max_distortion)
  f_clock = time.clock()
  proj_time = (f_clock - s_clock)

  #http://scikit-bio.org/docs/0.2.0/generated/skbio.stats.distance.html
  #http://stackoverflow.com/questions/1871536/euclidean-distance-between-points-in-two-different-numpy-arrays-not-within
  #https://docs.scipy.org/doc/scipy-0.19.0/reference/spatial.distance.html
  #http://stackoverflow.com/questions/22720864/efficiently-calculating-a-euclidean-distance-matrix-using-numpy
  #https://docs.scipy.org/doc/scipy-0.19.0/reference/spatial.distance.html
  print("Euclidean Distance")
  s_clock = time.clock()
  #projected_distances = sp.distance.pdist(data_doc.T, metric='euclidean')
  #projected_distances, s_time = bwdistance.DoEuclidianDistanceProjDocs(data_doc.T)
  #projected_distances = pdist(data_doc, 'sqeuclidean')

  print("Distortion")
  max_distortion = np.linalg.norm(data_doc)
  #max_distortion, mst = MaxDistortionSVD(mtx_original_distance, projected_distances)
  #print(max_distortion, mst)

  f_clock = time.clock()
  dist_time = (f_clock - s_clock)

  text_file = open(path + str(N) + "_svd_docs.txt", "w")
  text_file.write("%s\t%s\t%s\t%s\n" % ('svd_time', 'proj_time', 'dist_time', 'frobenius'))
  text_file.write("%f\t%f\t%f\t%f\n" % (svd_time, proj_time, dist_time, max_distortion))
  
  text_file.close()
