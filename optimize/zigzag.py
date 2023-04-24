from pickletools import uint8
import numpy as np


def zigzag_sequence_generator(n):
  '''
    生成zigzag编码序列,返回的generator的item形如[2,3] \n
    具体走的方向、判断0和7看zigzag的图
  '''
  point = np.array([0,0])
  MOVING_RIGHT,MOVING_DOWN_LEFT,MOVING_DOWN,MOVING_UP_RIGHT = range(4) #4种状态
  state = MOVING_RIGHT

  for i in range(n*n):
    yield (i, point) # 每一个项是 第几个 和 点的值
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

# 生成zigzag数组 item项形如[2,3]
for (i,point) in zigzag_sequence_generator(n):
  zigzag_sequence_array[i] = point


def zigzag_block_to_array(block_quant_known):
  '''
    将量化之后的8*8矩阵 根据zigzag编码 转换为一维数组
  '''
  array = np.empty(n*n, dtype=int)
  for i,point in enumerate(zigzag_sequence_array): #enumerate 数组转化为对象
    array[i] = block_quant_known[tuple(point)]
  return array

def zigzag_array_to_block(array_known):
  '''
    将zigzag编码后的一维数组 转化为 8*8的矩阵块
  '''
  block = np.empty((n,n), dtype=int)
  for i,point in enumerate(zigzag_sequence_array):
    block[tuple(point)] = array_known[i]
  return block