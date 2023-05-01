'''
MSE在500以下的图像质量相对比较好，MSE在1000以下的图像质量一般可以接受
MSE  :  衡量原始图像和经过压缩后的图像之间差异的一种方法  
        MSE计算的是每个像素值之间的平方误差的均值
PSNR :  衡量压缩算法输出图像质量的一种方法 
        PSNR表示原始图像和经过压缩后的图像之间的峰值信噪比  
        峰值信噪比越高，表示压缩算法输出的图像质量越好
'''

import cv2
import numpy as np

for num in range(1,19):
  jpeg_original = f"./testImages/t{num}.jpg"
  jpeg_compressed = f"./testImages/t{num}_res.jpg"
  # 读取原始图像和经过压缩后的图像
  original_img = cv2.imread(jpeg_original)
  compressed_img = cv2.imread(jpeg_compressed)
  # 计算均方误差
  mse = np.mean((original_img - compressed_img) ** 2) # 

  # 计算峰值信噪比
  max_pixel_value = 255
  psnr = 10 * np.log10((max_pixel_value ** 2) / mse) # 

  print(f"图片{num}:    MSE={mse},      PSNR={psnr}")
