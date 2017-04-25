import numpy as np

import scipy
from scipy.sparse.linalg import svds
from scipy import sparse

import random

#sparsesvd
#propack

def RunSVD(documents, mtx_original_distance, n_cases, repeat, n_words, number_of_documents, path):

  mtx_documents = np.zeros(shape = (n_words, number_of_documents))


  for doc_id in range(0, number_of_documents):
    for id_word, count_w in documents[doc_id].items():
      mtx_documents[id_word][doc_id] = float(count_w)

  # print("Running SVDs")
  #X = scipy.sparse.csc_matrix(mtx_documents)
  #U, S, Vt = svds(X, 10, which = 'LM')

  m_size = 6
  a = np.zeros(shape = (m_size, m_size))
  for i in range(m_size):
    for j in range(m_size):
      a[i][j] = int(random.random() * 11)
  
  U, s, V = np.linalg.svd(a, full_matrices = False)
  S = np.diag(s)

  aX = scipy.sparse.csc_matrix(a)
  #print(min(aX.shape))
    
  
  #'LM' : largest singular values
  #'SM' : smallest singular values
  # size: 1 <= k < min(A.shape)
  sU, ss, sV = svds(aX, m_size-1, which = 'LM')
  sS = np.diag(ss)

  #print(U.shape, V.shape, s.shape)
  #S = np.zeros((9, 6), dtype = complex)
  #S[:6, :6] = np.diag(s)
  #print(np.allclose(a, np.dot(U, np.dot(S, V))))
  #U, s, V = np.linalg.svd(a, full_matrices = False)
  #print(U.shape, V.shape, s.shape)
  #S = np.diag(s)

  print("MATRIZ ORIGINAL")
  print(a)

  print("SVD", U.shape, S.shape, V.shape)
  print(np.dot(U, np.dot(S, V)))

  print("SVD sparse", sU.shape, sS.shape, sV.shape)
  print(np.dot(sU, np.dot(sS, sV)))
  
  #X = np.random.uniform(size = [40, 20])
  #X = scipy.sparse.csc_matrix(X)
  #su, ss, svt = svds(X, 10, which = 'LM')


