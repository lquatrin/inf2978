class lLSH:
  def __init__(self, hash_signatures):
    self.data = dict()
    self.n_signatures = hash_signatures
		
  def f(self):
    return 'hello world'
		
  def Insert(self, f_name, f_minhash):
    self.data[f_name] = f_minhash
	
  def EvaluateSimiliarities(self):
    print("hello")