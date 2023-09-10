# 毕业设计——jpeg算法优化

环境

```
apt-get install build-essential
apt-get install gfortran
pip install scipy==1.4.1
```



`origin目录` : 基础算法 

`optimize目录` : 优化算法

执行`origin目录`下的`encoder_decoder_test.bash`可以将`testImages`所有图片进行压缩

执行根目录下的size_compare.py可以看到压缩优化结果
```txt
第1张图片,  压缩比例:-0.192%
第2张图片,  压缩比例:-0.19%
第3张图片,  压缩比例:-0.19%
第4张图片,  压缩比例:-0.343%
第5张图片,  压缩比例:-0.18%
第6张图片,  压缩比例:0.499%
第7张图片,  压缩比例:-0.16%
第8张图片,  压缩比例:-0.259%
第9张图片,  压缩比例:-0.119%
第10张图片,  压缩比例:-0.217%
第11张图片,  压缩比例:-0.231%
第12张图片,  压缩比例:0.429%
第13张图片,  压缩比例:-0.238%
第14张图片,  压缩比例:-0.196%
第15张图片,  压缩比例:-0.142%
第16张图片,  压缩比例:-0.104%
第17张图片,  压缩比例:1.763%
第18张图片,  压缩比例:2.698%
第19张图片,  压缩比例:-0.215%
```



## 增加judge函数

对于Y分量，不需要进行空块判断

对于Cb、Cr分量，进行空块判断

Cb、Cr会有ac、dc两个系数，由于判断的是空块，也就是64个分量，因此无需单独建立buffer，Cb、Cr分量分别建立一个Buffer

```python
def judge_is_empty_block( block ):
  for i in range(block.shape[0]):
    for j in range (block.shape[1]):
      if(block[i][j] != 0):  
        return False
  return True
```

对于每一个块判断是否为空块




数据集里找图片
jpeg库(作为baseline)->计算MSE和PSNR值
串行->并行


optimize的执行时间

```python
for( block_row_index, block_col_index, block, block_index ) in block_generator(padded_matrix):
    quanted_block = quant_block(DCT_2D(block),quant_table_type) # 量化矩阵
    if( judge_is_empty_block(quanted_block) == True):
      buffer[block_index] = 0
      cnt_empty_block += 1
      continue
    else:
      buffer[block_index] = 1
      tmp_array = zigzag_block_to_array(quanted_block) # 游格编码后的数组
      dc[block_index - cnt_empty_block] = tmp_array[0] # dc系数
      ac_arrays[block_index - cnt_empty_block]=tmp_array[1:64] # ac系数,每一个ac系数是一个一维数组
```

修改后:
```python
  for( block_row_index, block_col_index, block, block_index ) in block_generator(padded_matrix):
    quanted_block[block_index] = quant_block(DCT_2D(block),quant_table_type) # 量化矩阵
    tmp_array = zigzag_block_to_array(quanted_block[block_index]) # 游格编码后的数组
    dc[block_index - cnt_empty_block] = tmp_array[0] # dc系数
    ac_arrays[block_index - cnt_empty_block]=tmp_array[1:64] # ac系数,每一个ac系数是一个一维数组
  

  for i in range(0,block_total):
    if( judge_is_empty_block(quanted_block[i]) == True):
      buffer[i] = 0
      cnt_empty_block += 1
    else:
      buffer[i] = 1

```

因为需要并行,而之前的代码中存在`block_index - cnt_empty_block`, `cnt_empty_block`表示前面所有空块的数量,后面的数据受到前面的影响,因此无法并行
因此修改为两次`O(n)`的计算,在delete_arr记录空块的下标,这样就可以将运算量大的第一部分执行并行


quantTime时间最长，占总时间的40%-60%

dct_quant_and_extract_DC_AC_from_padded_matrix优化这个函数非常有意义



```
UCID数据集

agricultural类别,			第97张图片,  压缩比例提高:1.541%
airplane类别,					第25张图片,  压缩比例提高:0.638%
baseballdiamond类别,	第90张图片,  压缩比例提高:0.725%
beach类别,						第72张图片,  压缩比例提高:1.206%
buildings类别,				第86张图片,  压缩比例提高:1.545%
denseresidential类别,	第86张图片,  压缩比例提高:0.757%
forest类别,						第07张图片,  压缩比例提高:1.247%
freeway类别,					第25张图片,  压缩比例提高:0.802%
golfcourse类别,				第30张图片,  压缩比例提高:0.398%
harbor类别,						第63张图片,  压缩比例提高:0.655%
intersection类别,			第75张图片,  压缩比例提高:1.359%
mediumresidential类别,第01张图片,  压缩比例提高:0.691%
mobilehomepark类别,		第19张图片,  压缩比例提高:0.784%
overpass类别,					第35张图片,  压缩比例提高:0.978%
parkinglot类别,				第99张图片,  压缩比例提高:0.959%
river类别,						第76张图片,  压缩比例提高:1.988%
runway类别,						第97张图片,  压缩比例提高:1.228%
sparseresidential类别,第49张图片,  压缩比例提高:0.566%
storagetanks类别,			第62张图片,  压缩比例提高:1.627%
tenniscourt类别,			第47张图片,  压缩比例提高:0.933%
1200张图片压缩提高, 共有1980张, 占比60.60606060606061%


ttotal_MSE: [35.4, 43.6, 18.3, 37.4, 32.9, 49.0, 31.1, 44.2, 37.0, 47.8, 31.5, 41.9, 57.5, 27.3, 51.3, 13.7, 34.8, 31.4, 49.3, 32.7]
total_MSE_2000: [31.1, 19.3, 10.4, 11.7, 8.1, 18.2, 28.4, 27.3, 28.9, 28.8, 17.0, 33.5, 30.5, 11.9, 31.9, 7.6, 24.2, 13.6, 9.0, 17.1]
total_PSNR: [32.6, 31.7, 35.5, 32.4, 33.0, 31.2, 33.2, 31.7, 32.4, 31.3, 33.1, 31.9, 30.5, 33.8, 31.0, 36.8, 32.7, 33.2, 31.2, 33.0]
total_PSNR_2000: [33.2, 35.3, 38.0, 37.4, 39.0, 35.5, 33.6, 33.8, 33.5, 33.5, 35.8, 32.9, 33.3, 37.4, 33.1, 39.3, 34.3, 36.8, 38.6, 35.8]
total_SSIM: [0.95, 0.91, 0.9, 0.93, 0.94, 0.93, 0.87, 0.9, 0.84, 0.95, 0.94, 0.9, 0.94, 0.95, 0.95, 0.95, 0.84, 0.93, 0.95, 0.92]
total_SSIM_2000: [0.95, 0.92, 0.91, 0.93, 0.96, 0.96, 0.88, 0.91, 0.85, 0.97, 0.95, 0.92, 0.96, 0.97, 0.95, 0.95, 0.85, 0.94, 0.97, 0.93]

['pic1', 'pic2', 'pic3', 'pic4', 'pic5', 'pic6', 'pic7', 'pic8', 'pic9', 'pic10', 'pic11', 'pic12', 'pic13', 'pic14', 'pic15', 'pic16', 'pic17', 'pic18', 'pic19', 'pic20', 'pic21', 'pic22',
'pic23', 'pic24', 'pic25', 'pic26', 'pic27', 'pic28', 'pic29', 'pic30']
```



```
UCID1338数据集

origin_size [26490, 20881, 19734, 29169, 26975, 13753, 25365, 32751, 13687, 27050, 35370, 32330, 32128, 37332, 34441, 28862, 25780, 25011, 19795, 27814]
paramell_size [25517, 20237, 19153, 28339, 26210, 13373, 24670, 31871, 13320, 26336, 34444, 31485, 31329, 36407, 33607, 28173, 25173, 24434, 19340, 27177]
rate_arr [3.673, 3.084, 2.944, 2.845, 2.836, 2.763, 2.74, 2.687, 2.681, 2.64, 2.618, 2.614, 2.487, 2.478, 2.422, 2.387, 2.355, 2.307, 2.299, 2.29]
index_arr [282, 1162, 543, 574, 500, 1060, 562, 430, 1059, 146, 334, 731, 445, 280, 330, 1155, 545, 541, 1160, 557]
1335张图片压缩提高, 共有1337张, 占比99.85041136873598%
平均压缩率为: 0.8626989787218112

[,1059 , , , , , , , , , , 

total_MSE: [29.4, 44.8, 29.7, 60.7, 45.1, 57.8, 45.9, 55.6, 56.2, 61.7, 49.1, 50.6, 58.9, 47.0, 55.4, 50.5, 43.7, 41.4, 53.5, 48.5]
total_MSE_2000: [10.5, 9.5, 6.1, 10.0, 8.3, 4.0, 8.7, 14.1, 3.9, 20.2, 12.9, 9.9, 12.0, 13.4, 11.7, 10.6, 8.9, 9.0, 8.6, 10.1]
total_PSNR: [33.4, 31.6, 33.4, 30.3, 31.6, 30.5, 31.5, 30.7, 30.6, 30.2, 31.2, 31.1, 30.4, 31.4, 30.7, 31.1, 31.7, 32.0, 30.8, 31.3]
total_PSNR_2000: [37.9, 38.3, 40.3, 38.2, 38.9, 42.2, 38.7, 36.6, 42.2, 35.1, 37.0, 38.2, 37.3, 36.9, 37.4, 37.9, 38.6, 38.6, 38.8, 38.1]
total_SSIM: [0.94, 0.94, 0.92, 0.91, 0.94, 0.92, 0.92, 0.84, 0.93, 0.84, 0.94, 0.9, 0.91, 0.91, 0.95, 0.92, 0.93, 0.93, 0.94, 0.93]
total_SSIM_2000: [0.95, 0.95, 0.95, 0.95, 0.95, 0.96, 0.95, 0.95, 0.97, 0.85, 0.95, 0.96, 0.95, 0.92, 0.96, 0.95, 0.95, 0.95, 0.96, 0.95]
```



```
```

