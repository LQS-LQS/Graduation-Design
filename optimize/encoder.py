import argparse
import numpy as np
import time

from bitarray         import bitarray
from bitarray.util    import ba2int
from PIL              import Image, ImageFilter
from DC_AC_extract    import dct_quant_and_extract_DC_AC_from_padded_matrix
from entropy_encoding import DPCM, RLE, decompose_RLE_list_to_huffmanResBitarray_valueBitarray, encode_DC_entropy_all,decode_DC_entropy_all
from padding_image    import *
from utils            import get_sub_sampling
from buffer_algorithm import getBuffer

def main():
  start_time = time.perf_counter()

  # 输入格式 python encoder.py 1.jpg 123
  parser = argparse.ArgumentParser()
  parser.add_argument("image_to_compress", help="path to the input image")
  parser.add_argument("compressed_file", help="path to the output compressed file")
  args = parser.parse_args()
  input_image_path  = args.image_to_compress
  output_image_path = args.compressed_file
  image_to_compress = Image.open(input_image_path) # 读入图片
  # image_to_compress = image_to_compress.filter(ImageFilter.GaussianBlur(radius=2)) #去噪

  # 1. 图片由RGB转换为YCbCr
  ycbcr = image_to_compress.convert('YCbCr') # RGB转换为YCbCr
  npmat = np.array(ycbcr, dtype=int) - 128 # 归一化处理,每一个分量的范围-128~127, npmat:width * height * 3
  
  rows,cols = npmat.shape[0],npmat.shape[1] # 像素的行数和列数
  # print("压缩文件的行数:",rows /2 /8,"压缩文件的列数:" ,cols /2 /8)
  readDataTime = time.perf_counter()
  print(f"encoder's readData time : {readDataTime-start_time:.4f} s")
  # 2. 色度缩减取样 subsampling(4:2:0) + padding
  '''
    这个步骤中,需要进行2*2的矩阵分块,
    之后矩阵大小变为 rows/2 和 cols/2,
    而dct中需要切割8*8的矩阵块,则 rows/2和cols/2需要是8的倍数
    故：rows和cols是16的倍数

    方法1:直接把原图像的rows和cols变为16的倍数
    方法2:Y,Cb,Cr分离,对于Y只需要8的倍数,而Cb和Cr先采样，再变为8的倍数
      demo:7*7大小的矩阵,采样后变为4*4,然后变为8*8;
  '''
  y  = npmat[:,:,0] # 取每一个元素的第三个分量 y:width * height * 1，YCbCr中的Y分量
  #Cb = npmat[::2,::2,1] # 行数和列数步长为2
  #print(Cb)
  #print(Cb)
  #Cr = npmat[::2,::2,2] # 行数和列数步长为2
  Cb = get_sub_sampling(npmat[:,:,1])
  Cr = get_sub_sampling(npmat[:,:,2])
  Y_padded  = martix_padding(y)  # 将矩阵补充成8的倍数
  Cb_padded = martix_padding(Cb) # 将矩阵补充成8的倍数
  Cr_padded = martix_padding(Cr) # 将矩阵补充成8的倍数

  sumSampAndPaddingTime = time.perf_counter()
  print(f"encoder's sumSampAndPaddingTime time : {sumSampAndPaddingTime-readDataTime:.4f} s")
  # 3. dct变换 + quant量化  + dc/ac提取

  # 提取dc和ac系数 y分量不需要buffer，cb和cr分量才需要有buffer，由于判断的是整个块是否为空，所以dc和ac的buffer其实是一样的
  dc_y,ac_arrays_y,_,_  = dct_quant_and_extract_DC_AC_from_padded_matrix(Y_padded,  'lum')
  dc_cb,ac_arrays_cb,buffer_cb,cnt_empty_block_cb = dct_quant_and_extract_DC_AC_from_padded_matrix(Cb_padded, 'chrom')
  dc_cr,ac_arrays_cr,buffer_cr,cnt_empty_block_cr = dct_quant_and_extract_DC_AC_from_padded_matrix(Cr_padded, 'chrom')
  
  # print("buffer:cb",len(buffer_cb))  #单纯的01矩阵
  # print("buffer:cr",len(buffer_cr))  #单纯的01矩阵
  quantTime = time.perf_counter()
  print(f"encoder's quantTime time : {quantTime-sumSampAndPaddingTime:.4f} s")
  ints_buffer_cb, avg_zeros_buffer_cb, add_0s_buffer_cb, cnt_empty_block_cb = getBuffer(buffer_cb, cnt_empty_block_cb)  #得到压缩之后的数据
  ints_buffer_cr, avg_zeros_buffer_cr, add_0s_buffer_cr, cnt_empty_block_cr = getBuffer(buffer_cr, cnt_empty_block_cr)  #得到压缩之后的数据
  # dpcm + dc的熵编码
  # 差分编码
  # print("buffer:cb",len(ints_buffer_cb),avg_zeros_buffer_cb,add_0s_buffer_cb,cnt_empty_block_cb)
  # print("buffer:cr",len(ints_buffer_cr),avg_zeros_buffer_cr,add_0s_buffer_cr,cnt_empty_block_cr)
  dpcm_y  = DPCM(dc_y)
  dpcm_cb = DPCM(dc_cb)
  dpcm_cr = DPCM(dc_cr)

  # dc差分编码
  size_bitarray_dc_y, value_bitarray_dc_y = encode_DC_entropy_all(dpcm_y)
  size_bitarray_dc_cb, value_bitarray_dc_cb = encode_DC_entropy_all(dpcm_cb)
  
  size_bitarray_dc_cr, value_bitarray_dc_cr = encode_DC_entropy_all(dpcm_cr)


  dcTime = time.perf_counter()
  print(f"encoder's dcTime time : {dcTime-quantTime:.4f} s")
  # print("size_bitarray_dc_cb",size_bitarray_dc_cb)
  # print("value_bitarray_dc_cb",value_bitarray_dc_cb)
  # print("size_bitarray_dc_cr",size_bitarray_dc_cr)
  # print("value_bitarray_dc_cr",value_bitarray_dc_cr)
  # 对于每一个8*8矩阵块的ac系数进行RLE行程编码,然后通过比特编码联合在一起
  huffman_res_bitarray_ac_y = bitarray()
  value_res_bitarray_ac_y = bitarray()
  for ac_y in ac_arrays_y:
    tmp_RLE_res = RLE(ac_y)
    huffman_tmp_bitarray_ac_y, value_tmp_bitarray_ac_y = decompose_RLE_list_to_huffmanResBitarray_valueBitarray(tmp_RLE_res)
    huffman_res_bitarray_ac_y += huffman_tmp_bitarray_ac_y
    value_res_bitarray_ac_y   += value_tmp_bitarray_ac_y
  
  huffman_res_bitarray_ac_cb = bitarray()
  value_res_bitarray_ac_cb   = bitarray()
  for ac_cb in ac_arrays_cb:
    tmp_RLE_res = RLE(ac_cb)
    huffman_tmp_bitarray_ac_cb, value_tmp_bitarray_ac_cb = decompose_RLE_list_to_huffmanResBitarray_valueBitarray(tmp_RLE_res)
    huffman_res_bitarray_ac_cb += huffman_tmp_bitarray_ac_cb
    value_res_bitarray_ac_cb   += value_tmp_bitarray_ac_cb
    
  huffman_res_bitarray_ac_cr = bitarray()
  value_res_bitarray_ac_cr   = bitarray()
  for ac_cr in ac_arrays_cr:
    tmp_RLE_res = RLE(ac_cr)
    huffman_tmp_bitarray_ac_cr, value_tmp_bitarray_ac_cr = decompose_RLE_list_to_huffmanResBitarray_valueBitarray(tmp_RLE_res)
    huffman_res_bitarray_ac_cr += huffman_tmp_bitarray_ac_cr
    value_res_bitarray_ac_cr += value_tmp_bitarray_ac_cr

  rleTime = time.perf_counter()
  print(f"encoder's rleTime time : {rleTime-dcTime:.4f} s")
  # 存储文件
  with open(output_image_path, 'wb') as outFile:
    bitarray_lst = [
      size_bitarray_dc_y,value_bitarray_dc_y,\
      size_bitarray_dc_cb,value_bitarray_dc_cb,\
      size_bitarray_dc_cr,value_bitarray_dc_cr,\
      huffman_res_bitarray_ac_y,value_res_bitarray_ac_y,\
      huffman_res_bitarray_ac_cb,value_res_bitarray_ac_cb,\
      huffman_res_bitarray_ac_cr,value_res_bitarray_ac_cr, \
      ints_buffer_cb, ints_buffer_cr,
    ]
    # y分量的dc和ac很多
    write_bitarray = bitarray()
    # print(avg_zeros_buffer_cb,add_0s_buffer_cb,cnt_empty_block_cb,avg_zeros_buffer_cr,add_0s_buffer_cr,cnt_empty_block_cr)
    rows_barr = bitarray( format(rows, '#018b')[2:] ) # 行数和列数
    cols_barr = bitarray( format(cols, '#018b')[2:] ) # 2:是因为去掉0b
    write_bitarray += rows_barr # 行数和列数
    write_bitarray += cols_barr
    write_bitarray += avg_zeros_buffer_cb # cb平均0的个数   16位  上面都是16位
    write_bitarray += add_0s_buffer_cb  # cb添加0的个数     16位
    write_bitarray += cnt_empty_block_cb # cb空快个数       16位
    write_bitarray += avg_zeros_buffer_cr # cr平均0的个数   16位
    write_bitarray += add_0s_buffer_cr  # cr添加0的个数     16位
    write_bitarray += cnt_empty_block_cr # cr空快个数       16位


    # print("行数:"+ format(rows, '#018b')[2:] + "  列数:" + format(cols, '#018b')[2:])

    for barr in bitarray_lst:
      # print("lennnnn",len(barr))
      # print(format(len(barr), '#034b')[2:])
      cur_bit_len_barr = bitarray( format(len(barr), '#034b')[2:] ) # 记住每一个item的长度
      write_bitarray += cur_bit_len_barr # bitarray_lst每一个item的长度

    for barr in bitarray_lst:
      write_bitarray += barr

    write_bitarray.tofile(outFile)
    # outFile格式 行数, 列数, 
    #

    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print(f"encoder's wtire time : {end_time-rleTime:.4f} s")
    print(f"encoder's execution time : {elapsed_time:.4f} s")
    print("------------------------------------------------")
    print((quantTime-sumSampAndPaddingTime)/elapsed_time*100)
    print("------------------------------------------------")
if __name__ == "__main__":
  main()


  
