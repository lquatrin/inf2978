
import re, time, sys, os
import editdistance
import pickle
import itertools
import time
import numpy 

root = ""
path = os.path.join(root, "TRAIN_DATASET/")
from multiprocessing import Pool

NUM_PROCESSES = 8


def is_same_string(string_a, string_b, char_margin=5):
   
    if not string_a or len(string_a) == 0:
        raise ValueError('Invalid input string.')
    if not string_b or len(string_b) == 0:
        raise ValueError('Invalid input string.')
    if isinstance(char_margin, int):
        if len(string_a) < char_margin or len(string_b) < char_margin:
            raise ValueError('Input strings shorter than tolerance margin.')

    d = editdistance.eval(string_a, string_b)

    if isinstance(char_margin, float):
        shortest_str_len = len(string_a) if len(string_a) < len(string_b) else len(string_b)
        return (False if float(d) / float(shortest_str_len) > char_margin else True), d
    else:
        return d < char_margin, d



def is_same_string_from_repo(website1_name, website2_name, string1, string2):
    
    vagalume_website_name = 'vagalume'

    if website1_name != vagalume_website_name or website2_name != vagalume_website_name:
        return False

    if string1 == string2 or string1 == string2 + " traducao" or string2 == string1 + " traducao":
        return True
        
    return False


def check_match(key1, key2):
# 'key[12]' is a string with the following:
# 'website_name|artist_name|lyrics_name'

    key1_split = key1.split('|')
    key2_split = key2.split('|')

    if not len(key1_split) == 3:
        print('Original key:{}\nSplit key:{}'.format(key1, key1_split))
        assert False
    assert len(key2_split) == 3

    try:
        # Checks whether artist name is the same
        is_same_artist_name, _ = is_same_string(key1_split[1], key2_split[1], 1)
        if not is_same_artist_name:
            return False

        is_same_lyrics_from_repo = is_same_string_from_repo(key1_split[0],
                                                                    key2_split[0],
                                                                    key1_split[2],
                                                                    key2_split[2])

        # Checks whether lyrics name is the same
        is_same_lyrics_name, _ = is_same_string(key1_split[2], key2_split[2], 1)
        if not is_same_lyrics_name and not is_same_lyrics_from_repo:
            return False

    except Exception:
        print("Error comparing '%s' and '%s'. Returning False for matching." % (key1, key2))
        return False

    return True



def combinations_test(tuples_lists):
    match_count = 0
    match_set = set()
    for key1, key2 in tuples_lists:
        if (key1, key2) not in match_set:
            is_match = check_match(key1, key2)
            if is_match:
                match_set.add((key1, key2))
                match_set.add((key2, key1))
                match_count += 1

    return match_count, match_set



def generate_matches(data):
    
  start = time.time()
  print(" Generating Combinations")
  tuples = set()

  for key1, key2 in itertools.combinations(data, 2):
    tuples.add((key1,key2))
   
    # combinations('ABCD', 2) --> AB AC AD BC BD CD
  tuple_size = int(len(tuples) / NUM_PROCESSES)
  dict_chunks = [tuples[i:i + tuple_size] for i in range(0, len(tuples), tuple_size)]
  print('Split the data into {} chunks of {} elements.'.format(NUM_PROCESSES, tuple_size))
  print("------------ generating pickle matches ---------------")
  pool = Pool(processes=NUM_PROCESSES)
  results = pool.map(combinations_test, dict_chunks)
  print('DONE!')

  count_true = sum(r[0] for r in results)
  matches = set.union(*(s[1] for s in results))
  
  
  now = time.time() - start
  print("finished! minutes: ",now/60)
  print('Number of matches found = {}'.format(count_true)) 
  return count_true,matches

def generate_ground_truth():
  
  pickle_ground_truth_output = "ground_truth2_8.p"
  tuples = []
  n_count = 0;
  for r,d,f in os.walk(path):
    for file in f:
      pathf = r.replace('\\','/')
      filename = pathf + '/' + file
      data = r.split("/")
      key = data[0] + "|" + data[1] + "|" + file
      #with open(filename, "rb") as fr:
      #  content = fr.read().decode("UTF-8")
      #t = (key)
      tuples.append(key)
      n_count = n_count + 1

  count_true,matches = generate_matches(tuples)

  #count_true, matches = generate_matches(tuples)
  
  with open(pickle_ground_truth_output, "wb") as file_out:
        pickle.dump((count_true, matches), file_out)
  print("------------------------------------------------------")
  
  
generate_ground_truth()
    
    
