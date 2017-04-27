import numpy as np

import scipy
from scipy.sparse.linalg import svds
from scipy import sparse

import random

#sparsesvd
#propack

K = 4
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
sU, ss, sV = svds(aX, K, which = 'LM')
diagshape = ss.shape[0]
sS = np.zeros(shape = (diagshape))
for i in range(diagshape):
  sS[i] = ss[diagshape - 1 - i]
sS = np.diag(sS)

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

print(sS)
  
#X = np.random.uniform(size = [40, 20])
#X = scipy.sparse.csc_matrix(X)
#su, ss, svt = svds(X, 10, which = 'LM')

