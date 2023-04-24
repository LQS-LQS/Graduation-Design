import os
import numpy as np
from PIL import Image

def jpeg_compression_quality(img_file, quality):
    """
    使用PIL库中的jpeg压缩函数压缩图像并返回压缩后的图像对象
    """
    img = Image.open(img_file)
    img = img.convert('RGB')
    img.save('temp.jpg', 'JPEG', quality=quality)
    compressed_img = Image.open('temp.jpg')
    return compressed_img

def mean_square_error(img1, img2):
    """
    计算两张图像之间的均方误差（MSE）
    """
    img1 = np.array(img1, dtype=np.float32)
    img2 = np.array(img2, dtype=np.float32)
    mse = np.mean((img1 - img2) ** 2)
    return mse

def classify_jpeg_compression(img_file, threshold=50):
    """
    判断JPEG图片压缩算法的损失情况是否达到标准
    """
    original_img = Image.open(img_file)
    compressed_img = jpeg_compression_quality(img_file, quality=50)
    mse = mean_square_error(original_img, compressed_img)
    os.remove('temp.jpg')
    if mse > threshold:
        return '压缩算法损失严重'
    else:
        return '压缩算法损失较小'

# 测试代码
# img_file = 'example.jpg'
# result = classify_jpeg_compression(img_file, threshold=50)
# print(result)

l1 = Image.open("./testImages/5.1.09.jpg")
l2 = Image.open("./testImages/5.1.09_buffer.jpg")
res = mean_square_error(l1, l2)
print(res)