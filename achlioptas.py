import time
import math

import bwdistance
import bwnumbergen

import bwprojection
import bwmath

import numpy as np

# Achlioptas
# . Generate than project
def AchlioptasV1 (data_size, origin_data, origin_distance_matrix, origin_dimension, projected_dimension):
  projection_matrix = None
  projected_documents = None
  projected_distance_matrix = None
        
  # 4.1 4.2
  projection_matrix, mtx_gen_time = bwnumbergen.GenerateRandomAchiloptasMatrix(projected_dimension, origin_dimension)

  # 4.3
  s_clock = time.clock()
  projected_documents = bwprojection.ProjectDocuments(origin_data, projection_matrix, projected_dimension, data_size)
  projected_documents = projected_documents * math.sqrt(3.0/float(projected_dimension))
  f_clock = time.clock()
  data_proj_time = (f_clock - s_clock)

  # 4.4
  projected_distance_matrix, mtx_proj_dist_time = bwdistance.DoEuclidianDistanceProjDocs(projected_documents)
          
  # 4.5
  max_distortion = bwmath.MaxDistortion(origin_distance_matrix, projected_distance_matrix)

  return { "gen_time" : mtx_gen_time, "proj_time" : data_proj_time, "dist_time" : mtx_proj_dist_time, "distortion" : max_distortion, "proj_data" : projected_documents }

# Achlioptas
# . Generate and project simultaneously
# . Use less memory
def AchlioptasV2 (data_size, origin_data, origin_distance_matrix, origin_dimension, projected_dimension):
  projected_documents = None
  projected_distance_matrix = None
        
  # 4.1 4.2 4.3
  s_clock = time.clock()
  projected_documents = bwprojection.GenerateAndProjectDocumentsAchiloptas(origin_data, projected_dimension, data_size, origin_dimension)
  projected_documents = projected_documents * math.sqrt(3.0/float(projected_dimension))
  f_clock = time.clock()
  data_gen_proj_time = (f_clock - s_clock)

  # 4.4
  projected_distance_matrix, mtx_proj_dist_time = bwdistance.DoEuclidianDistanceProjDocs(projected_documents)
        
  # 4.5
  max_distortion = bwmath.MaxDistortion(origin_distance_matrix, projected_distance_matrix)

  return { "gen_proj_time" : data_gen_proj_time, "dist_time" : mtx_proj_dist_time, "distortion" : max_distortion, "proj_data" : projected_documents }
  
# Random Projection
def Achlioptas (data_size, origin_data, origin_distance_matrix, origin_dimension, projected_dimension, use_less_memory = False):
  if use_less_memory:
    return AchlioptasV2(data_size, origin_data, origin_distance_matrix, origin_dimension, projected_dimension)
  else:
    return AchlioptasV1(data_size, origin_data, origin_distance_matrix, origin_dimension, projected_dimension)
