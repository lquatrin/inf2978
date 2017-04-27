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

def SVDDocsProjection (data_doc, mtx_original_distance, N, d, number_of_documents, path):
  print('SVD Case', N)
         
  text_file = open(path + str(N) + "_svd_docs.txt", "w")
  text_file.write("%s\t%s\t%s\t%s\n" % ('svd_time', 'proj_time', 'dist_time', 'distortion'))

  # Call SVD for sparse matrices
  s_clock = time.clock()
  U, s_autoval, Vt = linalg.svds(data_doc, k = N, which = 'LM')
  f_clock = time.clock()
  svd_time = (f_clock - s_clock)

  s_clock = time.clock()
  # Correct diagonal
  # linalg.svds returns eigenvalues on Ascending Order
  diagshape = s_autoval.shape[0]
  s = np.zeros(shape = (diagshape))
  for i in range(diagshape):
    s[i] = s_autoval[diagshape - 1 - i]
  #print(s)
  
  # https://stats.stackexchange.com/questions/107533/how-to-use-svd-for-dimensionality-reduction-to-reduce-the-number-of-columns-fea
  # Matrix V is used only to map the data from this reduced n-dimensional
  #   space to your original d-dimensional space. If you don't need to map
  #   it back, just leave V out, and done you are.
  projection = np.dot(U, np.diag(s))
  #projection = np.dot(projection, Vt)
  f_clock = time.clock()
  proj_time = (f_clock - s_clock)

  s_clock = time.clock()
  #projected_distances = sp.distance.pdist(projection.T, metric='euclidean')
  projected_distances, s_time = bwdistance.DoEuclidianDistanceProjDocs(projection.T)
  f_clock = time.clock()
  dist_time = (f_clock - s_clock)
  
  max_distortion = bwmath.MaxDistortion(mtx_original_distance, projected_distances)

  text_file.write("%f\t%f\t%f\t%f\n" % (svd_time, proj_time, dist_time, max_distortion))

  text_file.close()
