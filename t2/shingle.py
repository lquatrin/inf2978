import numpy as np
import msvcrt as m

def CreateShingle(filename):
  ret_set = set()
  
  print(filename)
  with open(filename, "rb") as f:
    content = f.read().decode("ascii")

    #Concatenate each line and replace '\n' by ' '
    content = ''.join(content).replace('\n',' ').lower()
    
    #TODO: Remove not used characters: é, ã, ê, ., ;, :, ...
    # ' to white space
    content.replace('ç', 'c')
    #content.replace("Is", "Was")

    print(content)

  #Get a slice: s[start:end], starts in 0
  assert(len(content) >= 4)
  for i in range(4, len(content)):
    ret_set.add(content[i-4:i])

  return ret_set

#with open("file.txt", "r") as ins:
#    array = []
#    for line in ins:
#        array.append(line)
