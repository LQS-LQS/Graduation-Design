import numpy as np

def get_sub_sampling(matrix):
  rows,cols = matrix.shape[0],matrix.shape[1]
  new_rows = (rows + 1) // 2
  new_cols = (cols + 1) // 2
  arr = np.zeros( (new_rows, new_cols ) )
  for i in range(0,new_rows):
    for j in range(0,new_cols):
      temp_value1 = matrix[i*2][j*2]
      temp_value2 = matrix[i*2][j*2+1]   if ( i*2   < rows and j*2+1 < cols ) else matrix[i*2][j*2]
      temp_value3 = matrix[i*2+1][j*2]   if ( i*2+1 < rows and j*2   < cols ) else matrix[i*2][j*2]
      temp_value4 = matrix[i*2+1][j*2+1] if ( i*2+1 < rows and j*2+1 < cols ) else matrix[i*2][j*2]
      arr[i][j] = (temp_value1 + temp_value2 + temp_value3 + temp_value4) // 4

  return arr