import timeimport mathimport randomimport bw_readersimport bw_distanceimport bw_number_genimport bw_serializationimport matUtils# id's considered to start by 1DOCWORD_FILE = "../docword.nytimes.txt"VOCAB_FILE = "vocab.nytimes.txt"# 1 2# 1. Baixe o dataset Bag of Words da UCI (arquivo NyTimes). Cerca de 300k docs e vocabulario com 102650 termos# 2. Crie uma bag of words para os 3000 primeiros documentosword_list = bw_readers.ReadVocabulary(VOCAB_FILE)D_t_work = 3000table_docs = bw_readers.ReadDocuments(DOCWORD_FILE, D_t_work)documents = table_docs[0]D = table_docs[1]W = table_docs[2]NNZ = table_docs[3]# 3# 3. Calcule a distancia entre cada par de pontos atraves da forca bruta e messa o tempo computacional deste procedimento. Armazene estes valores. Utilize dois loops para fazer isso e implemente o calculo da distanciaDistanceMatrix = bw_serialization.LoadPickleObject('distance_matrix')if DistanceMatrix == None:  DistanceMatrix = [[0 for x in range(D_t_work)] for y in range(D_t_work)]  start_clock = time.clock()  for x in range(1, D_t_work + 1):    for y in range(x, D_t_work + 1):      DistanceMatrix[x - 1][y - 1] = bw_distance.DocEuclidianDistance(x, y, documents, W)      # TODO: remove this      DistanceMatrix[y - 1][x - 1] = DistanceMatrix[x - 1][y - 1]  finish_clock = time.clock()  bw_serialization.SavePickleObject('distance_matrix', DistanceMatrix)  print(finish_clock - start_clock)# 4# 4. Para n = 4, 16, 64, 256, 1024, 4096, 15768, repita o procedimento abaixo 30 vezesn_cases = [4, 16, 64, 256, 1024, 4096, 15768]for N in n_cases:  n = N  d = W  for cases in range(30):    # 4.1. Obtenha uma matriz aleatoria de n linhas e d colunas pelo metodo de Achiloptas e pelo metodo dado em aula, onde d e o tamanho do vocaulario.    # 4.2. Messa o tempo computacional da geracao das matrizes    # Achiloptas    achiloptas_start_clock = time.clock()    A_Matrix = [[0 for x in range(N)] for y in range(W)]    for i in range(n):      for j in range(d):        A_Matrix[i][j] = bw_number_gen.RandomGenAchiloptasValue(random.random())        A_Matrix[i][j] = A_Matrix[i][j] * math.sqrt(3/n) # multiplicar por sqrt(3/n) depois da multiplicação é melhor    achiloptas_finish_clock = time.clock()       # Random projections with gaussian    random_start_clock = time.clock()    R_Matrix = [[0 for x in range(N)] for y in range(W)]    deviation = math.sqrt(n)    for i in range(n):      for j in range(d):        R_Matrix[i][j] = bw_number_gen.RandomGenGaussianValue(random.random(), 0, sqrt(1/n))    random_finish_clock = time.clock()    # 4.3. Projete os 3000 documentos no espaco Rn atraves das matrizes geradas. Messa o tempo da projecao    # TODO    # MATRIX_n_d * VETOR_d_1 = VERTO_n_1	    achiloptas_Proj_start = time.clock()    ProjMatAch = matUtils.matrixMultiply2(DistanceMatrix,A_Matrix)    achiloptas_Proj_end = time.clock()        Random_Proj_start = time.clock()    ProjMatRN = matUtils.matrixMultiply2(DistanceMatrix,R_Matrix)    Random_Proj_end = time.clock()        # 4.4. Messa o tempo para obter todas as distancias entre os pontos projetados    #RN_DistanceMatrix = [[0 for x in range(D_t_work)] for y in range(D_t_work)]    ach_dist_start_clock = time.clock()    Ach_DistanceMatrix = matUtils.distance_matrix(ProjMatAch)    ach_dist_finish_clock = time.clock()        rn_dist_start_clock = time.clock()    RN_DistanceMatrix = matUtils.distance_matrix(ProjMatRN)    rn_dist_finish_clock = time.clock()	    # 4.5. Calcule a distors˜ao maxima em relacao aos dados originais.    distortionAch = matUtils.maxDistortion(DistanceMatrix,ProjMatAch)        distortionRN = matUtils.maxDistortion(DistanceMatrix,ProjMatRN)    	# 4.6. Calcule o limite superior da distorsao previsto pelo Lema de J.L.    JL = calculateJLLema(W,n)# 5. Escreva um relatorio descrevendo os experimentos e os resultados obtidos. Analise se os resultados obtidos estao de acordo com a teoria apresentada. Considere a media, o maximo e o mınimo dos 30 experimentos do item 4.# TODO