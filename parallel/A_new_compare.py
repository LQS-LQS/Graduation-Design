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




def test_compare():
  index_arr = [97, 25, 90, 72, 86, 86, 7, 25, 30, 63, 75, 1, 19, 35, 99, 76, 97, 49, 62, 47]
  variables=[ "agricultural", "airplane", "baseballdiamond", "beach", "buildings",
            "denseresidential", "forest", "freeway", "golfcourse", "harbor", 
            "intersection", "mediumresidential", "mobilehomepark", "overpass", "parkinglot", 
            "river", "runway", "sparseresidential", "storagetanks", "tenniscourt"]
  total_MSE = []
  total_MSE_2000 = []
  total_PSNR = []
  total_PSNR_2000 = []
  total_SSIM = []
  total_SSIM_2000 = []
  for i in range(0, len(index_arr)):
    
    item = variables[i]
    num = index_arr[i]
    
    jpeg_original = f"./Images/{item}/{item}{num:02}.tif"
    jpeg_compressed = f"./Images/{item}/{item}{num:02}_resqq.jpg"
    jpeg_2000 = f"./Images/{item}/{item}{num:02}_2000.jpg"

    # 读取原始图像和经过压缩后的图像
    original_img = Image.open(jpeg_original)
    compressed_img = Image.open(jpeg_compressed)
    jpeg_2000_img = Image.open(jpeg_2000)
    
    
    original_img = np.array(original_img,dtype=np.uint8)
    compressed_img = np.array(compressed_img,dtype=np.uint8)
    jpeg_2000_img = np.array(jpeg_2000_img,dtype=np.uint8)
    # 计算均方误差
    mse = np.mean((original_img - compressed_img) ** 2) # 
    mse_2000 = np.mean((original_img - jpeg_2000_img) ** 2) # 
    # 计算峰值信噪比
    max_pixel_value = 255
    psnr = 10 * np.log10((max_pixel_value ** 2) / mse) # 
    psnr_2000 = 10 * np.log10((max_pixel_value ** 2) / mse_2000) # 
    # 计算ssim
    #ssim = metrics.structural_similarity(io.imread(jpeg_original, as_gray=True), io.imread(jpeg_compressed, as_gray=True))
    #io.imread(jpeg_original, as_gray=True)
    ssim_2000 = metrics.structural_similarity( original_img, jpeg_2000_img, channel_axis=2)
    
    ssim = metrics.structural_similarity(original_img, compressed_img ,channel_axis=2)
    print(f"{item}自己的图片{num}:    MSE={mse},      PSNR={psnr},  SSIM={ssim}")
    print(f"{item}标准的图片{num}:    MSE={mse_2000},      PSNR={psnr_2000},  SSIM={ssim_2000}")
    total_MSE.append( round(mse,1) )
    total_MSE_2000.append( round(mse_2000,1) )
    total_PSNR.append( round(psnr,1))
    total_PSNR_2000.append( round(psnr_2000,1))
    total_SSIM.append( round(ssim, 2))
    total_SSIM_2000.append( round(ssim_2000,2))
  print("total_MSE:", total_MSE)
  print("total_MSE_2000:", total_MSE_2000)
  print("total_PSNR:", total_PSNR)
  print("total_PSNR_2000:", total_PSNR_2000)
  print("total_SSIM:",total_SSIM)
  print("total_SSIM_2000:",total_SSIM_2000)
  return



def UCID1338_compare():
  index_arr = [282, 1162, 543, 574, 500, 1060, 562, 430, 1059, 146, 334, 731, 445, 280, 330, 1155, 545, 541, 1160, 557]
  total_MSE = []
  total_MSE_2000 = []
  total_PSNR = []
  total_PSNR_2000 = []
  total_SSIM = []
  total_SSIM_2000 = []
  for num in index_arr:
    jpeg_original = f"./UCID1338/{num}.tif"
    jpeg_compressed = f"./UCID1338/{num}_res.jpg"
    jpeg_2000 = f"./UCID1338/{num}_2000.jpg"

    # 读取原始图像和经过压缩后的图像
    original_img = Image.open(jpeg_original)
    compressed_img = Image.open(jpeg_compressed)
    jpeg_2000_img = Image.open(jpeg_2000)
    
    
    original_img = np.array(original_img,dtype=np.uint8)
    compressed_img = np.array(compressed_img,dtype=np.uint8)
    jpeg_2000_img = np.array(jpeg_2000_img,dtype=np.uint8)
    # 计算均方误差
    mse = np.mean((original_img - compressed_img) ** 2) # 
    mse_2000 = np.mean((original_img - jpeg_2000_img) ** 2) # 
    # 计算峰值信噪比
    max_pixel_value = 255
    psnr = 10 * np.log10((max_pixel_value ** 2) / mse) # 
    psnr_2000 = 10 * np.log10((max_pixel_value ** 2) / mse_2000) # 
    # 计算ssim
    #ssim = metrics.structural_similarity(io.imread(jpeg_original, as_gray=True), io.imread(jpeg_compressed, as_gray=True))
    #io.imread(jpeg_original, as_gray=True)
    ssim_2000 = metrics.structural_similarity( original_img, jpeg_2000_img, channel_axis=2)
    
    ssim = metrics.structural_similarity(original_img, compressed_img ,channel_axis=2)
    print(f"自己的图片{num}:    MSE={mse},      PSNR={psnr},  SSIM={ssim}")
    print(f"标准的图片{num}:    MSE={mse_2000},      PSNR={psnr_2000},  SSIM={ssim_2000}")
    total_MSE.append( round(mse,1) )
    total_MSE_2000.append( round(mse_2000,1) )
    total_PSNR.append( round(psnr,1))
    total_PSNR_2000.append( round(psnr_2000,1))
    total_SSIM.append( round(ssim, 2))
    total_SSIM_2000.append( round(ssim_2000,2))
  print("total_MSE:", total_MSE)
  print("total_MSE_2000:", total_MSE_2000)
  print("total_PSNR:", total_PSNR)
  print("total_PSNR_2000:", total_PSNR_2000)
  print("total_SSIM:",total_SSIM)
  print("total_SSIM_2000:",total_SSIM_2000)
  return


#jpeg_2000_compress()
#compare()

UCID1338_compare()