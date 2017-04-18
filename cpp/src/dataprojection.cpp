#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <map>

#include "dataprojection.h"

#ifdef USE_MYMATH
  #include "MathFunctions.h"
#endif

#define NUMBER_OF_DOCUMENTS 3000

#ifndef uint
  #define uint unsigned int
#endif

#ifdef USE_SINGLE_PRECISION
  #define precision_type float
#else
  #define precision_type double
#endif

precision_type distances[NUMBER_OF_DOCUMENTS][NUMBER_OF_DOCUMENTS];

int main (int argc, char *argv[])
{
  // 1 2
  // 1. Baixe o dataset Bag of Words da UCI(arquivo NyTimes).Cerca de 300k docs e vocabulario com 102650 (é 102660) termos
  // 2. Crie uma bag of words para os 3000 primeiros documentos

  std::vector<std::string> vocabulary;
  std::vector<std::map<uint, uint>> documents;

  // Reading vocabulary
  //////////////////////////////////////////////////////////////////////
  std::string line_vocab;
  std::ifstream vocab_in_file("../vocab.nytimes.txt");
  while (getline(vocab_in_file, line_vocab))
    vocabulary.push_back(line_vocab);
  vocab_in_file.close();
  //////////////////////////////////////////////////////////////////////

  // Reading Documents
  //////////////////////////////////////////////////////////////////////
  std::ifstream documents_in_file("../../docword.nytimes.txt");
  //std::hash<unsigned int>()
  for (int i = 0; i < NUMBER_OF_DOCUMENTS; i++)
    documents.push_back(std::map<uint, uint>());

  // D = Number of Documents
  // W = Number of words
  // NNZ = Number of queries
  int D, W, NNZ;
  documents_in_file >> D >> W >> NNZ;

  int doc_id, word_id, count;
  while (documents_in_file >> doc_id >> word_id >> count)
  {
    // Only the first 3000 Documents
    if (doc_id > NUMBER_OF_DOCUMENTS) break;

    // Correct the indexes of documents and words
    doc_id = doc_id - 1;
    word_id = word_id - 1;

    //std::cout << documents[doc_id].size() << std::endl;
    
    documents[doc_id][word_id] = count;
  }
  documents_in_file.close();
  //////////////////////////////////////////////////////////////////////

  // 3
  // 3. Calcule a distancia entre cada par de pontos atraves da forca bruta e messa o tempo computacional deste procedimento.
  //    Armazene estes valores. Utilize dois loops para fazer isso e implemente o calculo da distancia
  for(int x = 0; x < 3000; x++)  {    distances[x][x] = 0;    for (int y = 0; y < 3000; y++)    {      distances[x][y] = distances[y][x] = 0; //EuclideanDistance    }  }  
  // 4
  // 4. Para n = 4, 16, 64, 256, 1024, 4096, 15768, repita o procedimento abaixo 30 vezes
  std::vector<unsigned int> n_cases = { 4, 16, 64, 256, 1024, 4096, 15768 };
  for(int c = 0; c < n_cases.size(); c++)
  {
    unsigned int n = n_cases[c];

    // 4.1. Obtenha uma matriz aleatoria de n linhas e d colunas pelo metodo de Achiloptas e pelo metodo dado em aula, onde d e o tamanho do vocaulario.
    // 4.2. Messa o tempo computacional da geracao das matrizes
    // Achiloptas
    // Random projections with gaussian
    // 4.3. Projete os 3000 documentos no espaco Rn atraves das matrizes geradas. Messa o tempo da projecao
    // 4.4. Messa o tempo para obter todas as distancias entre os pontos projetados
    // 4.5. Calcule a distorsao maxima em relacao aos dados originais.
    // 4.6. Calcule o limite superior da distorsao previsto pelo Lema de J.L.
  }

  // 5. Escreva um relatorio descrevendo os experimentos e os resultados obtidos.
  //    Analise se os resultados obtidos estao de acordo com a teoria apresentada.
  //    Considere a media, o maximo e o minimo dos 30 experimentos do item 4.

  
  //if (argc < 2)
  //{
  //  fprintf(stdout,"%s Version %d.%d\n",
  //    argv[0],
  //    Tutorial_VERSION_MAJOR,
  //    Tutorial_VERSION_MINOR);
  //  fprintf(stdout, "Usage: %s number\n", argv[0]);
	//return 1;
  //}

//  double inputValue = atof(argv[1]);
//#ifdef USE_MYMATH
//  double outputValue = mysqrt(inputValue);
//#else
//  double outputValue = sqrt(inputValue);
//#endif
//
//  fprintf(stdout, "The square root of %g is %g\n",
//          inputValue, outputValue);
		  
  return 0;
}