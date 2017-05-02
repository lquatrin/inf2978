# Euclidean distanceimport mathimport numpy as npimport timeimport bwserializationfrom scipy.spatial.distance import pdistdef EuclidianSquaredDistance(id_x, id_y, docs, word_count):  dict_keys = dict()  sum_dist = 0.0  # words in id_x  for id_word, x1 in docs[id_x].items():    if dict_keys.get(id_word) == None:      x2 = docs[id_y].get(id_word) or 0.0      sum_dist = sum_dist + (x1 - x2) * (x1 - x2)      dict_keys[id_word] = True  # words in id_y  for id_word, x2 in docs[id_y].items():    if dict_keys.get(id_word) == None:      x1 = docs[id_x].get(id_word) or 0.0      sum_dist = sum_dist + (x1 - x2) * (x1 - x2)      dict_keys[id_word] = True  return sum_dist  # 3. Calcule a distancia entre cada par de pontos atraves da forca bruta e messa#    o tempo computacional deste procedimento. Armazene estes valores. Utilize#    dois loops para fazer isso e implemente o calculo da distancia.def GenerateOriginalDistanceMatrix(n_documents, n_words, documents):  mtx_original_distance = bwserialization.LoadPickleObject('distance_matrix_np')  if mtx_original_distance is None:    time_file = open("distance_time.txt", "w")        print("Generating Distance Matrix")    mtx_original_distance = np.zeros(shape = (n_documents, n_documents))    start_clock = time.clock()    if isinstance(documents, dict):      for x in range(0, n_documents):        mtx_original_distance[x][x] = 0.0        for y in range(x + 1, n_documents):          mtx_original_distance[x][y] = EuclidianSquaredDistance(x, y, documents, n_words)          mtx_original_distance[y][x] = mtx_original_distance[x][y]    elif isinstance(documents, np.ndarray):      print("ndarray")      mtx_original_distance = pdist(documents.T, 'sqeuclidean')          finish_clock = time.clock()    bwserialization.SavePickleObject('distance_matrix_np', mtx_original_distance)    print("Time Elapsed:", finish_clock - start_clock)    time_file.write("Time %f\n", (finish_clock - start_clock))    time_file.close()      return mtx_original_distance# proj_docs numpy [dimension, documents]def DoEuclidianDistanceProjDocs(mtx_data, transpose = True):  s_clock = time.clock()  if transpose:    projected_distances = pdist(mtx_data.T, 'sqeuclidean')  else:    projected_distances = pdist(mtx_data, 'sqeuclidean')  f_clock = time.clock()  return projected_distances, (f_clock - s_clock)def OLD_DoEuclidianDistanceProjDocs(proj_docs):  s_clock = time.clock()    dist_p = np.zeros(shape = (proj_docs.shape[1], proj_docs.shape[1]))    dim = proj_docs.shape[0]  docs = proj_docs.shape[1]  for x in range(0, docs):    dist_p[x][x] = 0.0    for y in range(x + 1, docs):      sum_dist = 0.0      for d in range(dim):        diff = (proj_docs[d][y] - proj_docs[d][x])        sum_dist = sum_dist + (diff*diff)       dist_p[x][y] = dist_p[y][x] = sum_dist  f_clock = time.clock()    return dist_p, (f_clock - s_clock)