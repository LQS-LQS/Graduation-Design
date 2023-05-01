import numpy as np 
from DCT_quant import *
from padding_image import *
from zigzag import *

def judge_is_empty_block( block ):
  for i in range(block.shape[0]):
    for j in range (block.shape[1]):
      if(block[i][j] != 0):  
        return False
  return True

def block_generator(padded_matrix):
  '''
    入参: 大矩阵
    函数功能: 返回划分后的8*8的矩阵块
    返回形式: [ { 矩阵块行数, 矩阵块列数, 8*8矩阵块, 矩阵块第几块 }]
  '''
  block = np.empty( (8,8), dtype=int) # 产生一个8*8的空矩阵
  block_index = -1
  for block_row_index in range( 0, padded_matrix.shape[0], 8): # 步长为8
    for block_col_index in range( 0, padded_matrix.shape[1], 8):
      block = padded_matrix[block_row_index:block_row_index+8, block_col_index:block_col_index+8] # 逐个获取padded_matrix的8*8分块矩阵
      block_index += 1
      yield (block_row_index, block_col_index, block ,block_index) # yield是干什么的？？


def dct_quant_and_extract_DC_AC_from_padded_matrix(padded_matrix,quant_table_type):
  cnt_empty_block = 0
  '''
    提取ac和dc系数 \n
      DC系数：对应于u=0，v=0的系数，称做直流分量，即DC系数。 \n
      AC系数：其余63个系数称做AC系数，即交流分量 \n
    返回值: dc数组 和 ac数组
  '''
  block_total = int( padded_matrix.size/64 ) # 8*8的矩阵块数
  dc = np.empty( block_total, dtype=int ) # dc系数, 大小为 block_total*1
  buffer = np.empty( block_total, dtype=int )
  ac_arrays = np.empty((block_total,63),dtype=int) # ac系数, 大小为 block_total*63
  tmp_array = np.empty(64,dtype=int)

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
  
  # 过滤掉零矩阵
  delete_arr = []
  for i in range(1,cnt_empty_block+1):
    delete_arr.append( ac_arrays.shape[0] - i)

  ac_ = np.delete(ac_arrays, delete_arr, axis=0)
  # print("delete_arr:",delete_arr)   #正确
  # print("dc-len:",len(dc[np.arange(dc.size - cnt_empty_block)]),"ac-len:",ac_.shape[0]) #正确
  # print( "oooooooo",dc.shape, ac_arrays.shape)
  # print( buffer )
  # print("dc.size:",dc.size, "cnt_empty_block",cnt_empty_block)
  return  dc[np.arange(dc.size - cnt_empty_block)], \
          ac_,  \
          buffer, \
          cnt_empty_block

def restore_padded_matrix_from_DC_AC(dc,ac_arrays,block_row_total, block_col_total, buffer, quant_table_type ):
  # print("dc:",dc.shape[0],"ac:",ac_arrays.shape[0])
  # print(len(buffer))
  '''
    根据dc系数和ac系数还原原始8*8矩阵
  '''
  restored_matrix = np.empty((8*block_row_total,8*block_col_total),dtype=int)
  tmp_block = np.empty((8,8),dtype=int)
  cnt_empty_block = 0

  if( quant_table_type == 'lum'): #cb or cr
    for row in range(0, block_row_total):
      for col in range(0, block_col_total):
        block_index = row*block_col_total + col # 第几个8*8块
        tmp_block = zigzag_array_to_block( np.concatenate((dc[block_index:block_index+1],ac_arrays[block_index])) ) # 将dc系数和ac系数合并 将这个数组逆zigzag变换,变成8*8的数组
        aaa = dequant_block(tmp_block,quant_table_type)
        restored_matrix[row*8:row*8+8,col*8:col*8+8] = iDCT_2D(aaa)
  else:
    for row in range(0, block_row_total):
      for col in range(0, block_col_total):
        block_index = row*block_col_total + col # 第几个8*8块
        if( buffer[block_index] == 0):
          tmp_block = zigzag_array_to_block( np.concatenate((np.array([0],dtype=int),np.zeros(63,dtype=int))) )
          cnt_empty_block += 1
        else:
          #print(dc[block_index-cnt_empty_block:block_index+1-cnt_empty_block])
          #print(ac_arrays[block_index-cnt_empty_block])
          tmp_block = zigzag_array_to_block( np.concatenate((dc[block_index-cnt_empty_block:block_index+1-cnt_empty_block],ac_arrays[block_index-cnt_empty_block])) ) # 将dc系数和ac系数合并 将这个数组逆zigzag变换,变成8*8的数组
        aaa = dequant_block(tmp_block,quant_table_type)
        restored_matrix[row*8:row*8+8,col*8:col*8+8] = iDCT_2D(aaa)


  return restored_matrix
