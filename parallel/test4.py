import numpy as np

dc = np.zeros( 5, dtype=int )

delete_dc = dc[np.arange(dc.size - 3)]

ac_arrays = np.zeros((4,2),dtype=int) # ac系数, 大小为 block_total*63


delete_ac = np.delete( ac_arrays, [2,3], axis=0)


print( delete_dc )
print( delete_ac )


from bitarray import bitarray

a = bitarray('1')
a += bitarray('0')
a = 8
print( len(bitarray('000'))  ) # 把开头的0b去掉)


print(np.zeros(63,dtype=int))

print(np.array([0],dtype=int))


def number_to_bitarray( int_value ):
  print('lqs1')
  temp = bin(int_value)[2:]
  print('lqs2')
  #print(int_value)
  print('lqs3')
  temp = temp.zfill(8)
  print('lqs4')
  return temp

#print( number_to_bitarray(bitarray('101')))



f = bitarray('01111111')

f = f[0] == 0

print(bitarray(str(0)))


print(len([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
           1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
           1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
           1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
           1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 
           1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 
           0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 
           1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0]) )


print([1].tolist())