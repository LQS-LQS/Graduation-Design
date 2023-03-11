from PIL              import Image
import numpy as np

input_image_path = "D:\\MyCode-Git\\Graduation-Design\\result_1.jpg"
image_to_compress = Image.open(input_image_path) # 读入图片
ycbcr = image_to_compress.convert('YCbCr') # RGB转换为YCbCr
npmat = np.array(ycbcr, dtype=int) - 128 # 归一化处理,每一个分量的范围-128~127, npmat:width * height * 3
rows,cols = npmat.shape[0],npmat.shape[1] # 像素的行数和列数
Cb = npmat[::2,::2,1] # 行数和列数步长为2
print("lqs",rows,cols)
print("Cb初始：",Cb.flatten().size)
Cb = np.mean(npmat[::2,::2,1:2], axis=(1,2),keepdims=True).astype(int)
print(Cb.flatten().size)
# print(rows/2,cols/2)
# Cb = Cb.reshape( int(rows/2), int(cols/2) )