from PIL import Image
import os
from skimage import measure
from skimage.io import imread

# 比较图片大小

bigThan0 = 0
smallThan0 = 0

total = 0

sumMore0 = 0
sumLess0 = 0

upgrade_rate = []

origin_size = []
paramell_size = []
rate_arr = []
index_arr = []

def compare_image_size(num,img1_path, img2_path):
  # 1是原始，2是并行
  global bigThan0,smallThan0,total,sumMore0,sumLess0

  total += 1
  try:
    size1 = os.path.getsize(img1_path)
    size2 = os.path.getsize(img2_path)
  except:
    return 0
  ans = (size1-size2) / size1 * 100
  
  if ans > 0:
    bigThan0 += 1
    sumMore0 += ans
  else:
    smallThan0 += 1
    sumLess0 += ans
  ans = round(ans,3)
  #print(f"第{num}张图片,  压缩比例提高:{ans}%")
  return ans




# 示例使用
for num in range(1,1339,1):
  img1_path = f"./origin/UCID1338/{num}"
  img2_path = f"./parallel/UCID1338/{num}"
  try:
    size1 = os.path.getsize(img1_path)
    size2 = os.path.getsize(img2_path)
  except:
    continue
  rate = compare_image_size(num,img1_path, img2_path)
  upgrade_rate.append( {
    'rate':rate,
    'ori_size':size1,
    'opt_size':size2,
    'num':num,
  } )





# print(origin_size)
# print(paramell_size)
# print(upgrade_rate)
# print(index_arr)
# print(arr)

#print(upgrade_rate)

upgrade_rate.sort(key=lambda x:x['rate'], reverse=True)
print( upgrade_rate[0:20])

new_arr = upgrade_rate[0:20]


for i in range(0, len(new_arr)):
  dic = new_arr[i]
  origin_size.append( dic['ori_size'] )
  paramell_size.append( dic['opt_size'] )
  rate_arr.append( dic['rate'] )
  index_arr.append( dic['num'] )



#print( 'origin_size', origin_size )
#print( 'paramell_size', paramell_size)
#print( 'rate_arr', rate_arr)
#print( 'index_arr', index_arr)
print(f"{bigThan0}张图片压缩提高, 共有{total}张, 占比{bigThan0 / total * 100}%")

print("平均压缩率为:", sumMore0 / bigThan0)
print( sumLess0 / smallThan0) 