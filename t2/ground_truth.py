
import re, time, sys, os
import editdistance

root = ""
path = os.path.join(root, "TRAIN_DATASET/")



def is_same_string(string_a, string_b, char_margin=5):
    """
    Given two strings, this function returns True if they are identical within
    a certain tolerance. This functions uses the edit distance to compare the
    inputs.
    Arguments:
    string_a -- The first string
    string_b -- The second string
    char_margin -- The number or percentage of characters to use as margin. If
    this parameter is float, it will be interpreted as a percentage of characters
    of the smallest string. If is of type int, then it will be interpreted as the
    number of characters of tolerance to declare that the two strings are the same.
    Returns:
    True if string_a matches string_b with at most "char_margin" different
    characters. Also returns the distance between the two strings.
    """
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
    vagalume_website_name = 'cifra-club'

    if website1_name != vagalume_website_name or website2_name != vagalume_website_name:
        return False


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


def generate_matches(lyrics_tuple_list):
    '''
    Given a list of tuples in the form ('website|artist|songname', 'lyrics'),
    this function searches through them and returns a dictionary containing the
    matches and a counter of how many matches occured.
    Arguments:
    lyrics_tuple_list -- The list of tuples in the form:
    [('website|artist|songname', 'lyrics'), ...)
    Returns:
    The number of matches and a set containing tuples of songs that matched, e.g.
    set((key1, key2), (key2, key1), (key4, key3), (key3, key4), ...)
    '''
    if not lyrics_tuple_list or len(lyrics_tuple_list) == 0:
        raise ValueError('Invalid lyrics dictionary')

    match_count = 0
    match_set = set()

    for key1, key2 in itertools.combinations(lyrics_tuple_list, 2):
        if (key1, key2) not in match_set:
            is_match = check_match(key1, key2)
            if is_match:
                match_set.add((key1, key2))
                match_set.add((key2, key1))
                match_count += 1

    return match_count, match_set

def generate_ground_truth():
  tuples = []
  n_count = 0;
  for r,d,f in os.walk(path):
      for file in f:
        pathf = r.replace('\\','/')
        filename = pathf + '/' + file
        data = r.split("\\")
        key = data[0] + "|" + data[1] + "|" + file
        with open(filename, "rb") as fr:
          content = fr.read().decode("UTF-8")
        t = (key,content)
        print("-------------------------------------")
        tuples.append(t)
        n_count = n_count + 1
      # Remove - just for testing 
      if n_count > 100:
        print(tuples[0])
        break
  #TO DO - SAVE OCURRENCES
  #count_true, matches = generate_count_true_and_matches(tuples)
  print("-------------------------------------")
  
  
generate_ground_truth()
    
    
