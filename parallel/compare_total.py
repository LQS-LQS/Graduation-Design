'''
MSE在500以下的图像质量相对比较好，MSE在1000以下的图像质量一般可以接受
MSE  :  衡量原始图像和经过压缩后的图像之间差异的一种方法  
        MSE计算的是每个像素值之间的平方误差的均值
PSNR :  衡量压缩算法输出图像质量的一种方法 
        PSNR表示原始图像和经过压缩后的图像之间的峰值信噪比  
        峰值信噪比越高，表示压缩算法输出的图像质量越好
'''

import numpy as np
import os
from PIL import Image
import random
from skimage import io, metrics, color

variables=[ "agricultural", "airplane", "baseballdiamond", "beach", "buildings",
            "denseresidential", "forest", "freeway", "golfcourse", "harbor", 
            "intersection", "mediumresidential", "mobilehomepark", "overpass", "parkinglot", 
            "river", "runway", "sparseresidential", "storagetanks", "tenniscourt"]
# variables= ["runway", "sparseresidential", "storagetanks", "tenniscourt"]


def UCID1338_compare():
  mseTotal = 0
  psnrTotal = 0
  ssimTotal = 0
  picNum = 0

  for num in range(1,1338):
    try:
      jpeg_original = f"./UCID1338/{num}.tif"
      jpeg_compressed = f"./UCID1338/{num}_res.jpg"


      # 读取原始图像和经过压缩后的图像
      original_img = Image.open(jpeg_original)
      compressed_img = Image.open(jpeg_compressed)


      original_img = np.array(original_img,dtype=np.uint8)
      compressed_img = np.array(compressed_img,dtype=np.uint8)



      mse = np.mean((original_img - compressed_img) ** 2) # 

      max_pixel_value = 255
      psnr = 10 * np.log10((max_pixel_value ** 2) / mse) # 

      ssim = metrics.structural_similarity(original_img, compressed_img ,channel_axis=2)

      mseTotal += mse
      psnrTotal += psnr
      ssimTotal += ssim

      picNum += 1
      print(num)
    except:
      continue

  print("mse ave:", mseTotal / picNum)
  print("psnr ave:", psnrTotal / picNum)
  print("ssim ave:", ssimTotal / picNum)
  return


def test_compare():
  mseTotal = 0
  psnrTotal = 0
  ssimTotal = 0
  picNum = 0
  for item in variables:
    for num in range(1,99):
      try:
        jpeg_original = f"./Images/{item}/{item}{num:02}.tif"
        jpeg_compressed = f"./Images/{item}/{item}{num:02}_res.jpg"

        # 读取原始图像和经过压缩后的图像
        original_img = Image.open(jpeg_original)
        compressed_img = Image.open(jpeg_compressed)
      
      
        original_img = np.array(original_img,dtype=np.uint8)
        compressed_img = np.array(compressed_img,dtype=np.uint8)

        mse = np.mean((original_img - compressed_img) ** 2) # 

        max_pixel_value = 255
        psnr = 10 * np.log10((max_pixel_value ** 2) / mse) # 
      
        ssim = metrics.structural_similarity(original_img, compressed_img ,channel_axis=2)
        mseTotal += mse
        psnrTotal += psnr
        ssimTotal += ssim

        picNum += 1
        print(num)
      except:
        continue

  print("mse ave:", mseTotal / picNum)
  print("psnr ave:", psnrTotal / picNum)
  print("ssim ave:", ssimTotal / picNum)
  return

#UCID1338_compare()

test_compare()