import cv2
import numpy as np


def calculate_image_difference(original_image_path, compressed_image_path):
  # 读取原始图像和压缩图像
  original_image = cv2.imread(original_image_path)
  compressed_image = cv2.imread(compressed_image_path)

  # 调整压缩图像的大小，使其与原始图像大小相同
  compressed_image = cv2.resize(
    compressed_image, (original_image.shape[1], original_image.shape[0]))

  # 计算两个图像之间的差异
  difference = cv2.absdiff(original_image, compressed_image)  #计算两个图片之间的差值
  difference_gray = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)  # 从BGR颜色空间转换为灰度颜色空间
  # 计算差异图像的均值和方差
  mean_difference = np.mean(difference_gray)  # 计算所有元素的平均值
  variance_difference = np.var(difference_gray) # 计算给定数据的方差

  print(mean_difference,variance_difference)

  # 判断压缩损失是否达到标准
  if mean_difference <= 10 and variance_difference <= 50:
    return "Compression algorithm meets the standard."
  else:
    return "Compression algorithm does not meet the standard."

res = calculate_image_difference("./testImages/5.1.09.jpg","./testImages/5.1.09_buffer.jpg")

print(res)