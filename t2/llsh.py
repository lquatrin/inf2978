import numpy as np
import lminhash

class lLSH:
  def __init__(self, hash_signatures, threshold):
    self.data = []
    self.mhnames = []
    self.n_signatures = hash_signatures
    self.n_files = 0
    self.mh_threshold = threshold
		
  def f(self):
    return 'hello world'
		
  def Insert(self, f_name, f_minhash):
    self.mhnames.append(f_name)
    self.data.append(f_minhash)
    self.n_files += 1

  def EvaluateMinHash(self, mhash, f_mhash):
    return sum([u==v for u,v in zip(mhash.GetData(),f_mhash.GetData())])/len(f_mhash.GetData())
	
  def query(self, fminhashq):
    ret = []
    for i in range(self.n_files):
      if self.EvaluateMinHash(self.data[i], fminhashq) >= self.mh_threshold:
        ret.append(self.mhnames[i])

    return ret