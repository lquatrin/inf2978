
import re, time, sys, os
import editdistance
import pickle
import itertools
import stextutils

root = ""
path = os.path.join(root, "TRAIN_DATASET/")
from multiprocessing import Pool

NUM_PROCESSES = 1


def is_same_string(string_a, string_b, char_margin=3):
   
    if not string_a or len(string_a) == 0:
        raise ValueError('Invalid input string.')
    if not string_b or len(string_b) == 0:
        raise ValueError('Invalid input string.')
    #if isinstance(char_margin, int):
    #    if len(string_a) < char_margin or len(string_b) < char_margin:
    #        raise ValueError('Input strings shorter than tolerance margin.')

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

    key1_split = key1[0].split('|')
    key2_split = key2[0].split('|')
	
    if not len(key1_split) == 3:
        print('Original key:{}\nSplit key:{}'.format(key1, key1_split))
        assert False
    assert len(key2_split) == 3

    try:
        # Checks whether artist name is the same
       is_same_artist_name, _ = is_same_string(key1_split[1], key2_split[1], 3)
       is_same_lyrics_from_repo = is_same_string_from_repo(key1_split[0],
                                                                   key2_split[0],
                                                                   key1_split[2],
                                                                   key2_split[2])

       # Checks whether lyrics name is the same
       is_same_lyrics_name, _ = is_same_string(key1_split[2], key2_split[2], 3)
       if (not is_same_artist_name or not is_same_lyrics_name or not is_same_lyrics_from_repo):
            #Verificar se a letra é igual
            split_content_1 = key1[1].split()
            split_content_2 = key2[1].split()
			
            if (len(split_content_1) == 1 and str.lower(split_content_1[0]) == str.lower('Instrumental')) or (len(split_content_2) == 1 and str.lower(split_content_2[0]) == str.lower('Instrumental')):
              return False

            same_lyrics, _ = is_same_string(key1[1], key2[1], 50)
            if same_lyrics :
               return True     
            else:
               return False

    except Exception:
        #print("Error comparing '%s' and '%s'. Returning False for matching." % (key1, key2))
        return False

    return True


def generate_matches(lyrics_tuple_list):
    
    if not lyrics_tuple_list or len(lyrics_tuple_list) == 0:
        raise ValueError('Invalid lyrics dictionary')

    match_count = 0
    match_set = set()

    # combinations('ABCD', 2) --> AB AC AD BC BD CD
    
    for key1, key2 in itertools.combinations(lyrics_tuple_list, 2):
        if (key1, key2) not in match_set:
            is_match = check_match(key1, key2)
            if is_match:
                match_set.add((key1[0], key2[0]))
                match_set.add((key2[0], key1[0]))
                match_count += 1
        

    return match_count, match_set

def generate_ground_truth():
 
  pickle_ground_truth_output = "ground_truth_seq_total.p"
  tuples = []
  n_count = 0;
  for r,d,f in os.walk(path):
      for file in f:
        pathf = r.replace('\\','/')
        filename = pathf + '/' + file
        data = r.split("/")
        key = data[1] + "|" + data[2] + "|" + file
        
        #Para Windows
        #key = data[1].replace('\\', '|') + "|" + file
        
        with open(filename, "rb") as fr:
          content = fr.read().decode("UTF-8")
		  #Remover caso não seja testada a letra
          content = stextutils.FormatContent(content)
		  
        t = (key,content)
        tuples.append(t)
        n_count = n_count + 1
  
  start = time.time()
  print(' Generating Combinations with {} '.format(NUM_PROCESSES))
  tuple_size = int(len(tuples) / NUM_PROCESSES)
  dict_chunks = [tuples[i:i + tuple_size] for i in range(0, len(tuples), tuple_size)]
  print('Split the data into {} chunks of {} elements.'.format(NUM_PROCESSES, tuple_size))
  print("------------ generating pickle matches ---------------")
  pool = Pool(processes=NUM_PROCESSES)
  results = pool.map(generate_matches, dict_chunks)
  print('DONE!')

  count_true = sum(r[0] for r in results)
  matches = set.union(*(s[1] for s in results))
  
  print('Number of matches found = {}'.format(count_true))
  
  now = time.time() - start
  print("finished! minutes: ",now/60)
  #count_true, matches = generate_matches(tuples)
  
  with open(pickle_ground_truth_output, "wb") as file_out:
        pickle.dump((count_true, matches), file_out)
  print("------------------------------------------------------")
 
def EvaluateNumberOfInstrumentalLyrics (path_dataset):
  n_count = 0;
  
  for r,d,f in os.walk(path_dataset):
    for file in f:
      pathf = r.replace('\\','/')
      filename = pathf + '/' + file
      data = r.split("/")
      key = data[1].replace('\\', '|') + "|" + file
      
      with open(filename, "rb") as fr:
        content = fr.read().decode("UTF-8")
        content = stextutils.FormatContent(content)
      
        split_cont = content.split()
        if len(split_cont) == 1 and str.lower(split_cont[0]) == str.lower('Instrumental'):
          n_count = n_count + 1
  return n_count
 
#verificar se é instrumental


#root = "F:/TRAIN_DATASET/"
#f1 = root + "vagalume/aaron-carter/forever-for-you-love"
#c1 = None
#with open(f1, "rb") as fr:
#  c1 = fr.read().decode("UTF-8")
#  c1 = stextutils.FormatContent(c1)
#
#f2 = root + "vagalume/aaron-carter/ill-wait"
#c2 = None
#with open(f2, "rb") as fr:
#  c2 = fr.read().decode("UTF-8")
#  c2 = stextutils.FormatContent(c2)
# 
#print(is_same_string(c1, c2, 47) == True)
#s, _ = is_same_string(c1, c2, 47)
#print(s == True)

#print(EvaluateNumberOfInstrumentalLyrics(path))
generate_ground_truth()
    
    
