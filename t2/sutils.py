# This Python file uses the following encoding: utf-8

import re
import numpy as np
import itertools
import pickle
from datasketch import MinHash, MinHashLSH


def FormatContent(content, manual_mode = False):
  
  #Concatenate each line and replace '\n' by ' '
  content = ''.join(content).replace('\n',' ').lower()


  # c
  content = re.sub("[ç]"   , 'c', content)  
  # â á à ã
  content = re.sub("[âáàã]", 'a', content)
  # ê é è
  content = re.sub("[êéè]" , 'e', content)
  # î í ì
  content = re.sub("[îíì]" , 'i', content)
  # ô ó ò õ
  content = re.sub("[ôóòõ]", 'o', content)
  # û ú ù
  content = re.sub("[ûúù]" , 'u', content)
  
  # ? ! ' . - " … : ; , [ ] ( ) { }
  content = re.sub("[\\?\\!\\'\\.\\-\"…:;,\\[\\]\\(\\)\\{\\}]", ' ', content)
  
  # 1 2 3 4 5 6 7 8 9 0
  #content = re.sub("[1234567890]", ' ', content)
  content = re.sub("[1]", '', content)
  content = re.sub("[2]", '', content)
  content = re.sub("[3]", '', content)
  content = re.sub("[4]", '', content)
  content = re.sub("[5]", '', content)
  content = re.sub("[6]", '', content)
  content = re.sub("[7]", '', content)
  content = re.sub("[8]", '', content)
  content = re.sub("[9]", '', content)
  content = re.sub("[0]", '', content)
   
  content = re.sub(' *', ' ', content)

  #trocar ' ' por '`' para facilitar o hash depois
  if manual_mode == True:
    content = re.sub(' ', chr(96), content)

  return content

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
