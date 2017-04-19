import numpy as npimport bwnumbergenimport randomdef ProjectDocuments(documents, proj_matrix, r, c):  r_mat = np.zeros(shape = (r, c))  # ProjMatrix(n.d) * Documents(d.D) = ProjectedDocuments(n.D)  #for each doc  for doc_id in range(c):    #for each word    for word_id, count_w in documents[doc_id].items():      #for each dimension in projected space      for id_v in range(r):        r_mat[id_v, doc_id] = r_mat[id_v, doc_id] + (count_w * proj_matrix[id_v, word_id])  return r_matdef GenerateAndProjectDocumentsAchiloptas(documents, r, c, d):  r_mat = np.zeros(shape = (r, c))  # ProjMatrix(n.d) * Documents(d.D) = ProjectedDocuments(n.D)  proj_line = np.zeros(shape = (d))  #for each dimension in projected space  for id_v in range(r):    print(id_v)    for j in range(d):        proj_line[j] = bwnumbergen.RandomGenAchiloptasValue(random.random())    #for each doc    for doc_id in range(c):      #for each word      for word_id, count_w in documents[doc_id].items():        r_mat[id_v, doc_id] = r_mat[id_v, doc_id] + (count_w * proj_line[word_id])  return r_matdef GenerateAndProjectDocumentsRandomGeneration(documents, r, c, d):  r_mat = np.zeros(shape = (r, c))  s_dev = math.sqrt(1/r)    # ProjMatrix(n.d) * Documents(d.D) = ProjectedDocuments(n.D)  proj_line = np.zeros(shape = (d))  #for each dimension in projected space  for id_v in range(r):    print(id_v)    for j in range(d):      proj_line[j] = bwnumbergen.RandomGenGaussianValue(random.random(), 0, s_dev)        #for each doc    for doc_id in range(c):      #for each word      for word_id, count_w in documents[doc_id].items():        r_mat[id_v, doc_id] = r_mat[id_v, doc_id] + (count_w * proj_line[word_id])  return r_mat