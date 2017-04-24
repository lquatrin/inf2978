import timeimport mathimport randomimport bwreadersimport bwdistanceimport bwnumbergenimport bwserializationimport bwprojectionimport bwmathimport numpy as npimport osimport gcimport bwrunsoutput_path = 'E:/Dropbox/data/'DOCWORD_FILE = "../docword.nytimes.txt"VOCAB_FILE = "vocab.nytimes.txt"# 1 2# 1. Baixe o dataset Bag of Words da UCI (arquivo NyTimes). Cerca de 300k docs e vocabulario com 102650 termos# 2. Crie uma bag of words para os 3000 primeiros documentosword_list = bwreaders.ReadVocabulary(VOCAB_FILE)D_t_work = 3000table_docs = bwreaders.ReadDocuments(DOCWORD_FILE, D_t_work)#documents =  bwreaders.read_document_corpus(filepath= './docword.nytimes.txt_preprocessed.txt',#                                              num_docs=3000,#                                              num_words_in_vocabulary=102650)documents = table_docs[0]# n documentosD = table_docs[1]# n palavrasW = table_docs[2]# n entradasNNZ = table_docs[3]# 3# 3. Calcule a distancia entre cada par de pontos atraves da forca bruta e messa o tempo computacional deste procedimento. Armazene estes valores. Utilize dois loops para fazer isso e implemente o calculo da distanciamtx_original_distance = bwdistance.GenerateOriginalDistanceMatrix(D_t_work, W, documents)# 4# 4. Para n = 4, 16, 64, 256, 1024, 4096, 15768, repita o procedimento abaixo 30 vezesrepeat = 30n_cases = [ 4, 16, 64, 256, 1024, 4096, 15768 ]##################################################################### Versão 1:# - Geração da matriz # - Projeção (maior consumo de memória)####################################################################bwruns.RunVersion01(documents, mtx_original_distance, n_cases, repeat, W, D_t_work, output_path)##################################################################### Versão 2:# - Geração e projeção ao mesmo tempo (menor consumo de memória)####################################################################bwruns.RunVersion02(documents, mtx_original_distance, n_cases, repeat, W, D_t_work, output_path)