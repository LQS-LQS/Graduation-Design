import numpy as np

# def get_sub_sampling(matrix):
#   rows,cols = matrix.shape[0],matrix.shape[1]
#   new_rows = (rows + 1) // 2
#   new_cols = (cols + 1) // 2
#   arr = np.zeros( (new_rows, new_cols ) )
#   for i in range(0,new_rows):
#     for j in range(0,new_cols):
#       temp_value1 = matrix[i*2][j*2]
#       temp_value2 = matrix[i*2][j*2+1]   if ( i*2   < rows and j*2+1 < cols ) else matrix[i*2][j*2]
#       temp_value3 = matrix[i*2+1][j*2]   if ( i*2+1 < rows and j*2   < cols ) else matrix[i*2][j*2]
#       temp_value4 = matrix[i*2+1][j*2+1] if ( i*2+1 < rows and j*2+1 < cols ) else matrix[i*2][j*2]
#       arr[i][j] = (temp_value1 + temp_value2 + temp_value3 + temp_value4) // 4

#   return arr

import concurrent.futures

def sub_sampling_worker(matrix, rows, cols, i_start, i_end, j_start, j_end):
    arr = np.zeros((i_end-i_start, j_end-j_start))
    for i in range(i_start, i_end):
        for j in range(j_start, j_end):
            temp_value1 = matrix[i*2][j*2]
            temp_value2 = matrix[i*2][j*2+1] if (i*2 < rows and j*2+1 < cols) else matrix[i*2][j*2]
            temp_value3 = matrix[i*2+1][j*2] if (i*2+1 < rows and j*2 < cols) else matrix[i*2][j*2]
            temp_value4 = matrix[i*2+1][j*2+1] if (i*2+1 < rows and j*2+1 < cols) else matrix[i*2][j*2]
            arr[i-i_start][j-j_start] = (temp_value1 + temp_value2 + temp_value3 + temp_value4) // 4
    return arr

def get_sub_sampling(matrix):
    rows, cols = matrix.shape[0], matrix.shape[1]
    new_rows = (rows + 1) // 2
    new_cols = (cols + 1) // 2

    # 分为4块并行计算
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        results = []
        results.append(executor.submit(sub_sampling_worker, matrix, rows, cols, 0, new_rows//2, 0, new_cols//2))
        results.append(executor.submit(sub_sampling_worker, matrix, rows, cols, 0, new_rows//2, new_cols//2, new_cols))
        results.append(executor.submit(sub_sampling_worker, matrix, rows, cols, new_rows//2, new_rows, 0, new_cols//2))
        results.append(executor.submit(sub_sampling_worker, matrix, rows, cols, new_rows//2, new_rows, new_cols//2, new_cols))

    arr = np.vstack((
        np.hstack((results[0].result(), results[1].result())),
        np.hstack((results[2].result(), results[3].result()))
    ))

    return arr