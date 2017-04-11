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
	
#dist = sqrt((xa-xb)^2 + ... + (za-zb)^2)
def euclidean(vec1,vec2):
	size = range(vec1)
	dist = 0
	for i in size:
	   dist = dist + (vec1[i] - vec2[i]) * (vec1[i] - vec2[i])
	return np.sqrt(dist)
	
	
def distMatrix(proj):
    DistProj = np.empty((proj[0], proj[0]))
    items = len(proj[0])
    for i in items:
        for j in items:
            if i == j:
                DistProj[i][j] = 0
            else:
                DistProj[i][j] = euclidean(proj[i], proj[j])
     
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
	
	