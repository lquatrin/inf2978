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

def MaxDistortionForSVD(original_distance, projected_distance):
    max_distortion = 0.0

    n_docs = original_distance.shape[0]
    index = 0
    for x in range(0, n_docs):
        for y in range(x + 1, n_docs):
            if original_distance[x][y] != 0.0:
                curr_distortion = abs((projected_distance[index] / original_distance[x][y]) - 1.0)
                if curr_distortion > max_distortion:
                    max_distortion = curr_distortion
            index = index + 1
    return max_distortion
                    
def SVDDocsProjection (documents, mtx_original_distance, N, d, number_of_documents, path):
  # Create DataDocs
  data_doc = np.zeros(shape = (number_of_documents, d))
  for doc_id in range(number_of_documents):
    for word_id, count_w in documents[doc_id].items():
      data_doc[doc_id, word_id] = float(count_w)
    
  print('SVD Case', N)
         
  print("SVD")
  # Call SVD for sparse matrices
  s_clock = time.clock()
  U, S, Vt = linalg.svds(data_doc, k = N, which = 'LM')
  f_clock = time.clock()
  svd_time = (f_clock - s_clock)

  print("Generate Original Matrix")
  s_clock = time.clock()
  # Correct diagonal
  # linalg.svds returns eigenvalues on Ascending Order    
  S = np.diag(S)
  
  # https://stats.stackexchange.com/questions/107533/how-to-use-svd-for-dimensionality-reduction-to-reduce-the-number-of-columns-fea
  # Matrix V is used only to map the data from this reduced n-dimensional
  #   space to your original d-dimensional space. If you don't need to map
  #   it back, just leave V out, and done you are.
  # We will not correct the colunm content, because the distance value will be the same.
  data_doc = np.dot(U, np.dot(S, Vt))
  #data_doc = np.dot(projection, Vt)

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
  projected_distances = pdist(data_doc, 'sqeuclidean')
  f_clock = time.clock()
  dist_time = (f_clock - s_clock)

  print("Distortion")
  max_distortion = MaxDistortionForSVD(mtx_original_distance, projected_distances)
  print(max_distortion)

  text_file = open(path + str(N) + "_svd_docs.txt", "w")
  text_file.write("%s\t%s\t%s\t%s\n" % ('svd_time', 'proj_time', 'dist_time', 'distortion'))

  text_file.write("%f\t%f\t%f\t%f\n" % (svd_time, proj_time, dist_time, max_distortion))

  text_file.close()
