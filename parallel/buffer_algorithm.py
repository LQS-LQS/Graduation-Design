import numpy as np
from bitarray import bitarray

def for_test_bitarray_to_int01_arr( bits ):
  lst = list(bits)
  result = [int(bit) for bit in lst]
  return result
def number_to_bitarray( int_value, total=8 ):
  #print( int_value )
  try:
    temp = bin(int_value)[2:]
  except:
    print(int_value)
  temp = temp.zfill(total)
  return temp
def int01_arr_to_bits(arr):
  '''
    传入01数组int \n
    返回二进制序列
  '''
  return bitarray(arr.tolist())
def bits_to_int01_arr(arr):
  result = list(arr)
  return result

# 将位转换为字节
def bits_to_ints(bits):
  length = len(bits)
  temp = length // 8
  if(temp*8 == length):
    add_0s = 0
  else:
    add_0s = (temp+1)*8 - length
  '''
    传入byte数组 \n
    返回int数组 \n
    大顶端模式，也就是末尾补0，如果传入1，返回128
  '''
  bytes_arr = bits.tobytes()
  int_arr = [int.from_bytes(bytes_arr[i:i+1], byteorder='big') for i in range(0, len(bytes_arr), 1)]
  #print(int_arr)
  return int_arr, add_0s

def ints_to_bits(ints):
  result = bitarray('')
  for i in range(0, len(ints)):
    result += bitarray( bin(ints[i])[2:].zfill(8) )
  return result

# 统计连续零值字节的数量和平均值
def count_zeros(data):
  num_zeros = 0
  num_sequences = 0
  zero_sequences = []
  for byte in data:
    if byte == 0:
      num_zeros += 1
    else:
      if num_zeros > 0:
        num_sequences += 1
        zero_sequences.append(num_zeros)
        num_zeros = 0
  if num_zeros > 0:
    num_sequences += 1
    zero_sequences.append(num_zeros)
  if( num_sequences == 0):
    avg_zeros = 255
  else:
    avg_zeros = int(sum(zero_sequences) / num_sequences)
  return avg_zeros, zero_sequences


# 替换连续零值字节序列
def replace_zeros(data, avg_zeros):
  data_list = []
  i = 0
  while i < len(data):
    if data[i] == 0:
      count = 1
      while count < avg_zeros and i + count < len(data) and data[i+count] == 0:
        count += 1
      if count == avg_zeros:
        data_list.append( 255 )
        i += avg_zeros
      else:
        for j in range(0,count):
          data_list.append(0)
        i += count
    else:
      data_list.append( data[i] )
      i += 1
  return data_list
def unreplace_zeros(data, avg_zeros):
  data_list = []
  for i in range( 0, len(data) ):
    if(data[i] == 255):
      for j in range(0, avg_zeros):
        data_list.append(0)
    else:
      data_list.append( data[i] )
  return data_list

def change_bit( arr ):
  res = np.zeros(arr.shape[0], dtype=int)
  res[0] = arr[0]
  for i in range(1, arr.shape[0]):
    if(arr[i] == arr[i-1]):
      res[i] = 0
    else:
      res[i] = 1
  return res
def de_change_bit( arr ):
  if( len(arr) == 0):
    return int01_arr_to_bits(np.zeros(0, dtype=int))
  res = np.zeros(len(arr), dtype=int)
  res[0] = arr[0]
  for i in range(1, len(arr)):
    if(arr[i]==0):
      res[i] = res[i-1]
    else:
      if( res[i-1] == 0):
        res[i] = 1
      else:
        res[i] = 0
  return int01_arr_to_bits(res)

def to_bitarray( arr, avg_zeros, add_0s, cnt_block_count):
  # print('into to_bitarray',cnt_block_count)
  '''
    全部变成八进制
  '''
  arr_bitarray = bitarray('')
  for i in range( 0, len(arr) ):
    arr_bitarray += bitarray( number_to_bitarray(arr[i]) )
  avg_zeros_bitarray =  bitarray(  number_to_bitarray( avg_zeros, 16 )  )
  add_0s_bitarray = bitarray(  number_to_bitarray( add_0s, 16 )  ) 
  cnt_block_count_bitarray = bitarray(  number_to_bitarray(cnt_block_count, 16)  )  
  return arr_bitarray, avg_zeros_bitarray, add_0s_bitarray, cnt_block_count_bitarray
def getBuffer(int_01_array, cnt_block_count):
  '''
    传入01矩阵int\n
    传出压缩之后的矩阵int && 补0的个数
  '''
  int_01_array = change_bit(int_01_array)      # 改变位
  # print("该变位之后的矩阵",int_01_array)
  bits_arr = int01_arr_to_bits( int_01_array ) # 将01的int数组转换为比特序列
  # print("比特序列",bits_arr)
  ints_arr,add_0s = bits_to_ints( bits_arr )   # 将比特序列转换为字节
  # print("字节序列",ints_arr)
  avg_zeros,_ = count_zeros(ints_arr)          # 计算连续0的平均个数
  ints_arr = replace_zeros(ints_arr, avg_zeros) # 进行连续0的平均个数的替换
  # print("替换之后的",ints_arr)
  ints_arr, avg_zeros, add_0s, cnt_block_count = to_bitarray(ints_arr, avg_zeros, add_0s, cnt_block_count)
  return ints_arr, avg_zeros, add_0s, cnt_block_count


def func(ints_arr, add_0s):
  length = len(ints_arr)
  # print("len",length)
  res = np.empty(length//8, dtype=int)
  for i in range(0, length-8, 8):
    bits = ints_arr[i:i+8]
    num = int(bits.to01(), 2)
    res[i//8] = num
  res[length//8 -1] = int(ints_arr[length-8:length-add_0s].to01(), 2)
  return res
def resumeBuffer(ints_arr, avg_zeros, add_0s):
  '''
    上面函数的逆
    传进来bitarray('0101010110什么玩意的')
  '''
  # print(avg_zeros,add_0s)
  #avg_zeros = int(avg_zeros.to01(), 2)
  #add_0s = int(add_0s.to01(), 2)
  arr,_ = bits_to_ints(ints_arr)
  # print("将01序列每八个变成整数",arr)
  ints_arr = unreplace_zeros(arr, avg_zeros) # 进行255替换成连续0
  # print("进行255替换成连续0",ints_arr)
  bits_arr = ints_to_bits(ints_arr) # 转换为二进制序列
  # print("转换为二进制序列",bits_arr)
  bits_arr = bits_arr[0 : len(bits_arr)-add_0s] #去掉补充的0
  # print("去掉补充的0",bits_arr)
  ints_arr = de_change_bit(bits_arr)  #改变位
  # print("改变位的",ints_arr)
  int_01_arr = bits_to_int01_arr(ints_arr)
  return int_01_arr


# ints_arr, avg_zeros, add_0s,_ = getBuffer( np.array([ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
#                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
#                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
#                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 
#                       0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
#                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 
#                       0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
#                       0, 0, 0,  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 
#                       0, 1
# ], dtype=int), 0)



# tt = resumeBuffer(ints_arr,avg_zeros,add_0s)

# print(tt)


# print(replace_zeros(np.array([	128, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 16, 128, 20, 0, 17, 0, 27, 20, 9, 240, 4],dtype=int),3))

# print(unreplace_zeros(np.array([128, 255, 255, 255, 5, 0, 0, 16, 128, 20, 0, 17, 0, 27, 20, 9, 240, 4]),3))