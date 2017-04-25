# Generate random numberimport randomimport mathimport timeimport numpy as np#def RandomGenGaussianValue(mean, st_dev):#  return np.random.normal(mean, st_dev, 1)[0]# https://en.wikipedia.org/wiki/Box%E2%80%93Muller_transform# Box-Muller transform to generate values from standard normal distribution#BoxMullerTransformdef RandomGenGaussianValue(mean, st_dev):  U = random.random()  V = random.random()  a = math.sqrt((-2.0) * math.log(U))  b = 2.0 * math.pi * V  return mean + st_dev * (a * math.cos(b)), mean + st_dev * (a * math.sin(b))  def RandomGenAchiloptasValue():  x = random.random()    #elif x <= 1:  ret_val = 1.0    if x < 1.0/6.0:    ret_val = -1.0  elif x < 5.0/6.0:    ret_val = 0.0    return ret_valdef GenerateRandomGaussianMatrix(n, d):  s_clock = time.clock()    W = np.zeros(shape = (n,d))  s_dev = math.sqrt(1.0/float(n))  # 102660 / 2 = 51330  half_d = int(d / 2)  for i in range(n):    for j in range(half_d):      a, b = RandomGenGaussianValue(0.0, s_dev)      W[i][2*j] = a      W[i][2*j + 1] = b              f_clock = time.clock()    return W, (f_clock - s_clock)def GenerateRandomAchiloptasMatrix(n, d):  s_clock = time.clock()  W = np.zeros(shape = (n,d))  for i in range(n):    for j in range(d):      W[i][j] = RandomGenAchiloptasValue()  f_clock = time.clock()  return W, (f_clock - s_clock)  