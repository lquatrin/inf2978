#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#include <iostream>
#include <fstream>
#include <string>
#include <vector>

#include "dataprojection.h"

#ifdef USE_MYMATH
  #include "MathFunctions.h"
#endif

#define NUMBER_OF_DOCUMENTS 3000

int main (int argc, char *argv[])
{
  std::string line;

  std::ifstream vocab_in_file("../vocab.nytimes.txt");
  // Reading vocabulary
  std::vector<std::string> vocabulary;
  while (getline(vocab_in_file, line))
    vocabulary.push_back(line);
  vocab_in_file.close();

  std::ifstream documents_in_file("../../docword.nytimes.txt");
  // Reading Documents
  std::vector<std::hash<unsigned int>> documents;
  for (int i = 0; i < NUMBER_OF_DOCUMENTS; i++)
    documents.push_back(std::hash<unsigned int>());

  // D = Number of Documents
  // W = Number of words
  // NNZ = Number of queries
  int D, W, NNZ;
  documents_in_file >> D >> W >> NNZ;

  int doc_id, word_id, count;
  while (documents_in_file >> doc_id >> word_id >> count)
    std::cout << doc_id - 1 << ", " << word_id - 1 << ", " << count << std::endl;
    //documents_in_file.push_back(line);
  documents_in_file.close();



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