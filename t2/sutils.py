# This Python file uses the following encoding: utf-8

import numpy as np
import itertools
import pickle
from datasketch import MinHash, MinHashLSH

def get_possible_duplicates(lsh_index):
  
  if not lsh_index:
    raise ValueError('Invalid LSH index.')

  possible_duplicates = []
  for bucket in lsh_index.hashtables:
    for elem in bucket.values():
      if len(elem) > 1:
        possible_duplicates.append(elem)

  return possible_duplicates



def keypair(lsh_index_list):
    
  if not lsh_index_list or len(lsh_index_list) == 0:
    raise ValueError('Invalid LSH index.')

  key_set = set()
  for sublist in lsh_index_list:
    key_set |= set(itertools.combinations(sublist, 2))
  
  return key_set



# Get the precision and recall
def evalutation(lsh):

   
  

  gt = set()
  not_founded = []


  with open('ground_truth_4.p', 'rb') as test_gt_in:
    gt = pickle.load(test_gt_in)
  
  lsh_key_dup = keypair(get_possible_duplicates(lsh))
  print(len(lsh_key_dup))
  num_matches_lsh = len(lsh_key_dup)
  num_actual_matches = 0
  match_set = gt[1]

  #print(lsh_key_dup)
  for key_pair in lsh_key_dup:
    #print(key_pair)
    if key_pair in match_set:
        num_actual_matches += 1
    if key_pair[::-1] in match_set:
       num_actual_matches += 1
    if not key_pair in match_set and not key_pair[::-1] in match_set:
       input(key_pair)
       not_founded.append(key_pair)

  
  precision = (num_actual_matches // 2) / num_matches_lsh
  recall = (num_actual_matches // 2) / gt[0]
  
  
  with open('not_founded.p', "wb") as file_out:
        pickle.dump(not_founded, file_out)
  print("------------------------------------------------------")
  

  return precision,recall


#links
#https://docs.python.org/release/2.7.2/library/multiprocessing.html
#http://scipy-cookbook.readthedocs.io/items/ParallelProgramming.html
#http://sebastianraschka.com/Articles/2014_multiprocessing.html
#http://www.parallelpython.com/
#https://blog.dominodatalab.com/simple-parallelization/
#http://dispy.sourceforge.net/
