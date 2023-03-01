from PIL import Image
import numpy as np
from DCT_quant import *
from zigzag import *
import math

def martix_padding(npmat):
  '''
    函数功能: 返回一个填充后的矩阵, 使得行数和列数为8的倍数
  '''
  # 传进来的npmay包括原始的Y,subsample过的Cb,Cr矩阵
  rows = npmat.shape[0] # 获取行数
  rows_pad = math.ceil( rows/8 ) * 8

  cols = npmat.shape[1] # 获取列数
  cols_pad = math.ceil( cols/8 ) * 8


  mat_append_col = np.broadcast_to( npmat[:,-1][:,None], (npmat.shape[0],cols_pad - npmat.shape[1]) ) # 要填充的元素
  mat_padded_col = np.hstack( (npmat,mat_append_col) ) # 此时 矩阵的列数满足8的倍数

  mat_append_row = np.broadcast_to(mat_padded_col[-1,:],(rows_pad - mat_padded_col.shape[0],cols_pad)) # 要填充的元素
  mat_padded_row = np.vstack((mat_padded_col,mat_append_row)) # 此时 矩阵的行数也满足8的倍数

  mat_pad = mat_padded_row

  return mat_pad

def restore_img_from_padding(Y_padded,Cb_padded,Cr_padded,rows_origin,cols_origin):
  # 传进来的都是None,None,None
  '''
    从填充的Y、Cb、Cr分量数组中恢复出原始图像的操作
  '''
  '''
  np.repeat(3, 4)
  array([3, 3, 3, 3])
  >>> x = np.array([ [1,2],[3,4] ])
  >>> np.repeat(x, 2) # 默认axis=None  
  array([1, 1, 2, 2, 3, 3, 4, 4]) # ?? 降低维数 ?? 
  >>> np.repeat(x, 3, axis=1) #  ?? axis=1不降低维数
  array([[1, 1, 1, 2, 2, 2],
      [3, 3, 3, 4, 4, 4]])
  >>> np.repeat(x, [1, 2], axis=0)
  array([ [1, 2],
          [3, 4],
          [3, 4]])
  
  '''
  ## Cb_restored = np.repeat((np.repeat(Cb_padded,2,axis=1)),2,axis=0)
  
  Cb_restored = np.repeat((np.repeat(Cb_padded,2,axis=1)),2,axis=0)  ## 第一个axis有问题
  Cr_restored = np.repeat((np.repeat(Cr_padded,2,axis=1)),2,axis=0)
  npmat_restored = np.empty( [rows_origin,cols_origin,3], dtype=np.uint8)
  npmat_restored[:,:,0] = Y_padded[   :rows_origin, :cols_origin]
  npmat_restored[:,:,1] = Cb_restored[:rows_origin, :cols_origin]
  npmat_restored[:,:,2] = Cr_restored[:rows_origin, :cols_origin]
  

  '''
  print(Y_padded,Cb_padded,Cr_padded)
  npmat_restored = np.empty( [rows_origin,cols_origin,3], dtype=np.uint8)
  npmat_restored[:,:,0] = Y_padded[   :rows_origin, :cols_origin]
  npmat_restored[:,:,1] = Cb_padded[:rows_origin, :cols_origin]
  npmat_restored[:,:,2] = Cr_padded[:rows_origin, :cols_origin]
  '''

  return npmat_restored

