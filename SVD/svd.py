import numpy as np
from PIL import Image

image = np.array(Image.open('lena.jpg'))
image = image/255
row, col, _ = image.shape
print ('pixels ', row ,' X ', col)

#separa os canais de cores
image_red = image[:,:,0]
image_green = image[:,:,1]
image_blue = image[:,:,2]

original_bytes = image.nbytes
print ("Space to store this",original_bytes)

# decomposição SVD para 3 matrizes correspondentes a cada canal
U_r,d_r,V_r = np.linalg.svd(image_red,full_matrices=True)
U_g,d_g,V_g = np.linalg.svd(image_green,full_matrices=True)
U_b,d_b,V_b = np.linalg.svd(image_blue,full_matrices=True)

#TODO
#APLICAR A PROJEÇÃO ALEATÓRIA CADA CANAL DE COR 
U_r_k = U_r #..... 
U_g_k = U_g #.....
U_b_k = U_b #.....

d_r_k = d_r #.....
d_g_k = d_g #.....
d_b_k = d_b #.....

V_r_k = V_r #.....
V_g_k = V_g #.....
V_b_k = V_b #.....

#TO DO
#RECONSTRUÇÃO DA IMAGEM

compressed = sum([matrix.nbytes for matrix in 
                        [U_r_k, d_r_k, V_r_k, U_g_k, d_g_k, V_g_k, U_b_k, d_b_k, V_b_k]])

print("size compressed ",compressed)
ratio = compressed/original_bytes
print("ratio ",ratio)

#red_recon = np.dot(U_r_k, np.dot(np.diag(d_r_k), V_r_k))
#green_recon = np.dot(U_g_k, np.dot(np.diag(d_g_k), V_g_k))
#blue_recon = np.dot(U_b_k, np.dot(np.diag(d_b_k), V_b_k))

#image_recon = np.zeros((row,col,3))

#image_recon[:,:,0] = red_recon
#image_recon[:,:,1] = green_recon
#image_recon[:,:,2] = blue_recon

#image_recon[image_recon < 0] = 0
#image_recon[image_recon > 1] = 1

#TO DO - plot image