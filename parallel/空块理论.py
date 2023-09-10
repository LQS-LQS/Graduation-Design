import numpy as np
from scipy import fftpack

table = [ [17, 18, 24, 47, 99, 99, 99, 99],
        [18, 21, 26, 66, 99, 99, 99, 99],
        [24, 26, 56, 99, 99, 99, 99, 99],
        [47, 66, 99, 99, 99, 99, 99, 99],
        [99, 99, 99, 99, 99, 99, 99, 99],
        [99, 99, 99, 99, 99, 99, 99, 99],
        [99, 99, 99, 99, 99, 99, 99, 99],
        [99, 99, 99, 99, 99, 99, 99, 99] ]

def DCT_2D(block):
  DCT_matrix = fftpack.dct( fftpack.dct(block.T, norm='ortho').T, norm='ortho' )
  return DCT_matrix

def quant_block(block):
  '''
    返回量化后的矩阵
  '''
  quanted_block = np.round(np.divide(block, table)).astype(int)
  return quanted_block


# block = np.full((8, 8), 0.49)

# ans = table * block

# DCT_matrix = fftpack.idct( fftpack.idct(ans.T, norm='ortho').T, norm='ortho' )

# DCT_matrix = np.round( DCT_matrix, decimals=1)
# print(DCT_matrix)







a = np.array([[ 269, -146,   53,  -30,   38,   -10,   15,    4],
 [-146,   -6,  -29,    10,   -9,   -3,  -12,    -6],
 [  53,  -29,    21,    4,    12,   -3,    2,    1],
 [ -30,   10,    4,   10,   -1,   -2,   -3,    1],
 [  38,    -9,   12,   -1,   2,   -4,    1,    3],
 [ -10,   -3,   -3,   -2,  -4,   -4,   -1,    1],
 [  15,  -12,     2,   -3,   1,   -1,    1,    1],
 [   4,   -6,    1,    1,   3,    1,    1,    0]])

#a = np.full((8, 8), 1)

print( fftpack.dct( fftpack.dct(a.T, norm='ortho').T, norm='ortho' ) )
aaa = np.round(
    np.divide(
        fftpack.dct( fftpack.dct(a.T, norm='ortho').T, norm='ortho' ),
        table
    )
)


print(aaa)

# maxY = 0
# maxCb = 0
# maxCr = 0
# minY = 0
# minCb = 0
# minCr = 0
def YCbCr( R,G,B ):
    global maxY,maxCb,maxCr,minY,minCb,minCr
    Y = 0.299 * R + 0.587 * G + 0.114 * B
    Cb = -0.169 * R - 0.331 * G + 0.5 * B + 128
    Cr = 0.5 * R - 0.419 * G - 0.081 * B + 128
    # maxY = max(maxY,Y)
    # maxCb = max(maxCb,Cb)
    # maxCr = max(maxCr,Cr)

    # minY = min(minY,Y)
    # minCb = min(minCb,Cb)
    # minCr = min(minCr,Cr)


# for R in range(0,256):
#     for G in range(0,256):
#         for B in range(0,256):
#             YCbCr(R-128,G-128,B-128)