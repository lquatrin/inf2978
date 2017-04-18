/**
 *  Leonardo Quatrin Campagnolo
 *  campagnolo.lq@gmail.com
 *
 *  April 2017
**/

#include "distance.h"

#include <cmath>
#include <iostream>

double EuclideanDistanceBetweenDocuments (std::map<unsigned int, unsigned int> doc1, std::map<unsigned int, unsigned int> doc2)
{
  double sum_dist = 0;
  
  std::map<int, int> map_keys = std::map<int, int>();
  
  for (const auto& kv1 : doc1)
  {
    if (map_keys[kv1.first] == 0)
    {
      double diff = (double)kv1.second - (double)doc2[kv1.first];
      sum_dist = diff * diff;
      map_keys[kv1.first] = 1;
    }
  }

  for (const auto& kv2 : doc2)
  {
    if (map_keys[kv2.first] == 0)
    {
      double diff = (double)doc1[kv2.first] - (double)kv2.second;
      sum_dist = diff * diff;
      map_keys[kv2.first] = 1;
    }
  }

  return sqrt(sum_dist);
}