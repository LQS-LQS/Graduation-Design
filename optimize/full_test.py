'''
from PIL import Image
import numpy as np
from scipy import fftpack

image_to_compress = Image.open("D:\\MyCode-Git\\Diff\\try_implement\\1.jpg")

ycbcr = image_to_compress.convert('YCbCr')

print(ycbcr)

npmat = np.array(ycbcr, dtype=int) - 128
rows,cols = npmat.shape[0], npmat.shape[1]

print(npmat.size)

print( len( npmat ), len( npmat[0] ), len( npmat[0][0] ))


print(rows,cols)

print( npmat[:,:,0] )

print( len(npmat[:,:,0]))
print( len(npmat[:,:,0][0]))
# print( len( npmat[0][0][0] ))

testArr = np.empty( (8,8), dtype=int)

block = np.random.randint(-128,127,(2,2))

print( fftpack.dct( fftpack.dct(block.T, norm='ortho').T, norm='ortho' ) )

print( fftpack.dct( block, norm='ortho'))

print( np.array([1,2,3])/np.array([1,2,3]) )


def func():
  for i in range(0,8):
    yield(i,i)

print(func())

print(tuple([1,2]))

'''



# -------------------------------------------------

'''
from pickletools import uint8
import numpy as np


def zigzag_sequence_generator(n):
  point = np.array([0,0])
  MOVING_RIGHT,MOVING_DOWN_LEFT,MOVING_DOWN,MOVING_UP_RIGHT = range(4) #4种状态
  state = MOVING_RIGHT

  for i in range(n*n):
    yield (i, point)
    if( state == MOVING_RIGHT ):
      point += [0,1]
      if( point[0] == 0 ):
        state = MOVING_DOWN_LEFT
      elif( point[0] == 7 ):
        state = MOVING_UP_RIGHT
  
    elif( state == MOVING_DOWN_LEFT ):
      point += [1,-1]
      if( point[0] == 7 ):
        state = MOVING_RIGHT
      elif( point[1] == 0 ):
        state = MOVING_DOWN
    
    elif( state == MOVING_DOWN ):
      point += [1,0]
      if( point[1] == 0 ):
        state = MOVING_UP_RIGHT
      elif( point[1] == 7 ):
        state = MOVING_DOWN_LEFT
    
    elif( state == MOVING_UP_RIGHT ):
      point += [-1,1]
      if( point[1] == 7 ):
        state = MOVING_DOWN  
      elif( point[0] ==0 ):
        state = MOVING_RIGHT


n = 8
zigzag_sequence_array = np.empty( (n*n, 2), dtype=int)

for (i,point) in zigzag_sequence_generator(n):
  zigzag_sequence_array[i] = point


def zigzag_block_to_array(block_quant_known):
  array = np.empty(64, dtype=int)
  for i,point in enumerate(zigzag_sequence_array): #enumerate 数组转化为对象
    array[i] = block_quant_known[tuple(point)]
  return array

print( zigzag_block_to_array(np.random.randint(-128,127,(8,8))))

print( np.sign(1110) )

'''





import numpy as np
from scipy import fftpack
from bitarray import bitarray
lqs_ar = np.ones((3,3))
DCT_matrix = fftpack.dct( fftpack.dct(lqs_ar.T).T )
print( fftpack.dct(lqs_ar.T) )
print( DCT_matrix )



a,b,c,d = range(4)
print(a,b,c,d)


for i in range(0,3):
    print(i)


print( len([1,23]))


print( bitarray( format(len([1]), '#018b')[2:] ) )