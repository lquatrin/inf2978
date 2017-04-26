import time
import math
import random
import bwreaders
import bwdistance
import bwnumbergen
import bwserialization
import bwprojection
import bwmath

import numpy as np

import os
import gc

import randomprojection as lrp

# 4.1. Obtenha uma matriz aleatoria de n linhas e d colunas pelo metodo de Achiloptas e pelo metodo dado em aula, onde d e o tamanho do vocaulario.
# 4.2. Messa o tempo computacional da geracao das matrizes
# 4.3. Projete os 3000 documentos no espaco Rn atraves das matrizes geradas. Messa o tempo da projecao
# TODO
# MATRIX_n_d * VETOR_d_1 = VERTO_n_1
# 4.4. Messa o tempo para obter todas as distancias entre os pontos projetados
# 4.5. Calcule a distors˜ao maxima em relacao aos dados originais.
# Achiloptas
# 4.6. Calcule o limite superior da distorsao previsto pelo Lema de J.L.

def RunVersion01(documents, mtx_original_distance, n_cases, repeat, d, number_of_documents, path, do_achiloptas, do_randomproj):
  for N in n_cases:
    n = N

    #se N for maior que 4096
    if N > 4096:
      break
    
    print("V1 Caso: ", N)
    #matrizes com os tempos:
    # . número de casos (7)
    # . número de repetições (30)
    # . número de operações x2
    #   1. matriz achiloptas
    #   2. projeção achiloptas
    #   3. tempo para obter novas distâncias
    ########################################
    #   4. matriz random proj
    #   5. projeção random proj
    #   6. tempo para obter novas distâncias
    v1_timers = np.zeros(shape = (6))
    v1_distortions = np.zeros(shape = (2, 3)) # mean, min, max
    # Set initial Min Max Distortions
    for x in range(2):
      v1_distortions[x][1] = float('inf')
      v1_distortions[x][2] = -float('inf')

    if do_achiloptas == True:
      print("  . Achiloptas")
      for ith_repeat in range(repeat):
        projected_documents = None
        Proj_DistanceMatrix = None
        projection_matrix = None

        # Achiloptas
        # 4.1 4.2
        projection_matrix, s_time = bwnumbergen.GenerateRandomAchiloptasMatrix(n,d)
        v1_timers[0] += s_time

        # 4.3
        s_clock = time.clock()
        projected_documents = bwprojection.ProjectDocuments(documents, projection_matrix, n, number_of_documents)
        projected_documents = projected_documents * math.sqrt(3/n)
        f_clock = time.clock()
        v1_timers[1] += (f_clock - s_clock)

        # 4.4
        Proj_DistanceMatrix, s_time = bwdistance.DoEuclidianDistanceProjDocs(projected_documents)
        v1_timers[2] += s_time

        # 4.5
        max_distortion = bwmath.MaxDistortion(mtx_original_distance, Proj_DistanceMatrix)
        v1_distortions[0][0] += max_distortion
        v1_distortions[0][1] = min(max_distortion, v1_distortions[0][1])
        v1_distortions[0][2] = max(max_distortion, v1_distortions[0][2])

      # compute results
      text_file = open(path + str(N) + "_v1_achiloptas.txt", "w")
      for x in range(0, 3):
        v1_timers[x] = v1_timers[x] / (float(repeat))
      text_file.write("%f\n%f\n%f\n" % (v1_timers[0], v1_timers[1], v1_timers[2]))
      v1_distortions[0][0] = v1_distortions[0][0] / float(repeat)
      text_file.write("%f\t%f\t%f" % (v1_distortions[0][0], v1_distortions[0][1], v1_distortions[0][2]))
      text_file.close()    

    if do_randomproj == True:
      print("  . Random Projections")
      for ith_repeat in range(repeat):
        ret_data = lrp.RandomProjection(number_of_documents, documents, mtx_original_distance, d, n)

        v1_timers[3] += ret_data['gen_time']
        v1_timers[4] += ret_data['proj_time']
        v1_timers[5] += ret_data['dist_time']

        max_distortion = ret_data['distortion']

        v1_distortions[1][0] += max_distortion
        v1_distortions[1][1] = min(max_distortion, v1_distortions[1][1])
        v1_distortions[1][2] = max(max_distortion, v1_distortions[1][2])

      # compute results
      text_file = open(path + str(N) + "_v1_randomproj.txt", "w")
      for x in range(3, 6):
        v1_timers[x] = v1_timers[x] / (float(repeat))
      text_file.write("%f\n%f\n%f\n" % (v1_timers[3], v1_timers[4], v1_timers[5]))

      v1_distortions[1][0] = v1_distortions[1][0] / float(repeat)
      text_file.write("%f\t%f\t%f" % (v1_distortions[1][0], v1_distortions[1][1], v1_distortions[1][2]))
      text_file.close()
      
      # 4.6
      text_file = open(path + str(N) + "_v1_JL.txt", "w")
      text_file.write("%f" % (bwmath.CalculateJLLema(d, n)))
      text_file.close()


def RunVersion02(documents, mtx_original_distance, n_cases, repeat, d, number_of_documents, path, do_achiloptas, do_randomproj):
  for N in n_cases:
    n = N
    
    print("V2 Caso: ", N)

    #matrizes com os tempos:
    # . número de casos (7)
    # . número de repetições (30)
    # . número de operações x2
    #   1. matriz e projeção achiloptas
    #   2. tempo para obter novas distâncias
    ########################################
    #   3. matriz e projeção random proj
    #   4. tempo para obter novas distâncias
    v2_timers = np.zeros(shape = (4))
    v2_distortions = np.zeros(shape = (2, 3)) # mean, min, max
    # Set initial Min Max Distortions
    for x in range(2):
      v2_distortions[x][1] = float('inf')
      v2_distortions[x][2] = -float('inf')

    if do_achiloptas == True:
      print("  . Achiloptas")
      for ith_repeat in range(repeat):
        projected_documents = None
        Proj_DistanceMatrix = None

        # Achiloptas
        # 4.1 4.2 4.3
        s_clock = time.clock()
        projected_documents = bwprojection.GenerateAndProjectDocumentsAchiloptas(documents, n, number_of_documents, d)
        projected_documents = projected_documents * math.sqrt(3/n)
        f_clock = time.clock()
        v2_timers[0] += (f_clock - s_clock)

        # 4.4
        Proj_DistanceMatrix, s_time = bwdistance.DoEuclidianDistanceProjDocs(projected_documents)
        v2_timers[1] += s_time

        # 4.5
        max_distortion = bwmath.MaxDistortion(mtx_original_distance, Proj_DistanceMatrix)
        v2_distortions[0][0] += max_distortion
        v2_distortions[0][1] = min(max_distortion, v2_distortions[0][1])
        v2_distortions[0][2] = max(max_distortion, v2_distortions[0][2])

      # compute results
      text_file = open(path + str(N) + "_v2_achiloptas.txt", "w")
      for x in range(0, 2):
        v2_timers[x] = v2_timers[x] / (float(repeat))
      text_file.write("%f\n%f\n" % (v2_timers[0], v2_timers[1]))
      v2_distortions[0][0] = v2_distortions[0][0] / float(repeat)
      text_file.write("%f\t%f\t%f" % (v2_distortions[0][0], v2_distortions[0][1], v2_distortions[0][2]))
      text_file.close()

    if do_randomproj == True:
      print("  . Random Projections")
      for ith_repeat in range(repeat):
        ret_data = lrp.RandomProjection(number_of_documents, documents, mtx_original_distance, d, n, use_less_memory = True)
        
        v2_timers[2] += ret_data['gen_proj_time']
        v2_timers[3] += ret_data['dist_time']

        max_distortion = ret_data['distortion']
        
        v2_distortions[1][0] += max_distortion
        v2_distortions[1][1] = min(max_distortion, v2_distortions[1][1])
        v2_distortions[1][2] = max(max_distortion, v2_distortions[1][2])

      # compute results
      text_file = open(path + str(N) + "_v2_randomproj.txt", "w")
      for x in range(2, 4):
        v2_timers[x] = v2_timers[x] / (float(repeat))
      text_file.write("%f\n%f\n" % (v2_timers[2], v2_timers[3]))

      v2_distortions[1][0] = v2_distortions[1][0] / float(repeat)
      text_file.write("%f\t%f\t%f" % (v2_distortions[1][0], v2_distortions[1][1], v2_distortions[1][2]))
      text_file.close()
      
      # 4.6
      text_file = open(path + str(N) + "_v2_JL.txt", "w")
      text_file.write("%f" % (bwmath.CalculateJLLema(d, n)))
      text_file.close()   
