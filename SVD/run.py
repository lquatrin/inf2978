import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import cur_gen
import svd
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


print("Initializing SVD")
svd.generate(image_red,image_green,image_blue,dimension,original_bytes,row,col)

print("Initializing CUR")
 
cur_gen.generate(image_red,image_green,image_blue,dimension,original_bytes,row,col)