import itertools
import sys
import pickle
from multiprocessing import Process, Queue


import re, time, sys, os


root = ""
path = os.path.join(root, "TRAIN_DATASET/")


NUM_PROCS = 32

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



def is_same_string_from_vagalume(website1_name, website2_name, string1, string2):
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

    assert len(key1_split) == 3
    assert len(key2_split) == 3

    try:
        # Checks whether artist name is the same
        is_same_artist_name, _ = is_same_string(key1_split[1], key2_split[1], 1)
        if not is_same_artist_name:
            return False

        is_same_lyrics_from_vagalume = is_same_string_from_vagalume(key1_split[0],
                                                                    key2_split[0],
                                                                    key1_split[2],
                                                                    key2_split[2])

        # Checks whether lyrics name is the same
        is_same_lyrics_name, _ = is_same_string(key1_split[2], key2_split[2], 1)
        if not is_same_lyrics_name and not is_same_lyrics_from_vagalume:
            return False

    except:
        print("Error comparing '%s' and '%s'. Returning False for matching." % (key1, key2))
        return False

    return True

def divide_work(l, num_pieces):
    size_of_each_chunk = float(len(l))/float(num_pieces)
    size_done = 0.0
    last_done = 0
    list_of_chunks = []
    for _ in range(num_pieces):
        size_done += size_of_each_chunk
        chunk = l[last_done:int(size_done)]
        list_of_chunks.append(chunk)
        last_done = int(size_done)
    if last_done != len(l):
        list_of_chunks[-1].append(l[-1])
    return list_of_chunks



def save_if_match(list_of_pairs_of_dict_lyrics_keys, out_queue):
        matches_set = set()
        for dict_lyrics_key1, dict_lyrics_key2 in list_of_pairs_of_dict_lyrics_keys:
            if (dict_lyrics_key1, dict_lyrics_key2) not in matches_set:
                is_a_match = check_match(dict_lyrics_key1,
                                         dict_lyrics_key2)
                if is_a_match:
                    matches_set.add((dict_lyrics_key1, dict_lyrics_key2))
                    matches_set.add((dict_lyrics_key2, dict_lyrics_key1))
                    count_true += 1
        out_queue.put((count_true, matches_set))



def solve(list_of_comparisons):
        jobs = divide_work(list_of_comparisons, NUM_PROCS)
        process_list = []
        result_queue = Queue()
        print("Starting 32 processes")
        for job in jobs:
            process_list.append(Process(target=save_if_match, args=(job, result_queue)))
            process_list[-1].start()
        for process in process_list:
            process.join()
        print("Processes done!")
        count_true_total = 0
        matches_set_total = set()
        while not result_queue.empty():
            curr_count, curr_matches = result_queue.get()
            count_true_total += curr_count
            matches_set_total.union(curr_matches)
        return count_true_total, matches_set_total



def generate_ground_thuth():
    
  tuples = []
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
      #n_count = n_count + 1
    
  middle = int(len(tuples)/2)

        # First half only
  print("Starting part 1 (out of 3)")
  list_of_comparisons = list(itertools.combinations(tuples[:middle], 2))
  curr_count_true, curr_matches_set = solve(list_of_comparisons)
  count_true_total = curr_count_true
  matches_set_total = curr_matches_set

        # Mixed halfs
  print("Starting part 2 (out of 3)")
  list_of_comparisons = list(itertools.product(tuples[:middle], tuples[middle:]))
  curr_count_true, curr_matches_set = solve(list_of_comparisons)
  count_true_total += curr_count_true
  matches_set_total.union(curr_matches_set)

        # Second half only
  print("Starting part 3 (out of 3)")
  list_of_comparisons = list(itertools.combinations(tuples[middle:], 2))
  curr_count_true, curr_matches_set = solve(list_of_comparisons)
  count_true_total += curr_count_true
  matches_set_total.union(curr_matches_set)

    
  pickle_ground_truth_output = "ground_truth3.p"    
  with open(pickle_ground_truth_output, "wb") as file_out:
    pickle.dump((count_true_total, matches_set_total), file_out)
  print("------------------------------------------------------")
  

generate_ground_thuth()