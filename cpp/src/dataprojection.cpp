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

#include "randomgen.h"

#include "matrix.h"

ml::Matrix<precision_type> distances(NUMBER_OF_DOCUMENTS, NUMBER_OF_DOCUMENTS);

int main (int argc, char *argv[])
{
  InitUniformDistribution();
  
  // 1 2
  // 1. Baixe o dataset Bag of Words da UCI(arquivo NyTimes).Cerca de 300k docs e vocabulario com 102650 (é 102660) termos
  // 2. Crie uma bag of words para os 3000 primeiros documentos
  std::vector<std::string> vocabulary = ReadingVocabulary("../vocab.nytimes.txt");
  int D, W, NNZ;
  std::vector<std::map<uint, uint>> documents = ReadingDocuments("../../docword.nytimes.txt", NUMBER_OF_DOCUMENTS, &D, &W, &NNZ);

  // 3
  // 3. Calcule a distancia entre cada par de pontos atraves da forca bruta e messa o tempo computacional deste procedimento.
  //    Armazene estes valores. Utilize dois loops para fazer isso e implemente o calculo da distancia
  std::ifstream fin("pre_matrix_distance.txt");
  if (!fin.is_open())
  {
    #ifdef COMPUTE_TIME
    #endif
    for (int x = 0; x < NUMBER_OF_DOCUMENTS; x++)
    {
      distances.Set(0, x, x);
      for (int y = x + 1; y < NUMBER_OF_DOCUMENTS; y++)
      {
        precision_type v = EuclideanDistanceBetweenDocuments(documents[x], documents[y]);
        distances.Set(v, x, y);
        distances.Set(v, y, x);
      }
    }
    #ifdef COMPUTE_TIME
    #endif  
    std::ofstream fou("pre_matrix_distance.txt");
    for (int x = 0; x < NUMBER_OF_DOCUMENTS; x++)
      for (int y = 0; y < NUMBER_OF_DOCUMENTS; y++)
        fou << distances(x,y) << " ";
    fou.close();
  }
  else
  {
    double a;
    for (int x = 0; x < NUMBER_OF_DOCUMENTS; x++)
    {
      for (int y = 0; y < NUMBER_OF_DOCUMENTS; y++)
      {
        fin >> a;
        distances.Set(a, x, y);
      }
    }
    fin.close();
  }

  // 4
  // 4. Para n = 4, 16, 64, 256, 1024, 4096, 15768, repita o procedimento abaixo 30 vezes
  std::vector<unsigned int> n_cases = { 4, 16, 64, 256, 1024, 4096, 15768 };
  for(int c = 0; c < n_cases.size(); c++)
  {
    int n = n_cases[c];
    int d = W;

    // 4.1. Obtenha uma matriz aleatoria de n linhas e d colunas pelo metodo de Achiloptas e pelo metodo dado em aula, onde d e o tamanho do vocaulario.
    // 4.2. Messa o tempo computacional da geracao das matrizes
    // 4.3. Projete os 3000 documentos no espaco Rn atraves das matrizes geradas. Messa o tempo da projecao
    // TODO    // MATRIX_n_d * VETOR_d_1 = VERTO_n_1    // 4.4. Messa o tempo para obter todas as distancias entre os pontos projetados
  
    // 4.1 4.2 4.3 4.4 - Achiloptas
    /////////////////////////////////////////////////////////////////////
    #ifdef COMPUTE_TIME
    #endif  
    ml::Matrix<precision_type> m_achiloptas(n, d);
    for (int i = 0; i < n; i++)
    {
      for (int j = 0; j < d; j++)
      {
        precision_type v = RandomGenAchiloptasValue();
        m_achiloptas.Set(v, i, j);
      }
    }
    #ifdef COMPUTE_TIME
    #endif  
  
    #ifdef COMPUTE_TIME
    #endif  
    #ifdef COMPUTE_TIME
    #endif  

    #ifdef COMPUTE_TIME
    #endif  
    #ifdef COMPUTE_TIME
    #endif  
    /////////////////////////////////////////////////////////////////////

    // 4.1 4.2 4.3 4.4 - Random projections with gaussian
    /////////////////////////////////////////////////////////////////////
    #ifdef COMPUTE_TIME
    #endif                     
    ml::Matrix<precision_type> m_randomproj(n, d);
    double std_dev = sqrt(1.0/(double)n);
    for (int i = 0; i < n; i++)
    {
      for (int j = 0; j < d; j++)
      {
        precision_type v = RandomGenGaussianValue(0, std_dev);
        m_randomproj.Set(v, i, j);
      }
    }
    #ifdef COMPUTE_TIME
    #endif  
    
    
    #ifdef COMPUTE_TIME
    #endif  
    #ifdef COMPUTE_TIME
    #endif  
    
    #ifdef COMPUTE_TIME
    #endif  
    #ifdef COMPUTE_TIME
    #endif  
    /////////////////////////////////////////////////////////////////////
    
    // 4.5. Calcule a distorsao maxima em relacao aos dados originais.
    // Achiloptas    //distortionAch = matUtils.maxDistortion(DistanceMatrix, ProjMatAch)    // Random projections    //distortionRN = matUtils.maxDistortion(DistanceMatrix, ProjMatRN)
    
    // 4.6. Calcule o limite superior da distorsao previsto pelo Lema de J.L.
    //JL = calculateJLLema(d, n)

  }

  // 5. Escreva um relatorio descrevendo os experimentos e os resultados obtidos.
  //    Analise se os resultados obtidos estao de acordo com a teoria apresentada.
  //    Considere a media, o maximo e o minimo dos 30 experimentos do item 4.
		  
  ClearUniformDistribution();
  
  return 0;
}