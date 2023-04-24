from PIL import Image
import os

# 比较图片大小


def compare_image_size(num,img1_path, img2_path):
  size1 = os.path.getsize(img1_path)
  size2 = os.path.getsize(img2_path)

  ans = (size2-size1) / size2 * 100
  ans = round(ans,3)
  print(f"第{num}张图片,  压缩比例:{ans}%")




# 示例使用

for num in range(1,20,1):
  img1_path = f"./optimize/testImages/t{num}"
  img2_path = f"./origin/testImages/t{num}"
  compare_image_size(num,img1_path, img2_path)
