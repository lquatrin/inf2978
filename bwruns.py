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
import achlioptas as acl

# 4.1. Obtenha uma matriz aleatoria de n linhas e d colunas pelo metodo de Achiloptas e pelo metodo dado em aula, onde d e o tamanho do vocaulario.
# 4.2. Messa o tempo computacional da geracao das matrizes
# 4.3. Projete os 3000 documentos no espaco Rn atraves das matrizes geradas. Messa o tempo da projecao
# TODO
# MATRIX_n_d * VETOR_d_1 = VERTO_n_1
# 4.4. Messa o tempo para obter todas as distancias entre os pontos projetados
# 4.5. Calcule a distors˜ao maxima em relacao aos dados originais.
# Achiloptas
# 4.6. Calcule o limite superior da distorsao previsto pelo Lema de J.L.

def ReportV1Results(text_file, repeat, v_timers, global_mean_distortion, global_min_distortion, global_max_distortion):
  text_file.write("%d\n" % (repeat))   
  for x in range(0, 3):
    v_timers[x] = v_timers[x] / (float(repeat))
  text_file.write("%f\n%f\n%f\n" % (v_timers[0], v_timers[1], v_timers[2]))
      
  global_mean_distortion = global_mean_distortion / float(repeat)
  text_file.write("%f\t%f\t%f" % (global_mean_distortion, global_min_distortion, global_max_distortion))
  
def RunVersion01(documents, mtx_original_distance, N, repeat, d, number_of_documents, path, do_achiloptas, do_randomproj):
  n = N

  #se N for maior que 4096
  if N > 4096:
    return
    
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
    

  if do_achiloptas == True:
    print("  . Achiloptas")

    v_timers = np.zeros(shape = (3))
    global_mean_distortion = 0.0
    global_min_distortion = float('inf')
    global_max_distortion = -float('inf')
      
    text_file = open(path + str(N) + "_v1_achiloptas.txt", "w")
    text_file.write("%s\t%s\t%s\t%s\t%s\n" % ('case', 'gen_time', 'proj_time', 'dist_time', 'distortion'))
      
    for ith_repeat in range(repeat):
      ret_data = acl.Achlioptas(number_of_documents, documents, mtx_original_distance, d, n)
        
      v_timers[0] += ret_data['gen_time']
      v_timers[1] += ret_data['proj_time']
      v_timers[2] += ret_data['dist_time']

      max_distortion = ret_data['distortion']

      text_file.write("%d\t%f\t%f\t%f\t%f\n" % (ith_repeat + 1, ret_data['gen_time'], ret_data['proj_time'], ret_data['dist_time'], ret_data['distortion']))

      global_mean_distortion += max_distortion
      global_min_distortion = min(max_distortion, global_min_distortion)
      global_max_distortion = max(max_distortion, global_max_distortion)

    # compute results
    ReportV1Results(text_file, repeat, v_timers, global_mean_distortion, global_min_distortion, global_max_distortion)
    text_file.close()    

  ##############################################################################
    
  if do_randomproj == True:
    print("  . Random Projections")

    v_timers = np.zeros(shape = (3))
    global_mean_distortion = 0.0
    global_min_distortion = float('inf')
    global_max_distortion = -float('inf')
      
    text_file = open(path + str(N) + "_v1_randomproj.txt", "w")
    text_file.write("%s\t%s\t%s\t%s\t%s\n" % ('case', 'gen_time', 'proj_time', 'dist_time', 'distortion'))
      
    for ith_repeat in range(repeat):
      ret_data = lrp.RandomProjection(number_of_documents, documents, mtx_original_distance, d, n)

      v_timers[0] += ret_data['gen_time']
      v_timers[1] += ret_data['proj_time']
      v_timers[2] += ret_data['dist_time']

      max_distortion = ret_data['distortion']

      text_file.write("%d\t%f\t%f\t%f\t%f\n" % (ith_repeat + 1, ret_data['gen_time'], ret_data['proj_time'], ret_data['dist_time'], ret_data['distortion']))

      global_mean_distortion += max_distortion
      global_min_distortion = min(max_distortion, global_min_distortion)
      global_max_distortion = max(max_distortion, global_max_distortion)

    # compute results
    ReportV1Results(text_file, repeat, v_timers, global_mean_distortion, global_min_distortion, global_max_distortion)
    text_file.close()
    
    # 4.6
    text_file = open(path + str(N) + "_v1_JL.txt", "w")
    text_file.write("%f" % (bwmath.CalculateJLLema(d, n)))
    text_file.close()


def ReportV2Results(text_file, repeat, v_timers, global_mean_distortion, global_min_distortion, global_max_distortion):
  text_file.write("%d\n" % (repeat)) 
  for x in range(0, 2):
    v_timers[x] = v_timers[x] / (float(repeat))
  text_file.write("%f\n%f\n" % (v_timers[0], v_timers[1]))

  global_mean_distortion = global_mean_distortion / float(repeat)
  text_file.write("%f\t%f\t%f" % (global_mean_distortion, global_min_distortion, global_max_distortion))

def RunVersion02(documents, mtx_original_distance, N, repeat, d, number_of_documents, path, do_achiloptas, do_randomproj):
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

  if do_achiloptas == True:
    print("  . Achiloptas")

    v_timers = np.zeros(shape = (2))
    global_mean_distortion = 0.0
    global_min_distortion = float('inf')
    global_max_distortion = -float('inf')

    text_file = open(path + str(N) + "_v2_achiloptas.txt", "w")
    text_file.write("%s\t%s\t%s\t%s\n" % ('case', 'gen_proj_time', 'dist_time', 'distortion'))
      
    for ith_repeat in range(repeat):
      ret_data = acl.Achlioptas(number_of_documents, documents, mtx_original_distance, d, n, use_less_memory = True)
        
      v_timers[0] += ret_data['gen_proj_time']
      v_timers[1] += ret_data['dist_time']

      max_distortion = ret_data['distortion']

      text_file.write("%d\t%f\t%f\t%f\n" % (ith_repeat + 1, ret_data['gen_proj_time'], ret_data['dist_time'], ret_data['distortion']))

      global_mean_distortion += max_distortion
      global_min_distortion = min(max_distortion, global_min_distortion)
      global_max_distortion = max(max_distortion, global_max_distortion)

    # compute results
    ReportV2Results(text_file, repeat, v_timers, global_mean_distortion, global_min_distortion, global_max_distortion)
    text_file.close()

  ##############################################################################

  if do_randomproj == True:
    print("  . Random Projections")

    v_timers = np.zeros(shape = (2))
    global_mean_distortion = 0.0
    global_min_distortion = float('inf')
    global_max_distortion = -float('inf')

    text_file = open(path + str(N) + "_v2_randomproj.txt", "w")
    text_file.write("%s\t%s\t%s\t%s\n" % ('case', 'gen_proj_time', 'dist_time', 'distortion'))
      
    for ith_repeat in range(repeat):
      ret_data = lrp.RandomProjection(number_of_documents, documents, mtx_original_distance, d, n, use_less_memory = True)
        
      v_timers[0] += ret_data['gen_proj_time']
      v_timers[1] += ret_data['dist_time']

      max_distortion = ret_data['distortion']

      text_file.write("%d\t%f\t%f\t%f\n" % (ith_repeat + 1, ret_data['gen_proj_time'], ret_data['dist_time'], ret_data['distortion']))
        
      global_mean_distortion += max_distortion
      global_min_distortion = min(max_distortion, global_min_distortion)
      global_max_distortion = max(max_distortion, global_max_distortion)

    # compute results
    ReportV2Results(text_file, repeat, v_timers, global_mean_distortion, global_min_distortion, global_max_distortion)  
    text_file.close()
      
    # 4.6
    text_file = open(path + str(N) + "_v2_JL.txt", "w")
    text_file.write("%f" % (bwmath.CalculateJLLema(d, n)))
    text_file.close()   
