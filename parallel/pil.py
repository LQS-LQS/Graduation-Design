from PIL import Image

# 读取JPEG图像
im = Image.open('D:\\MyCode-Git\\Graduation-Design\\source_2.jpg')

# 保存图像为JPEG格式
im.save('D:\\MyCode-Git\\Graduation-Design\\output2.jpg', quality=100)