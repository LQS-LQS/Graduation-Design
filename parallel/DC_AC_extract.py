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
  quanted_block = np.empty((block_total,8,8), dtype=int) # 临时存储
  for row_index in range(0, padded_matrix.shape[0], 8):  # 步长为8
    for col_index in range(0, padded_matrix.shape[1], 8):
      block = padded_matrix[row_index:row_index+8, col_index:col_index+8]  # 逐个获取padded_matrix的8*8分块矩阵
      
      block_index = row_index // 8 * (padded_matrix.shape[1] // 8) + col_index // 8
      # if(quant_table_type == 'chrom'):
      #   print(block)
      quanted_block[block_index] = quant_block(DCT_2D(block),quant_table_type) # 量化矩阵
      # if( judge_is_empty_block(quanted_block[block_index]) == True):
      #   print(block)
      tmp_array = zigzag_block_to_array(quanted_block[block_index]) # 游格编码后的数组
      dc[block_index] = tmp_array[0] # dc系数
      ac_arrays[block_index]=tmp_array[1:64] # ac系数,每一个ac系数是一个一维数组
  
  for i in range(0,block_total):
    if( judge_is_empty_block(quanted_block[i]) == True):
      buffer[i] = 0
      cnt_empty_block += 1
    else:
      buffer[i] = 1
  
  delete_arr = []
  for i in range(0,block_total):
    if( buffer[i] == 0):
      delete_arr.append(i)

  
  dc_ = np.delete(dc, delete_arr)
  ac_ = np.delete(ac_arrays, delete_arr, axis=0)
  # print("delete_arr:",delete_arr)   #正确
  # print("dc-len:",len(dc[np.arange(dc.size - cnt_empty_block)]),"ac-len:",ac_.shape[0]) #正确
  # print( "oooooooo",dc.shape, ac_arrays.shape)
  # print( buffer )
  # print("dc.size:",dc.size, "cnt_empty_block",cnt_empty_block)
  return  dc_, \
          ac_,  \
          buffer, \
          cnt_empty_block



# def dct_quant_and_extract_DC_AC_from_padded_matrix(padded_matrix,quant_table_type):
#   def sub(i_start, i_end, j_start, j_end):
#     #print("--------------------------------222")
#     t = []
#     for i in range(i_start, i_end, 8):
#       for j in range(j_start, j_end, 8):
#         block = padded_matrix[i:i+8, j:j+8]  # 逐个获取padded_matrix的8*8分块矩阵
#         block_index = i // 8 * (padded_matrix.shape[1] // 8) + j // 8
#         quanted_block[block_index] = quant_block(DCT_2D(block),quant_table_type) # 量化矩阵
#         tmp_array = zigzag_block_to_array(quanted_block[block_index]) # 游格编码后的数组
#         dc[block_index] = tmp_array[0] # dc系数
#         ac_arrays[block_index]=tmp_array[1:64] # ac系数,每一个ac系数是一个一维数组
#   rows, cols = padded_matrix.shape[0], padded_matrix.shape[1]
#   left_rows = int(rows // 8 / 2) * 8
#   left_cols = int(cols // 8 / 2) * 8
#   #print("rows=",rows,"  cols=",cols)
#   cnt_empty_block = 0
#   '''
#     提取ac和dc系数 \n
#       DC系数：对应于u=0，v=0的系数，称做直流分量，即DC系数。 \n
#       AC系数：其余63个系数称做AC系数，即交流分量 \n
#     返回值: dc数组 和 ac数组
#   '''
#   block_total = int( padded_matrix.size/64 ) # 8*8的矩阵块数
#   dc = np.empty( block_total, dtype=int ) # dc系数, 大小为 block_total*1
#   buffer = np.empty( block_total, dtype=int )
#   ac_arrays = np.empty((block_total,63),dtype=int) # ac系数, 大小为 block_total*63
#   tmp_array = np.empty(64,dtype=int)
#   quanted_block = np.empty((block_total,8,8), dtype=int) # 临时存储
#   # sub(0, left_rows, 0, left_cols)
#   # sub(0, left_rows, left_cols, cols)
#   # sub(left_rows, rows, 0, left_cols)
#   # sub(left_rows, rows, left_cols, cols)
#   #print("------111")
#   with concurrent.futures.ProcessPoolExecutor() as pool:
#     pool.submit(sub, 0, left_rows, 0, left_cols)
#     pool.submit(sub, 0, left_rows, left_cols, cols)
#     pool.submit(sub, left_rows, rows, 0, left_cols)
#     pool.submit(sub, left_rows, rows, left_cols, cols)
#   for i in range(0,block_total):
#     if( judge_is_empty_block(quanted_block[i]) == True):
#       buffer[i] = 0
#       cnt_empty_block += 1
#     else:
#       buffer[i] = 1
  
#   delete_arr = []
#   for i in range(0,block_total):
#     if( buffer[i] == 0):
#       delete_arr.append(i)

#   dc_ = np.delete(dc, delete_arr)
#   ac_ = np.delete(ac_arrays, delete_arr, axis=0)
#   # print("delete_arr:",delete_arr)   #正确
#   # print("dc-len:",len(dc[np.arange(dc.size - cnt_empty_block)]),"ac-len:",ac_.shape[0]) #正确
#   # print( "oooooooo",dc.shape, ac_arrays.shape)
#   # print( buffer )
#   # print("dc.size:",dc.size, "cnt_empty_block",cnt_empty_block)
#   return  dc_, \
#           ac_,  \
#           buffer, \
#           cnt_empty_block




# def sub(i_start, i_end, j_start, j_end, quant_table_type, padded_matrix, quanted_block, dc, ac_arrays):
#     print("--------------------------------222")
#     print(dc)
#     for i in range(i_start, i_end, 8):
#       for j in range(j_start, j_end, 8):
#         block = padded_matrix[i:i+8, j:j+8]  # 逐个获取padded_matrix的8*8分块矩阵
#         block_index = i // 8 * (padded_matrix.shape[1] // 8) + j // 8
#         quanted_block[block_index] = quant_block(DCT_2D(block),quant_table_type) # 量化矩阵
#         tmp_array = zigzag_block_to_array(quanted_block[block_index]) # 游格编码后的数组
#         dc[block_index] = tmp_array[0] # dc系数
#         ac_arrays[block_index]=tmp_array[1:64] # ac系数,每一个ac系数是一个一维数组

# def dct_quant_and_extract_DC_AC_from_padded_matrix(padded_matrix,quant_table_type):
#   rows, cols = padded_matrix.shape[0], padded_matrix.shape[1]
#   left_rows = int(rows // 8 / 2) * 8
#   left_cols = int(cols // 8 / 2) * 8
#   #print("rows=",rows,"  cols=",cols)
#   cnt_empty_block = 0
#   '''
#     提取ac和dc系数 \n
#       DC系数：对应于u=0，v=0的系数，称做直流分量，即DC系数。 \n
#       AC系数：其余63个系数称做AC系数，即交流分量 \n
#     返回值: dc数组 和 ac数组
#   '''
#   block_total = int( padded_matrix.size/64 ) # 8*8的矩阵块数
#   dc = np.empty( block_total, dtype=int ) # dc系数, 大小为 block_total*1
#   buffer = np.empty( block_total, dtype=int )
#   ac_arrays = np.empty((block_total,63),dtype=int) # ac系数, 大小为 block_total*63
#   tmp_array = np.empty(64,dtype=int)
#   quanted_block = np.empty((block_total,8,8), dtype=int) # 临时存储
#   # sub(0, left_rows, 0, left_cols)
#   # sub(0, left_rows, left_cols, cols)
#   # sub(left_rows, rows, 0, left_cols)
#   # sub(left_rows, rows, left_cols, cols)
#   #print("------111")
#   with concurrent.futures.ProcessPoolExecutor() as pool:
#     pool.submit(sub, 0, left_rows, 0, left_cols, quant_table_type,  padded_matrix, quanted_block, dc, ac_arrays)
#     pool.submit(sub, 0, left_rows, left_cols, cols, quant_table_type, padded_matrix, quanted_block, dc, ac_arrays)
#     pool.submit(sub, left_rows, rows, 0, left_cols, quant_table_type, padded_matrix, quanted_block, dc, ac_arrays)
#     pool.submit(sub, left_rows, rows, left_cols, cols, quant_table_type, padded_matrix, quanted_block, dc, ac_arrays)
#   for i in range(0,block_total):
#     if( judge_is_empty_block(quanted_block[i]) == True):
#       buffer[i] = 0
#       cnt_empty_block += 1
#     else:
#       buffer[i] = 1
  
#   delete_arr = []
#   for i in range(0,block_total):
#     if( buffer[i] == 0):
#       delete_arr.append(i)

#   dc_ = np.delete(dc, delete_arr)
#   ac_ = np.delete(ac_arrays, delete_arr, axis=0)
#   return  dc_, \
#           ac_,  \
#           buffer, \
#           cnt_empty_block








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






# def sub(i_start, i_end, j_start, j_end, quant_table_type, padded_matrix, quanted_block, dc, ac_arrays):
#     #print("--------------------------------222")
#     #print(dc[:])
#     for i in range(i_start, i_end, 8):
#       for j in range(j_start, j_end, 8):
#         block = padded_matrix[i:i+8, j:j+8]  # 逐个获取padded_matrix的8*8分块矩阵
#         block_index = i // 8 * (padded_matrix.shape[1] // 8) + j // 8
#         #print(block_index)
#         quanted_block[block_index] = quant_block(DCT_2D(block),quant_table_type) # 量化矩阵
#         tmp_array = zigzag_block_to_array(quanted_block[block_index]) # 游格编码后的数组
#         dc[block_index] = tmp_array[0] # dc系数
#         ac_arrays[block_index]=tmp_array[1:64] # ac系数,每一个ac系数是一个一维数组

# def dct_quant_and_extract_DC_AC_from_padded_matrix(padded_matrix,quant_table_type):
#   def sub(i_start, i_end, j_start, j_end):
#     for i in range(i_start, i_end, 8):
#       for j in range(j_start, j_end, 8):
#         block = padded_matrix[i:i+8, j:j+8]  # 逐个获取padded_matrix的8*8分块矩阵
#         block_index = i // 8 * (padded_matrix.shape[1] // 8) + j // 8
#         quanted_block[block_index] = quant_block(DCT_2D(block),quant_table_type) # 量化矩阵
#         tmp_array = zigzag_block_to_array(quanted_block[block_index]) # 游格编码后的数组
#         dc[block_index] = tmp_array[0] # dc系数
#         ac_arrays[block_index]=tmp_array[1:64] # ac系数,每一个ac系数是一个一维数组
#   #print("-----------------------")  
#   manager = Manager()
#   rows, cols = padded_matrix.shape[0], padded_matrix.shape[1]
#   left_rows = int(rows // 8 / 2) * 8
#   left_cols = int(cols // 8 / 2) * 8
#   #print("rows=",rows,"  cols=",cols)
#   cnt_empty_block = 0
#   '''
#     提取ac和dc系数 \n
#       DC系数：对应于u=0，v=0的系数，称做直流分量，即DC系数。 \n
#       AC系数：其余63个系数称做AC系数，即交流分量 \n
#     返回值: dc数组 和 ac数组
#   '''
#   block_total = int( padded_matrix.size/64 ) # 8*8的矩阵块数
#   #dc = manager.list([None] * block_total) # 将共享内存对象转换为NumPy数组 #np.empty( block_total, dtype=int ) 
#   dc = np.empty( block_total, dtype=int ) # dc系数, 大小为 block_total*1
#   buffer = np.empty( block_total, dtype=int )
#   #ac_arrays = manager.list([None] * block_total)# 将共享内存对象转换为NumPy数组
#   ac_arrays = np.empty((block_total,63),dtype=int) # ac系数, 大小为 block_total*63
#   tmp_array = np.empty(64,dtype=int)
#   #quanted_block = manager.list([None] * block_total)
#   quanted_block = np.empty((block_total,8,8), dtype=int) # 临时存储
#   # sub(0, left_rows, 0, left_cols)
#   # sub(0, left_rows, left_cols, cols)
#   # sub(left_rows, rows, 0, left_cols)
#   # sub(left_rows, rows, left_cols, cols)
#   #print("------111")
#   with concurrent.futures.ThreadPoolExecutor() as pool:
#     pool.submit(sub, 0, left_rows, 0, left_cols)
#     pool.submit(sub, 0, left_rows, left_cols, cols)
#     pool.submit(sub, left_rows, rows, 0, left_cols)
#     pool.submit(sub, left_rows, rows, left_cols, cols)
#   # p1 = Process(target=sub, args=(0, left_rows, 0, left_cols, quant_table_type,  padded_matrix, quanted_block, dc, ac_arrays,))
#   # p2 = Process(target=sub, args=(0, left_rows, left_cols, cols, quant_table_type, padded_matrix, quanted_block, dc, ac_arrays))
#   # p3 = Process(target=sub, args=(left_rows, rows, 0, left_cols, quant_table_type, padded_matrix, quanted_block, dc, ac_arrays))
#   # p4 = Process(target=sub, args=(left_rows, rows, left_cols, cols, quant_table_type, padded_matrix, quanted_block, dc, ac_arrays))
  
#   # p1.start()
#   # p2.start()
#   # p3.start()
#   # p4.start()
#   # p1.join()
#   # p2.join()
#   # p3.join()
#   # p4.join()
#   for i in range(0,block_total):
#     if( judge_is_empty_block(quanted_block[i]) == True):
#       buffer[i] = 0
#       cnt_empty_block += 1
#     else:
#       buffer[i] = 1
  
#   delete_arr = []
#   for i in range(0,block_total):
#     if( buffer[i] == 0):
#       delete_arr.append(i)

#   dc_ = np.delete(dc, delete_arr)
#   ac_ = np.delete(ac_arrays, delete_arr, axis=0)
#   return  dc_, \
#           ac_,  \
#           buffer, \
#           cnt_empty_block