import numpy as np

[ [ [1,2,3],[2,3,4],[3,4,5] ],
          [ [4,5,6],[6,7,8],[8,9,10] ],
          [[11,12,13],[13,14,15],[15,16,17] ]
]
# print(array[:,:,0])

n1 = np.ones((2,2))

n2 = np.ones((1,1))

# n1[0:2,0:2] = np.ones((8,0))
# ValueError: could not broadcast input array from shape (8,0) into shape (2,2)


arr = np.array(
       [[1,2],
       [1,2],
       [1,2] ]
)


print( arr[1:2,2:3] )



'''

Traceback (most recent call last):
  File "D:\MyCode-Git\Diff\try_implement\jpeg_compress\decoder.py", line 94, in <module>
    main()
  File "D:\MyCode-Git\Diff\try_implement\jpeg_compress\decoder.py", line 87, in main
    npmat_restored = restore_img_from_padding(padded_matrix_restored_y,padded_matrix_restored_cb,padded_matrix_restored_cr,rows,cols)+128
  File "D:\MyCode-Git\Diff\try_implement\jpeg_compress\padding_image.py", line 33, in restore_img_from_padding
    Cb_restored = np.repeat((np.repeat(Cb_padded,2,axis=1)),2,axis=0)
  File "<__array_function__ internals>", line 5, in repeat
  File "C:\Users\AIERXUAN\AppData\Local\Programs\Python\Python39\lib\site-packages\numpy\core\fromnumeric.py", line 480, in repeat
    return _wrapfunc(a, 'repeat', repeats, axis=axis)
  File "C:\Users\AIERXUAN\AppData\Local\Programs\Python\Python39\lib\site-packages\numpy\core\fromnumeric.py", line 55, in _wrapfunc
    return _wrapit(obj, method, *args, **kwds)
  File "C:\Users\AIERXUAN\AppData\Local\Programs\Python\Python39\lib\site-packages\numpy\core\fromnumeric.py", line 44, in _wrapit
    result = getattr(asarray(obj), method)(*args, **kwds)
numpy.AxisError: axis 1 is out of bounds for array of dimension 1


'''