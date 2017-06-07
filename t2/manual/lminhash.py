import numpy as np

class lMinHash:
  def __init__(self, minhash_data):
    self.mh_data = minhash_data

  def GetData(self):
    return self.mh_data