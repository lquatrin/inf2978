import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
image = Image.open('lena.jpg')
#image = image/255
#row, col, _ = image.shape
#print ('pixels ', row ,' X ', col)

#imggray = image.convert('LA')
imgmat = np.array(list(image.getdata(band=0)), float)
imgmat.shape = (image.size[1], image.size[0])
imgmat = np.matrix(imgmat)
rank = np.linalg.matrix_rank(imgmat)
print(rank)

dimension = rank/100

#separa os canais de cores
img = np.array(image)
img = img/255
row, col, _ = img.shape
print ('pixels ', row ,' X ', col)
image_red = img[:,:,0]
image_green = img[:,:,1]
image_blue = img[:,:,2]

original_bytes = img.nbytes
print ("Space to store this",original_bytes)

# decomposição SVD para 3 matrizes correspondentes a cada canal
U_r,d_r,V_r = np.linalg.svd(image_red,full_matrices=True)
U_g,d_g,V_g = np.linalg.svd(image_green,full_matrices=True)
U_b,d_b,V_b = np.linalg.svd(image_blue,full_matrices=True)

cases = [1,2,5,10]
for n in cases:

  dim = int(dimension * n)
  U_r_k = U_r[:,0:dim]
  U_g_k = U_g[:,0:dim]
  U_b_k = U_b[:,0:dim]
  
  d_r_k = d_r[0:dim]
  d_g_k = d_g[0:dim]
  d_b_k = d_b[0:dim]
  
  V_r_k = V_r[0:dim,:]
  V_g_k = V_g[0:dim,:]
  V_b_k = V_b[0:dim,:]
  #TO DO
  #RECONSTRUÇÃO DA IMAGEM
  
  compressed = sum([matrix.nbytes for matrix in 
                          [U_r_k, d_r_k, V_r_k, U_g_k, d_g_k, V_g_k, U_b_k, d_b_k, V_b_k]])
  
  print("size compressed ",compressed)
  ratio = compressed/original_bytes
  print("ratio ",ratio)
  
  red_recon = np.dot(U_r_k, np.dot(np.diag(d_r_k), V_r_k))
  green_recon = np.dot(U_g_k, np.dot(np.diag(d_g_k), V_g_k))
  blue_recon = np.dot(U_b_k, np.dot(np.diag(d_b_k), V_b_k))
  
  image_recon = np.zeros((row,col,3))
  
  image_recon[:,:,0] = red_recon
  image_recon[:,:,1] = green_recon
  image_recon[:,:,2] = blue_recon
  
  image_recon[image_recon < 0] = 0
  image_recon[image_recon > 1] = 1
  
  fig = plt.figure(figsize=(15,10))
  a = fig.add_subplot(1,1,1)
  imgplot = plt.imshow(image_recon)
  plt.show()
