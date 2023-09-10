from PIL import Image
import os
from skimage import measure
from skimage.io import imread

# 比较图片大小
maxValue = 0
index = 0

bigThan0 = 0
smallThan0 = 0

total = 0

sumMore0 = 0
sumLess0 = 0

arr = []

variables=[ "agricultural", "airplane", "baseballdiamond", "beach", "buildings",
            "denseresidential", "forest", "freeway", "golfcourse", "harbor", 
            "intersection", "mediumresidential", "mobilehomepark", "overpass", "parkinglot", 
            "river", "runway", "sparseresidential", "storagetanks", "tenniscourt"]
#variables=["freeway"]

origin_size = []
paramell_size = []
upgrade_rate = []
index_arr = []
def compare_image_size(num,img1_path, img2_path):
  # 1是原始，2是并行
  global maxValue,index,bigThan0,smallThan0,total,sumMore0,sumLess0

  total += 1

  size1 = os.path.getsize(img1_path)
  size2 = os.path.getsize(img2_path)

  ans = (size1-size2) / size1 * 100
  
  if ans > 0:
    bigThan0 += 1
    sumMore0 += ans
    arr.append( round(ans,2) )
  else:
    smallThan0 += 1
    sumLess0 += ans

  maxValue = max(maxValue,ans)
  if maxValue == ans:
    index = num

  ans = round(ans,3)
  #print(f"第{num}张图片,  压缩比例提高:{ans}%")
  return




# 示例使用
for item in variables:
  for num in range(1,100,1):
    img1_path = f"./origin/Images/{item}/{item}{num:02}qq"
    img2_path = f"./parallel/Images/{item}/{item}{num:02}qq"
    compare_image_size(num,img1_path, img2_path)
  print(f"{item}类别,第{index:02}张图片,  压缩比例提高:{round(maxValue,3)}%")
  size1 = os.path.getsize(f"./origin/Images/{item}/{item}{index:02}qq")
  size2 = os.path.getsize(f"./parallel/Images/{item}/{item}{index:02}qq")

  origin_size.append( size1 )
  paramell_size.append( size2 )
  index_arr.append( index )
  rate = (size1 - size2) / size1 * 100
  rate = round(rate,2)
  upgrade_rate.append( str(rate) + '%')
  maxValue = 0
  index = 0


print(f"{bigThan0}张图片压缩提高, 共有{total}张, 占比{bigThan0 / total * 100}%")


print(sumMore0 / bigThan0)
print(sumLess0 / smallThan0)

#print(origin_size)
#print(paramell_size)
#print(upgrade_rate)
#print(index_arr)
# print(arr)