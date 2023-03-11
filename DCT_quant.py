import numpy as np
from scipy import fftpack

'''
  Y_padded Cb_padded Cr_padded
'''

def DCT_2D(block):
  '''
    传入8*8的矩阵 \n
    返回DCT变换后的矩阵 \n
  '''
  # dct参数见 https://vimsky.com/zh-tw/examples/usage/python-scipy.fftpack.dct.html
  # scipy.fftpack.dct(x, type=2, n=None, axis=- 1, norm=None, overwrite_x=False)
  # .先将block转置,然后计算dct,结果转置后再次计算dct,相当于计算block本身   两次转置是为了支持格式问题
  # 先对每一行做dct,然后再对列做dct,减少运算时间
  DCT_matrix = fftpack.dct( fftpack.dct(block.T, norm='ortho').T, norm='ortho' )
  return DCT_matrix

def iDCT_2D(DCT_block):
  '''
    DCT逆变换 \n
    传入DCT矩阵 \n
    返回逆变换之后的矩阵
  '''
  block = fftpack.idct(fftpack.idct(DCT_block.T,norm='ortho').T,norm='ortho')
  return block

def get_quantization_table(type):
  '''
    返回jpeg标准量化表
  '''
  if(type == 'lum'): # 亮度量化表
    table = np.array(
      [ [16, 11, 10, 16, 24,	40,	 51,	61],
        [12, 12, 14, 19, 26,	58,	 60,	55],
        [14, 13, 16, 24, 40,	57,	 69,	56],
        [14, 17, 22, 29, 51,	87,	 80,	62],
        [18, 22, 37, 56, 68,	109, 103, 77],
        [24, 35, 55, 64, 81,	104, 113, 92],
        [49, 64, 78, 87, 103, 121, 120, 101],
        [72, 92, 95, 98, 112, 100, 103, 99] ]
    )
  elif(type == 'chrom'): #Cb Cr量化表
    table = np.array(
      [ [17, 18, 24, 47, 99, 99, 99, 99],
        [18, 21, 26, 66, 99, 99, 99, 99],
        [24, 26, 56, 99, 99, 99, 99, 99],
        [47, 66, 99, 99, 99, 99, 99, 99],
        [99, 99, 99, 99, 99, 99, 99, 99],
        [99, 99, 99, 99, 99, 99, 99, 99],
        [99, 99, 99, 99, 99, 99, 99, 99],
        [99, 99, 99, 99, 99, 99, 99, 99] ]
    )
  return table

def quant_block(block, type):
  '''
    返回量化后的矩阵
  '''
  quant_table = get_quantization_table(type) # 得到量化表
  quanted_block = np.round(np.divide(block, quant_table)).astype(int)
  return quanted_block

def dequant_block(block, type):
  '''
    返回反量化后的矩阵
  '''
  
  quant_table = get_quantization_table(type) # 得到量化表
  dequanted_block = block*quant_table.astype(np.int32) # 对应分量相乘,然后取整
  return dequanted_block

