import numpy as np
import msvcrt as m

def CreateShingle(ngram_size, filename):
  ret_set = set()

  with open(filename, "rb") as f:
    content = f.read().decode("UTF-8")

    #Concatenate each line and replace '\n' by ' '
    content = ''.join(content).replace('\n',' ').lower()
    
    #TODO: Remove not used characters: é, ã, ê, ., ;, :, ...
    # ' to white space
    content = content.replace('ç', 'c').replace('é', 'e').replace('á', 'a')
    #content.replace("Is", "Was")

    print(content)

  #Get a slice: s[start:end], starts in 0
  assert(len(content) >= 4)

  #[' '.join(tokens[i:i+ngram_size]) for i in range(0, len(tokens) - ngram_size + 1)]
  for i in range(ngram_size, len(content)):
    ret_set.add(content[i-ngram_size:i])

  return ret_set

#with open("file.txt", "r") as ins:
#    array = []
#    for line in ins:
#        array.append(line)
