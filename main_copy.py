import timeimport mathimport randomimport bwreadersimport bwdistanceimport bwnumbergenimport bwserializationimport bwprojectionimport bwmathimport numpy as npimport osimport gcDOCWORD_FILE = "../docword.nytimes.txt"VOCAB_FILE = "vocab.nytimes.txt"# 1 2# 1. Baixe o dataset Bag of Words da UCI (arquivo NyTimes). Cerca de 300k docs e vocabulario com 102650 termos# 2. Crie uma bag of words para os 3000 primeiros documentosword_list = bwreaders.ReadVocabulary(VOCAB_FILE)D_t_work = 3000table_docs = bwreaders.ReadDocuments(DOCWORD_FILE, D_t_work)#documents =  bwreaders.read_document_corpus(filepath= './docword.nytimes.txt_preprocessed.txt',#                                              num_docs=3000,#                                              num_words_in_vocabulary=102650)documents = table_docs[0]D = table_docs[1]W = table_docs[2]NNZ = table_docs[3]# 3# 3. Calcule a distancia entre cada par de pontos atraves da forca bruta e messa o tempo computacional deste procedimento. Armazene estes valores. Utilize dois loops para fazer isso e implemente o calculo da distanciamtx_original_distance = bwserialization.LoadPickleObject('distance_matrix')if mtx_original_distance == None:  print("Generating Distance Matrix")  mtx_original_distance = np.zeros(shape = (D_t_work, D_t_work))  start_clock = time.clock()  for x in range(0, D_t_work):    mtx_original_distance[x][x] = 0.0    for y in range(x + 1, D_t_work):      mtx_original_distance[x][y] = bwdistance.DocEuclidianDistance(x, y, documents, W)      mtx_original_distance[y][x] = mtx_original_distance[x][y]  finish_clock = time.clock()  bwserialization.SavePickleObject('distance_matrix', mtx_original_distance)  print("Time Elapsed:", finish_clock - start_clock)# 4# 4. Para n = 4, 16, 64, 256, 1024, 4096, 15768, repita o procedimento abaixo 30 vezesrepeat = 30n_cases = [ 4, 16, 64, 256, 1024, 4096, 15768 ]# 4.1. Obtenha uma matriz aleatoria de n linhas e d colunas pelo metodo de Achiloptas e pelo metodo dado em aula, onde d e o tamanho do vocaulario.# 4.2. Messa o tempo computacional da geracao das matrizes# 4.3. Projete os 3000 documentos no espaco Rn atraves das matrizes geradas. Messa o tempo da projecao# TODO# MATRIX_n_d * VETOR_d_1 = VERTO_n_1# 4.4. Messa o tempo para obter todas as distancias entre os pontos projetados# 4.5. Calcule a distors˜ao maxima em relacao aos dados originais.# Achiloptas# 4.6. Calcule o limite superior da distorsao previsto pelo Lema de J.L.##################################################################### Versão 1:# - Geração da matriz # - Projeção (maior consumo de memória)#####################################################################matrizes com os tempos:# . número de casos (7)# . número de repetições (30)# . número de operações x2#   1. matriz achiloptas#   2. projeção achiloptas#   3. tempo para obter novas distâncias#########################################   4. matriz random proj#   5. projeção random proj#   6. tempo para obter novas distânciasv1_timers = np.zeros(shape = (7, repeat, (6 * 2)))v1_distortions = np.zeros(shape = (7, repeat, 2))v1_JL = np.zeros(shape = (7))ith_case = 0for N in n_cases:  n = N  d = W  # se N for maior que 1024  if N > 1024:    break  print("Case: ", N)  for ith_repeat in range(repeat):    projected_documents = None    Proj_DistanceMatrix = None    projection_matrix = None    # Achiloptas    ##################################################################################    print(N, ith_repeat, "Achiloptas")    # 4.1 4.2    v1_timers[ith_case][ith_repeat][0] = time.clock()    projection_matrix = bwnumbergen.GenerateRandomAchiloptasMatrix(n,d)    v1_timers[ith_case][ith_repeat][1] = time.clock()    # 4.3    v1_timers[ith_case][ith_repeat][2] = time.clock()    projected_documents = bwprojection.ProjectDocuments(documents, projection_matrix, n, D_t_work)    projected_documents = projected_documents * math.sqrt(3/n)    v1_timers[ith_case][ith_repeat][3] = time.clock()    # 4.4    v1_timers[ith_case][ith_repeat][4] = time.clock()    Proj_DistanceMatrix = bwdistance.DoEuclidianDistanceProjDocs(projected_documents)    v1_timers[ith_case][ith_repeat][5] = time.clock()    # 4.5    v1_distortions[ith_case][ith_repeat][0] = bwmath.MaxDistortion(mtx_original_distance, Proj_DistanceMatrix)    print("  ", v1_distortions[ith_case][ith_repeat][0])    ##################################################################################        projected_documents = None    Proj_DistanceMatrix = None    projection_matrix = None    # Random projections with gaussian    ##################################################################################    print(N, ith_repeat, "Random Projection")    # 4.1 4.2    v1_timers[ith_case][ith_repeat][6] = time.clock()    projection_matrix = bwnumbergen.GenerateRandomGaussianMatrix(n,d)    v1_timers[ith_case][ith_repeat][7] = time.clock()    # 4.3    v1_timers[ith_case][ith_repeat][8] = time.clock()    projected_documents = bwprojection.ProjectDocuments(documents, projection_matrix, n, D_t_work)    v1_timers[ith_case][ith_repeat][9] = time.clock()    # 4.4    v1_timers[ith_case][ith_repeat][10] = time.clock()    Proj_DistanceMatrix = bwdistance.DoEuclidianDistanceProjDocs(projected_documents)    v1_timers[ith_case][ith_repeat][11] = time.clock()        # 4.5    v1_distortions[ith_case][ith_repeat][1] = bwmath.MaxDistortion(mtx_original_distance, Proj_DistanceMatrix)    print("  ", v1_distortions[ith_case][ith_repeat][1])    ##################################################################################  # 4.6  v1_JL[ith_case] = bwmath.CalculateJLLema(d, n)  ith_case = ith_case + 1bwserialization.SavePickleObject('v1_JL', v1_JL)##################################################################### Versão 2:# - Geração e projeção ao mesmo tempo (menor consumo de memória)#####################################################################matrizes com os tempos:# . número de casos (7)# . número de repetições (30)# . número de operações x2#   1. matriz e projeção achiloptas#   2. tempo para obter novas distâncias#########################################   3. matriz e projeção random proj#   4. tempo para obter novas distânciasv2_timers = np.zeros(shape = (7, repeat, (4 * 2)))v2_distortions = np.zeros(shape = (7, repeat, 2))v2_JL = np.zeros(shape = (7))ith_case = 0for N in n_cases:  n = N  d = W  print("Case: ", N)  for ith_repeat in range(repeat):    projected_documents = None    Proj_DistanceMatrix = None    # Achiloptas    ##################################################################################    print(N, ith_repeat, "Achiloptas")    # 4.1 4.2 4.3    v2_timers[ith_case][ith_repeat][0] = time.clock()    projected_documents = bwprojection.GenerateAndProjectDocumentsAchiloptas(documents, n, D_t_work, d)    projected_documents = projected_documents * math.sqrt(3/n)    v2_timers[ith_case][ith_repeat][1] = time.clock()    # 4.4    v2_timers[ith_case][ith_repeat][2] = time.clock()    Proj_DistanceMatrix = bwdistance.DoEuclidianDistanceProjDocs(projected_documents)    v2_timers[ith_case][ith_repeat][3] = time.clock()    # 4.5    v2_distortions[ith_case][ith_repeat][0] = bwmath.MaxDistortion(mtx_original_distance, Proj_DistanceMatrix)    ##################################################################################        projected_documents = None    Proj_DistanceMatrix = None    # Random projections with gaussian    ##################################################################################    print(N, ith_repeat, "Random Projection")    # 4.1 4.2 4.3    v2_timers[ith_case][ith_repeat][4] = time.clock()    projected_documents = bwprojection.GenerateAndProjectDocumentsRandomGeneration(documents, n, D_t_work, d)    v2_timers[ith_case][ith_repeat][5] = time.clock()    # 4.4    v2_timers[ith_case][ith_repeat][6] = time.clock()    Proj_DistanceMatrix = bwdistance.DoEuclidianDistanceProjDocs(projected_documents)    v2_timers[ith_case][ith_repeat][7] = time.clock()        # 4.5    v2_distortions[ith_case][ith_repeat][1] = bwmath.MaxDistortion(mtx_original_distance, Proj_DistanceMatrix)    ##################################################################################  # 4.6  v2_JL[ith_case] = bwmath.CalculateJLLema(d, n)  ith_case = ith_case + 1bwserialization.SavePickleObject('v2_JL', v2_JL)