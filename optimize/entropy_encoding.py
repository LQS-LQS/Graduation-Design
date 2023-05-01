import numpy as np
from bitstring import BitArray
from DC_AC_extract import *
from bitarray import *
import sys

# dc分量,亮度的哈夫曼表
# 见pdf 这里的01234是位数的意思
'''
  dc差分编码后一个值是-8,则表示为1010111
  8的二进制是1000,经过decompose_int_to_size_value函数返回了4和0111
  然后4的哈夫曼是101
  所以 -8就变味了1010111
'''
huffman_table_DC = {
    '0':bitarray('00'),
    '1':bitarray('010'),
    '2':bitarray('011'),
    '3':bitarray('100'),
    '4':bitarray('101'),
    '5':bitarray('110'),
    '6':bitarray('1110'),
    '7':bitarray('11110'),
    '8':bitarray('111110'),
    '9':bitarray('1111110'),
    'a':bitarray('11111110'),
    'b':bitarray('111111110')
}
# ac分量,Cb和Cr的哈夫曼表
huffman_table_AC = {
    (0,0): bitarray('1010'),
    (0,1): bitarray('00'),
    (0,2): bitarray('01'),
    (0,3): bitarray('100'),
    (0,4): bitarray('1011'),
    (0,5): bitarray('11010'),
    (0,6): bitarray('1111000'),
    (0,7): bitarray('11111000'),
    (0,8): bitarray('1111110110'),
    (0,9): bitarray('1111111110000010'),
    (0,10):bitarray('1111111110000011'),

    (1,1): bitarray('1100'),
    (1,2): bitarray('11011'),
    (1,3): bitarray('1111001'),
    (1,4): bitarray('111110110'),
    (1,5): bitarray('11111110110'),
    (1,6): bitarray('1111111110000100'),
    (1,7): bitarray('1111111110000101'),
    (1,8): bitarray('1111111110000110'),
    (1,9): bitarray('1111111110000111'),
    (1,10):bitarray('1111111110001000'),

    (2,1): bitarray('11100'),
    (2,2): bitarray('11111001'),
    (2,3): bitarray('1111110111'),
    (2,4): bitarray('111111110100'),
    (2,5): bitarray('1111111110001001'),
    (2,6): bitarray('1111111110001010'),
    (2,7): bitarray('1111111110001011'),
    (2,8): bitarray('1111111110001100'),
    (2,9): bitarray('1111111110001101'),
    (2,10):bitarray('1111111110001110'),

    (3,1): bitarray('111010'),
    (3,2): bitarray('111110111'),
    (3,3): bitarray('111111110101'),
    (3,4): bitarray('1111111110001111'),
    (3,5): bitarray('1111111110010000'),
    (3,6): bitarray('1111111110010001'),
    (3,7): bitarray('1111111110010010'),
    (3,8): bitarray('1111111110010011'),
    (3,9): bitarray('1111111110010100'),
    (3,10):bitarray('1111111110010101'),

    (4,1): bitarray('111011'),
    (4,2): bitarray('1111111000'),
    (4,3): bitarray('1111111110010110'),
    (4,4): bitarray('1111111110010111'),
    (4,5): bitarray('1111111110011000'),
    (4,6): bitarray('1111111110011001'),
    (4,7): bitarray('1111111110011010'),
    (4,8): bitarray('1111111110011011'),
    (4,9): bitarray('1111111110011100'),
    (4,10):bitarray('1111111110011101'),

    (5,1): bitarray('1111010'),
    (5,2): bitarray('11111110111'),
    (5,3): bitarray('1111111110011110'),
    (5,4): bitarray('1111111110011111'),
    (5,5): bitarray('1111111110100000'),
    (5,6): bitarray('1111111110100001'),
    (5,7): bitarray('1111111110100010'),
    (5,8): bitarray('1111111110100011'),
    (5,9): bitarray('1111111110100100'),
    (5,10):bitarray('1111111110100101'),

    (6,1): bitarray('1111011'),
    (6,2): bitarray('111111110110'),
    (6,3): bitarray('1111111110100110'),
    (6,4): bitarray('1111111110100111'),
    (6,5): bitarray('1111111110101000'),
    (6,6): bitarray('1111111110101001'),
    (6,7): bitarray('1111111110101010'),
    (6,8): bitarray('1111111110101011'),
    (6,9): bitarray('1111111110101100'),
    (6,10):bitarray('1111111110101101'),

    (7,1): bitarray('11111010'),
    (7,2): bitarray('111111110111'),
    (7,3): bitarray('1111111110101110'),
    (7,4): bitarray('1111111110101111'),
    (7,5): bitarray('1111111110110000'),
    (7,6): bitarray('1111111110110001'),
    (7,7): bitarray('1111111110110010'),
    (7,8): bitarray('1111111110110011'),
    (7,9): bitarray('1111111110110100'),
    (7,10):bitarray('1111111110110101'),

    (8,1): bitarray('111111000'),
    (8,2): bitarray('111111111000000'),
    (8,3): bitarray('1111111110110110'),
    (8,4): bitarray('1111111110110111'),
    (8,5): bitarray('1111111110111000'),
    (8,6): bitarray('1111111110111001'),
    (8,7): bitarray('1111111110111010'),
    (8,8): bitarray('1111111110111011'),
    (8,9): bitarray('1111111110111100'),
    (8,10):bitarray('1111111110111101'),

    (9,1): bitarray('111111001'),
    (9,2): bitarray('1111111110111110'),
    (9,3): bitarray('1111111110111111'),
    (9,4): bitarray('1111111111000000'),
    (9,5): bitarray('1111111111000001'),
    (9,6): bitarray('1111111111000010'),
    (9,7): bitarray('1111111111000011'),
    (9,8): bitarray('1111111111000100'),
    (9,9): bitarray('1111111111000101'),
    (9,10):bitarray('1111111111000110'),
    
    (10,1): bitarray('111111010'),
    (10,2): bitarray('1111111111000111'),
    (10,3): bitarray('1111111111001000'),
    (10,4): bitarray('1111111111001001'),
    (10,5): bitarray('1111111111001010'),
    (10,6): bitarray('1111111111001011'),
    (10,7): bitarray('1111111111001100'),
    (10,8): bitarray('1111111111001101'),
    (10,9): bitarray('1111111111001110'),
    (10,10):bitarray('1111111111001111'),
    
    (11,1): bitarray('1111111001'),
    (11,2): bitarray('1111111111010000'),
    (11,3): bitarray('1111111111010001'),
    (11,4): bitarray('1111111111010010'),
    (11,5): bitarray('1111111111010011'),
    (11,6): bitarray('1111111111010100'),
    (11,7): bitarray('1111111111010101'),
    (11,8): bitarray('1111111111010110'),
    (11,9): bitarray('1111111111010111'),
    (11,10):bitarray('1111111111011000'),

    (12,1): bitarray('1111111010'),
    (12,2): bitarray('1111111111011001'),
    (12,3): bitarray('1111111111011010'),
    (12,4): bitarray('1111111111011011'),
    (12,5): bitarray('1111111111011100'),
    (12,6): bitarray('1111111111011101'),
    (12,7): bitarray('1111111111011110'),
    (12,8): bitarray('1111111111011111'),
    (12,9): bitarray('1111111111100000'),
    (12,10):bitarray('1111111111100001'),

    (13,1): bitarray('11111111000'),
    (13,2): bitarray('1111111111100010'),
    (13,3): bitarray('1111111111100011'),
    (13,4): bitarray('1111111111100100'),
    (13,5): bitarray('1111111111100101'),
    (13,6): bitarray('1111111111100110'),
    (13,7): bitarray('1111111111100111'),
    (13,8): bitarray('1111111111101000'),
    (13,9): bitarray('1111111111101001'),
    (13,10):bitarray('1111111111101010'),

    (14,1): bitarray('1111111111101011'),
    (14,2): bitarray('1111111111101100'),
    (14,3): bitarray('1111111111101101'),
    (14,4): bitarray('1111111111101110'),
    (14,5): bitarray('1111111111101111'),
    (14,6): bitarray('1111111111110000'),
    (14,7): bitarray('1111111111110001'),
    (14,8): bitarray('1111111111110010'),
    (14,9): bitarray('1111111111110011'),
    (14,10):bitarray('1111111111110100'),

    (15,0): bitarray('11111111001'),
    (15,1): bitarray('1111111111110101'),
    (15,2): bitarray('1111111111110110'),
    (15,3): bitarray('1111111111110111'),
    (15,4): bitarray('1111111111111000'),
    (15,5): bitarray('1111111111111001'),
    (15,6): bitarray('1111111111111010'),
    (15,7): bitarray('1111111111111011'),
    (15,8): bitarray('1111111111111100'),
    (15,9): bitarray('1111111111111101'),
    (15,10):bitarray('1111111111111110'),
    
}


#not the pythonic way of writing this, but at least it works
def DPCM(dc):
  '''
    差分编码 \n
    dc是一个矩阵 1*n的矩阵 长度就是8*8块的个数 每一个item是一个8*8块的dc分量 \n
    a0, a1, a2, a3, a4 -> a0, a1-a0, a2-a1, a3-a2, a4-a3

    demo:
      形如[1,20,30,40] 差分编码后 变为 [1,19,10,10] 使得数字变小,二进制位数就变少了
  '''
  dpcm_arr = np.empty(dc.shape,dtype=dc.dtype)
  # print("dc--------------------",dc)
  if(len(dc) != 0):
    dpcm_arr[0] = dc[0]
  
  for i in range(1,dc.shape[0]):
    dpcm_arr[i] = dc[i]-dc[i-1]
  
  return dpcm_arr

def DPCM_decode(dpcm_arr):
  '''
    dpcm逆变换,很简单,无注释
  '''
  dc_restored = np.empty(dpcm_arr.shape,dtype=dpcm_arr.dtype)
  # print("wwwwwwwwwwwww",dpcm_arr.shape)
  if(dpcm_arr.shape[0] == 0):
    return dc_restored
  dc_restored[0] = dpcm_arr[0]
  for i in range(1,dpcm_arr.shape[0]):
    dc_restored[i] = dpcm_arr[i] + dc_restored[i-1]
  # for i in range(1,dpcm_arr.shape[0]):
  #   dc_restored[i] -= 10
  return dc_restored 
  
def decompose_int_to_size_value(n):
  '''
    返回: (n的二进制比特数量, n的二进制序列)
  '''
  if( n == 0 ):
    size = 0
    value_bitarray = bitarray()
  else:
    size = len( bin(abs(n)) ) - 2 # 将n转换为2进制 bin(abs(n))后的格式如0b101010,size为n采用二进制编码后的比特数
    flag = np.sign(n) # n<0,返回-1; n=0,返回0; n>0,返回1
    abs_bitarray = bitarray( bin(abs(n))[2:] ) # 把开头的0b去掉
    if( flag == -1):
      value_bitarray = flip_bitarray(abs_bitarray) # n<0时翻转二进制数组
    else:
      value_bitarray = abs_bitarray
  return (size, value_bitarray)

def compose_size_value_to_int(size,value_bitarray):
  '''
    参数: size:二进制比特数量 value_bitarray:二进制序列
    返回值: int值
  '''
  if(size == 0): 
    restored_int_val = 0
  else:
    if( value_bitarray[0] == 1 ): # 说明是正数
      restored_int_val =  int(value_bitarray[:size].to01(),2) #截取0到size下标的二进制,能解释传入的value_bitarray贼长
    elif( value_bitarray[0] == 0): # 负数
      restored_int_val = - int(flip_bitarray(value_bitarray[:size]).to01(),2)

  return restored_int_val

def flip_bitarray(barr):
  '''
    翻转二进制数组
    demo:
      1000变为01111
  '''
  converted_str = barr.to01()
  flipped_str = ''
  for i in converted_str:
    if (i=='0'): flipped_str+='1'
    else: flipped_str+='0'
  return bitarray(flipped_str)

def encode_DC_entropy_all(dpcm_arr):
  '''
    参数: dcpm之后的数组 \n
    返回: 编码之后的二进制序列(size_bitarray, value_bitarray) \n
    注意: 并没有返回数组,而是返回每一个item编码后的二进制序列的字符串累加
  '''
  size_bitarray = bitarray()
  value_bitarray = bitarray()

  for n in dpcm_arr:
    cur_size, cur_value_bitarray = decompose_int_to_size_value(n) # cur_size:n所占的比特位数 cur_value_bitarray:二进制数组序列
    #print(hex(cur_size)[2:])
    cur_size_bitarray = huffman_table_DC[hex(cur_size)[2:]] # hex先转换为16进制后再把开头的0x去掉,由DC哈夫曼表得到cur_size的编码
    size_bitarray += cur_size_bitarray
    value_bitarray += cur_value_bitarray
  
  return size_bitarray, value_bitarray

def decode_DC_entropy_all(size_bitarray,value_bitarray):
  '''
    根据size_bitarray,value_bitarray解码得到dcpm之后的数组
    疑问: 不是dcpm之后的数组吧,而是dc之后的数组
  '''
  size_decoded_list = size_bitarray.decode(huffman_table_DC) # 将二进制序列的数组 根据DC哈夫曼表 还原为16进制的数组
  DC_numbers = len(size_decoded_list) # DC分量数组的长度
  dpcm_arr_restored = np.empty(DC_numbers, dtype=int)
  
  index = 0
  for str_cur_size in size_decoded_list:
    cur_size = int(str_cur_size,16)
    restored_val = compose_size_value_to_int(cur_size, value_bitarray) #根据size和bitarray还原成int值,这里的value_bitarray包含此处的值和后面的所有制,函数里面做了截取
    dpcm_arr_restored[index] = restored_val
    value_bitarray = value_bitarray[cur_size:] # 除掉已经运算之后的
    index += 1

  return dpcm_arr_restored


def RLE(ac):
  '''
    RLE编码函数
  '''
  # ac数据格式 1*63
  # rle_arr 不是长度固定的 取决于有多少个0
  # 如果63个ac分量都是0 则返回空的list
  rle_list = []
  consecutive_0s = 0 # 连续0的数量
  
  for ac_coefficient in ac:
    if( ac_coefficient == 0 ):
      consecutive_0s += 1
    else:
      if(consecutive_0s > 15) :
        rle_list.append( (15,0) )
        consecutive_0s -= 16    
      if(consecutive_0s > 15) :
        rle_list.append( (15,0) )
        consecutive_0s -= 16    
      if(consecutive_0s > 15) :
        rle_list.append( (15,0) )
        consecutive_0s -= 16    
      if(consecutive_0s > 15) :
        rle_list.append( (15,0) )
        consecutive_0s -= 16
        
      rle_list.append( (consecutive_0s,ac_coefficient) )
      consecutive_0s = 0 # bug 给错了
    # 不要append(0,0) 直接把他放入huffman_ac表里面
  
  return rle_list


def RLE_decode(rle):
  '''
    RLE解码函数
  '''
  ac_restored_lst = []
 
  for consecutive_0s,number in rle:
    ac_restored_lst.extend([0]*consecutive_0s)
    ac_restored_lst.append(number)
  
  ac_restored_lst.extend([0]*(63-len(ac_restored_lst))) #末尾补上0
  ac_restored_array = np.array(ac_restored_lst)
  
  return ac_restored_array


def decompose_RLE_list_to_huffmanResBitarray_valueBitarray(rle_list):
  '''
    传入RLE编码之后的数组, 返回huffman_res_bitarray, value_bitarray
  '''
  huffman_res_bitarray = bitarray()
  value_bitarray = bitarray()

  for item in rle_list:
    consecutive_0s = item[0] # 0的个数
    (cur_size, cur_value_bitarray) = decompose_int_to_size_value(item[1])
    cur_huffman_key_tuple = (consecutive_0s,cur_size) # key值 0的个数和当前值的二进制比特数构成tuple
    cur_huffman_res_bitarray = huffman_table_AC[cur_huffman_key_tuple]
    huffman_res_bitarray += cur_huffman_res_bitarray
    value_bitarray += cur_value_bitarray # 之后根据这个确定取几个bit
  
  huffman_res_bitarray += bitarray('1010') # 表示block编码的结束

  return huffman_res_bitarray, value_bitarray


def All_block_huffmanResbitarray_valueBitarray_to_RLE_lists(all_block_huffman_res_bitarray,all_block_value_bitarray):
  '''
    RLE逆变换
  '''
  all_block_rle_lists = []
  value_bitarray_left = all_block_value_bitarray
  cur_block_index = 0
  cur_block_RLE_lst = []
  AC_huffman_decode_res = all_block_huffman_res_bitarray.decode(huffman_table_AC) #得到形如 [(0,1),(2,0),...]的表达形式
  
  for cur_consecutive_0s,cur_size in AC_huffman_decode_res:
    if((cur_consecutive_0s,cur_size) == (0,0)): # reaching end of 1 8x8 block
      all_block_rle_lists.append(cur_block_RLE_lst)
      cur_block_index += 1
      cur_block_RLE_lst = []
      continue
    restored_val = compose_size_value_to_int(cur_size,value_bitarray_left)
    cur_block_RLE_lst.append([cur_consecutive_0s,restored_val])
    value_bitarray_left = value_bitarray_left[cur_size:]
    
  return all_block_rle_lists




'''
ab = [1,2,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,8,1,3,0,0,0,0]
ab = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
ans = RLE(ab) # [(0, 1), (0, 2), (3, 3), (7, 1), (0, 8), (0, 1), (0, 3)]
print(ans)

rle_1, rle_2 =  decompose_RLE_list_to_huffmanResBitarray_valueBitarray(ans)
print(rle_1,rle_2)

ans2 = RLE_decode(ans)
print(ans2)
ANSS = All_block_huffmanResbitarray_valueBitarray_to_RLE_lists(rle_1,rle_2)
#cao = decompose_RLE_list_to_huffmanResBitarray_valueBitarray(ANSS)

print(ANSS)
#print(cao)
'''


