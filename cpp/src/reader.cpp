/**
 *  Leonardo Quatrin Campagnolo
 *  campagnolo.lq@gmail.com
 *
 *  April 2017
**/

#include "reader.h"

// Reading vocabulary
std::vector<std::string> ReadingVocabulary (std::string file_name)
{
  std::vector<std::string> vocabulary;

  std::string line_vocab;
  std::ifstream vocab_in_file(file_name);
  while (getline(vocab_in_file, line_vocab))
    vocabulary.push_back(line_vocab);
  vocab_in_file.close();

  return vocabulary;
}

// Reading Documents
std::vector<std::map<unsigned int, unsigned int>> ReadingDocuments (std::string file_name, int n_documents, int* D, int* W, int* NNZ)
{
  std::vector<std::map<unsigned int, unsigned int>> documents;

  std::ifstream documents_in_file(file_name);
  //std::hash<unsigned int>()
  for (int i = 0; i < n_documents; i++)
    documents.push_back(std::map<unsigned int, unsigned int>());

  // D = Number of Documents
  // W = Number of words
  // NNZ = Number of queries
  documents_in_file >> (*D) >> (*W) >> (*NNZ);

  int doc_id, word_id, count;
  while (documents_in_file >> doc_id >> word_id >> count)
  {
    // Only the first 3000 Documents
    if (doc_id > n_documents) break;

    // Correct the indexes of documents and words
    doc_id = doc_id - 1;
    word_id = word_id - 1;

    //std::cout << documents[doc_id].size() << std::endl;

    documents[doc_id][word_id] = count;
  }
  documents_in_file.close();

  return documents;
}