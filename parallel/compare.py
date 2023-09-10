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

def UCID1338_jpeg_2000_compress():
  for num in range(1,1339):
    try:
      print(num)
      quality = 100
      source_size = os.path.getsize(f"./UCID1338/{num}.tif") / 1024
      target_size = os.path.getsize(f"./UCID1338/{num}_res.jpg") / 1024
      im = Image.open(f"./UCID1338/{num}.tif")

      while source_size > target_size:
        im.save(f"./UCID1338/{num}_2000.jpg", quality=quality)
        if quality < 1:
          break
        quality -= 1
        source_size = os.path.getsize(f"./UCID1338/{num}_2000.jpg") / 1024
    except:
      continue
  return
def jpeg_2000_compress():
  for item in variables:
    for num in range(1,99):
      try:
        quality = 100
        source_size = os.path.getsize(f"./Images/{item}/{item}{num:02}.tif") / 1024
        target_size = os.path.getsize(f"./Images/{item}/{item}{num:02}_res.jpg") / 1024
        im = Image.open(f"./Images/{item}/{item}{num:02}.tif")
    
        while source_size > target_size:
          im.save(f"./Images/{item}/{item}{num:02}_2000.jpg", quality=quality)
          if quality < 1:
            break
          quality -= 1
          source_size = os.path.getsize(f"./Images/{item}/{item}{num:02}_2000.jpg") / 1024
      except:
        continue
    print(item)

def compare():
  for item in variables:
    for num in range(1,99):
      try:
        jpeg_original = f"./Images/{item}/{item}{num:02}.tif"
        jpeg_compressed = f"./Images/{item}/{item}{num:02}_res.jpg"
        jpeg_2000 = f"./Images/{item}/{item}{num:02}_2000.jpg"
        # 读取原始图像和经过压缩后的图像
        original_img = Image.open(jpeg_original)
        compressed_img = Image.open(jpeg_compressed)
        jpeg_2000_img = Image.open(jpeg_2000)
        
        original_img = np.array(original_img)
        compressed_img = np.array(compressed_img)
        jpeg_2000_img = np.array(jpeg_2000_img)
        # 计算均方误差
        mse = np.mean((original_img - compressed_img) ** 2) # 
        mse_2000 = np.mean((original_img - jpeg_2000_img) ** 2) # 
        # 计算峰值信噪比
        max_pixel_value = 255
        psnr = 10 * np.log10((max_pixel_value ** 2) / mse) # 
        psnr_2000 = 10 * np.log10((max_pixel_value ** 2) / mse_2000) # 

        print(f"自己的图片{num}:    MSE={mse},      PSNR={psnr}")
        print(f"标准的图片{num}:    MSE={mse_2000},      PSNR={psnr_2000}")
      except:
        continue

def test_compare():
  total_MSE = []
  total_MSE_2000 = []
  total_PSNR = []
  total_PSNR_2000 = []
  total_SSIM = []
  total_SSIM_2000 = []
  for i in range(1,31):
    item = variables[random.randint(0, len(variables)-1)]
    num = random.randint(1,99)
    
    
    jpeg_original = f"./Images/{item}/{item}{num:02}.tif"
    jpeg_compressed = f"./Images/{item}/{item}{num:02}_res.jpg"
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
  UCID1338_total_MSE = []
  UCID1338_total_MSE_2000 = []
  UCID1338_total_PSNR = []
  UCID1338_total_PSNR_2000 = []
  UCID1338_total_SSIM = []
  UCID1338_total_SSIM_2000 = []

  for times in range(1,15):
    num = random.randint(1,1338)
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
    ssim = metrics.structural_similarity(original_img, compressed_img ,channel_axis=2)
    ssim_2000 = metrics.structural_similarity( original_img, jpeg_2000_img, channel_axis=2)
    
    print(f"自己的图片{num}:    MSE={mse},      PSNR={psnr},  SSIM={ssim}")
    print(f"标准的图片{num}:    MSE={mse_2000},      PSNR={psnr_2000},  SSIM={ssim_2000}")
    UCID1338_total_MSE.append( round(mse,1) )
    UCID1338_total_MSE_2000.append( round(mse_2000,1) )
    UCID1338_total_PSNR.append( round(psnr,1))
    UCID1338_total_PSNR_2000.append( round(psnr_2000,1))
    UCID1338_total_SSIM.append( round(ssim, 2))
    UCID1338_total_SSIM_2000.append( round(ssim_2000,2))
  print("total_MSE:", UCID1338_total_MSE)
  print("total_MSE_2000:", UCID1338_total_MSE_2000)
  print("total_PSNR:", UCID1338_total_PSNR)
  print("total_PSNR_2000:", UCID1338_total_PSNR_2000)
  print("total_SSIM:", UCID1338_total_SSIM)
  print("total_SSIM_2000:", UCID1338_total_SSIM_2000)
  return


#jpeg_2000_compress()
#compare()
# test_compare()

#UCID1338_jpeg_2000_compress()
UCID1338_compare()