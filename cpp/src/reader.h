#pragma once

#include <vector>
#include <iostream>
#include <fstream>
#include <string>
#include <map>

std::vector<std::string> ReadingVocabulary (std::string file_name);

std::vector<std::map<unsigned int, unsigned int>> ReadingDocuments (std::string file_name, int n_documents, int* D, int* W, int* NNZ);