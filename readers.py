# 1. Baixe o dataset Bag of Words da UCI (arquivo NyTimes). Cerca de 300k docs e vocabulario com 102650 termos
# 2. Crie uma bag of words para os 3000 primeiros documentos
# 3. Calcule a distancia entre cada par de pontos atraves da forca bruta e messa o tempo computacional deste procedimento. Armazene estes valores. Utilize dois loops para fazer isso e implemente o calculo da distancia

# TODO

# 4. Para n = 4, 16, 64, 256, 1024, 4096, 15768, repita o procedimento abaixo 30 vezes
  # Obtenha uma matriz aleatoria de n linhas e d colunas pelo m´etodo de Achiloptas e pelo metodo dado em aula, onde d e o tamanho do vocaulario.
  # Messa o tempo computacional da geracao das matrizes
  # Projete os 3000 documentos no espaco Rn atraves das matrizes geradas. Messa o tempo da projecao
  # Messa o tempo para obter todas as distancias entre os pontos projetados
  # Calcule a distors˜ao maxima em relacao aos dados originais.
  # Calcule o limite superior da distorsao previsto pelo Lema de J.L.
# 5. Escreva um relatorio descrevendo os experimentos e os resultados obtidos. Analise se os resultados obtidos estao de acordo com a teoria apresentada. Considere a media, o maximo e o mınimo dos 30 experimentos do item 4.

import time
import math
import random

# id's considered to start by 1

############ 2
DOCWORD_FILE = "../docword.nytimes.txt"
VOCAB_FILE = "vocab.nytimes.txt"

word_list = {}
index = 1
with open(VOCAB_FILE,'r+') as file_reader:
  for line in file_reader:
    word = line.replace('\n','')
    # Update List to maintain order
    word_list[index] = word
    index = index + 1

file_reader.close()

doc_reader = open(DOCWORD_FILE, 'r+')

D = int(doc_reader.readline().replace('\n',''))
D_t_work = 3000
W = int(doc_reader.readline().replace('\n',''))
NNZ = int(doc_reader.readline().replace('\n',''))

documents = dict()

for x in range(1, 3001):
  documents[x] = dict()

for x in range(NNZ):
  wordList = doc_reader.readline().replace('\n', '').split()
  doc_id = int(wordList[0])

  if doc_id > 3000:
    break

  word_id = int(wordList[1])
  count = int(wordList[2])

  documents[doc_id][word_id] = count
  
doc_reader.close()  


# print a bag of words doc
def print_bag_doc(document, vocab):
  for name, count in document.items():
     print('{0:25} --> {1:10d}'.format(vocab[name], count))
#print_bag_doc(documents[1], word_list)
############ 2

############ 3
def DocEuclidianDistance(id_x, id_y, docs, word_count):
  dict_keys = dict()
  sum_dist = 0

  start_clock_1 = time.clock()
  # words in id_x
  for id_word, x1 in docs[id_x].items():
    if dict_keys.get(id_word) == None:
      x2 = docs[id_y].get(id_word) or 0
      sum_dist = sum_dist + (x1 - x2) * (x1 - x2)
      dict_keys[id_word] = True

  # words in id_y
  for id_word, x2 in docs[id_y].items():
    if dict_keys.get(id_word) == None:
      x1 = docs[id_x].get(id_word) or 0
      sum_dist = sum_dist + (x1 - x2) * (x1 - x2)
      dict_keys[id_word] = True
  end_clock_1 = time.clock()

  # 1 for to all words (probably slower)
  # test
  #sum_dist1 = 0
  #start_clock_2 = time.clock()
  #for id_w in range(1, word_count + 1):
  #  x1 = docs[id_x].get(id_w) or 0
  #  x2 = docs[id_y].get(id_w) or 0
  #  sum_dist1 = sum_dist1 + (x1 - x2) * (x1 - x2)
  #end_clock_2 = time.clock()
  #assert(sum_dist == sum_dist1)
  # test

  return math.sqrt(sum_dist)

DistanceMatrix = [[0 for x in range(D_t_work)] for y in range(D_t_work)] 

start_clock = time.clock()

for x in range(1, D_t_work + 1):
  for y in range(x, D_t_work + 1):
    DistanceMatrix[x - 1][y - 1] = DocEuclidianDistance(x, y, documents, W)
    # TODO: remove this
    DistanceMatrix[y - 1][x - 1] = DistanceMatrix[x - 1][y - 1] 

finish_clock = time.clock()

print(finish_clock - start_clock)
############ 3

############ 4
def RandomGenGaussianValue(x, mean, deviation):
  s = deviation
  s_t = math.sqrt(2.0 * math.pi)
  expo =  math.pow((x - mean) / s, 2)
  ret_val = (1.0/s*s_t) * math.exp(-0.5 * expo)
  return ret_val

def RandomGenAchiloptasValue(x)
  ret_val = 0
  
  if x < 1/6:
    ret_val = -1
  else if x < 5/6
    ret_val = 0
  else if < 1:
    ret_val = 1
  
  return ret_val

n_cases = [4, 16, 64, 256, 1024, 4096, 15768]
for N in n_cases:
  n = N
  d = W

  # Achiloptas
  A_Matrix = [[0 for x in range(N)] for y in range(W)]
  for i in range(n):
    for j in range(d):
      A_Matrix[i][j] = RandomGenAchiloptasValue(random.random())
      A_Matrix[i][j] = A_Matrix[i][j] * math.sqrt(3/n)
      
  # Random projections with gaussian
  R_Matrix = [[0 for x in range(N)] for y in range(W)]
  deviation = math.sqrt(n)
  for i in range(n):
    for j in range(d):
      R_Matrix[i][j] = RandomGenGaussianValue(random.random(), 0, sqrt(1/n))

  # MATRIX_n_d * VETOR_d_1 = VERTO_n_1
############ 4

