/**
 *  Leonardo Quatrin Campagnolo
 *  campagnolo.lq@gmail.com
 *
 *  April 2017
**/

#include "randomgen.h"

#include <random>
#include <iostream>

std::mt19937 *gen = NULL;
std::uniform_real_distribution<> *dis = NULL;

#define _USE_MATH_DEFINES
#include <math.h>

void InitUniformDistribution ()
{
  std::random_device rd;  //Will be used to obtain a seed for the random number engine
  gen = new std::mt19937(rd()); //Standard mersenne_twister_engine seeded with rd()
  dis = new std::uniform_real_distribution<>(0, 1);
}

void ClearUniformDistribution ()
{
  delete dis;
}

double RandomGenGaussianValue (double mean, double standard_deviation)
{
  double x = (*dis)((*gen));

  double expo = powf((x - mean) / standard_deviation, 2.0);

  double f_den = (standard_deviation*sqrt(2.0 *  M_PI));
  
  double ret_val = (1.0 / f_den) * exp(-(1.0 / 2.0) * expo);

  return ret_val;
}

double RandomGenAchiloptasValue ()
{
  double ret_val = 1;

  double x = (*dis)((*gen));

  if(x < 1.0/6.0)
    ret_val = -1;
  else if(x < 5.0/6.0)
    ret_val = 0;

  return ret_val;
}
