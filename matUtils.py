import numpy as np
import math



def matrixMultiply1(m1,m2):
    prodM = []
    for i in range(len(m1)): #for each row of m1
        row = m1[i]
        newRow = []
        for j in range(len(m2[0])): #for each column of m2
            y = 0
            for x in range(len(row)):
                rowEl = row[x]
                colEl = m2[x][j]
                y += rowEl*colEl
            newRow.append(y)
        prodM.append(newRow)
    return prodM
	

def matrixMultiply2(orig,rand):
	prodM = np.mat(orig) * rand
	return prodM

#TO DO - programação dinamica (multi eficiente de matrizes)
def matrixMultDim(orig,rand):
    return orig	
	
def distMatrix(proj):
    items = len(proj)
    DistProj = np.empty((items, items))
    a,b = 0,0
    for i in proj:
        b = 0
        for j in proj:
          DistProj[a][b] = np.linalg.norm(i-j)
          b+=1
        a+=1
    return DistProj
	
# normalizada
def calculateSampleDistortion(originalVec, projectedVec):
    return abs((np.dot(projectedVec, projectedVec) / np.dot(originalVec, originalVec)) - 1)


def maxDistortion(list_of_original_vectors, list_of_projected_vectors):
    max_distortion = 0.0
    for original_vector, projected_vector in zip(
            list_of_original_vectors, list_of_projected_vectors):
        curr_distortion = calculateSampleDistortion(original_vector, projected_vector)
        if curr_distortion > max_distortion:
            max_distortion = curr_distortion
    return max_distortion

#probabilidade
def calculateJLLema(number_of_samples, projected_sample_dimension, delta=0.01):
    return math.sqrt(6.0 * math.log((number_of_samples**2)/delta) / projected_sample_dimension)
	
	
