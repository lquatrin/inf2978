import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import cur


def generate(image_red,image_green,image_blue,dimension,original_bytes,row,col):

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
    
    result = Image.fromarray((image_recon * 255).astype(np.uint8))
    result.save('lena_svd_'+str(n)+'.jpg')


 
