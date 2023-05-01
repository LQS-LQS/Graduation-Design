from logging import BufferingFormatter
from bitarray import *
from bitarray.util import *

def file_bitarray_decompose(file_bitarray):
  rows = ba2int(file_bitarray[:16]) # rows
  cols = ba2int(file_bitarray[16:32]) # 列数
  avg_zeros_buffer_cb = ba2int(file_bitarray[32:48])
  add_0s_buffer_cb    = ba2int(file_bitarray[48:64])
  cnt_empty_block_cb  = ba2int(file_bitarray[64:80])
  avg_zeros_buffer_cr = ba2int(file_bitarray[80:96])
  add_0s_buffer_cr    = ba2int(file_bitarray[96:112])
  cnt_empty_block_cr  = ba2int(file_bitarray[112:128])
  file_bitarray = file_bitarray[128:] # 其余的数据

  buffer_relative_arr = [ avg_zeros_buffer_cb,  \
                          add_0s_buffer_cb,     \
                          cnt_empty_block_cb,   \
                          avg_zeros_buffer_cr,  \
                          add_0s_buffer_cr,     \
                          cnt_empty_block_cr]
  bitarr_len_lst = []
  for i in range(14):
    # print("lennnnnnnnnnnnn",int(file_bitarray[:32].to01(),2))
    bitarr_len_lst.append(file_bitarray[:32])
    file_bitarray = file_bitarray[32:] # 每次取走一个len值,一个len占32位


  bitarr_lst = []
  for bcur_bitarr_len in bitarr_len_lst:
    cur_len = ba2int(bcur_bitarr_len)
    bitarr_lst.append(file_bitarray[:cur_len])
    file_bitarray = file_bitarray[cur_len:] #whats fking wrong with this line?

  return rows,cols,buffer_relative_arr,bitarr_len_lst,bitarr_lst