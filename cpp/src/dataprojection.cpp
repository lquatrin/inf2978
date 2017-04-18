/**
 *  Leonardo Quatrin Campagnolo
 *  campagnolo.lq@gmail.com
 *
 *  April 2017
**/

#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <map>

#include "dataprojection.h"

#include "reader.h"

#ifdef USE_SINGLE_PRECISION
  #define precision_type float
#else
  #define precision_type double
#endif

#include "distance.h"

#ifdef USE_MYMATH
  #include "MathFunctions.h"
#endif

#define NUMBER_OF_DOCUMENTS 3000

#ifndef uint
  #define uint unsigned int
#endif


precision_type distances[NUMBER_OF_DOCUMENTS][NUMBER_OF_DOCUMENTS];

int main (int argc, char *argv[])
{
  // 1 2
  // 1. Baixe o dataset Bag of Words da UCI(arquivo NyTimes).Cerca de 300k docs e vocabulario com 102650 (é 102660) termos
  // 2. Crie uma bag of words para os 3000 primeiros documentos
  std::vector<std::string> vocabulary = ReadingVocabulary("../vocab.nytimes.txt");
  int D, W, NNZ;
  std::vector<std::map<uint, uint>> documents = ReadingDocuments("../../docword.nytimes.txt", NUMBER_OF_DOCUMENTS, &D, &W, &NNZ);

  // 3
  // 3. Calcule a distancia entre cada par de pontos atraves da forca bruta e messa o tempo computacional deste procedimento.
  //    Armazene estes valores. Utilize dois loops para fazer isso e implemente o calculo da distancia
  #ifdef COMPUTE_TIME
  #endif
  for(int x = 0; x < 3000; x++)
  {
    distances[x][x] = 0;
    for (int y = x + 1; y < 3000; y++)
    {
      distances[x][y] = distances[y][x] = EuclideanDistanceBetweenDocuments(documents[x], documents[y]);
    }
  }
  #ifdef COMPUTE_TIME
  #endif  

  // 4
  // 4. Para n = 4, 16, 64, 256, 1024, 4096, 15768, repita o procedimento abaixo 30 vezes
  std::vector<unsigned int> n_cases = { 4, 16, 64, 256, 1024, 4096, 15768 };
  for(int c = 0; c < n_cases.size(); c++)
  {
    unsigned int n = n_cases[c];

    // 4.1. Obtenha uma matriz aleatoria de n linhas e d colunas pelo metodo de Achiloptas e pelo metodo dado em aula, onde d e o tamanho do vocaulario.
  
  
    // 4.2. Messa o tempo computacional da geracao das matrizes
    // Achiloptas
    #ifdef COMPUTE_TIME
    #endif  
    #ifdef COMPUTE_TIME
    #endif  

    // Random projections with gaussian
    #ifdef COMPUTE_TIME
    #endif  
    #ifdef COMPUTE_TIME
    #endif  
    
    
    // 4.3. Projete os 3000 documentos no espaco Rn atraves das matrizes geradas. Messa o tempo da projecao
    #ifdef COMPUTE_TIME
    #endif  
    #ifdef COMPUTE_TIME
    #endif  
    
    
    // 4.4. Messa o tempo para obter todas as distancias entre os pontos projetados
    #ifdef COMPUTE_TIME
    #endif  
    #ifdef COMPUTE_TIME
    #endif  

    
    // 4.5. Calcule a distorsao maxima em relacao aos dados originais.
  
    
    // 4.6. Calcule o limite superior da distorsao previsto pelo Lema de J.L.
  

  }

  // 5. Escreva um relatorio descrevendo os experimentos e os resultados obtidos.
  //    Analise se os resultados obtidos estao de acordo com a teoria apresentada.
  //    Considere a media, o maximo e o minimo dos 30 experimentos do item 4.
		  
  return 0;
}