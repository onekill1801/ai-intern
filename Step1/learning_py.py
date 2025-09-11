import numpy as np

arr = np.array([[1,2,3],[4,5,6]])
print(arr.shape)   # (2, 3)
print(arr.ndim)    # 2 chiều

arr = np.array([1,2,3])
print(arr + 10)  # [11 12 13] (10 được “broadcast” cho mọi phần tử)

arr = np.arange(1,6)
print(arr ** 2)   # [ 1  4  9 16 25]

arr = np.array([10,20,30,40,50])
print(arr[arr > 25])   # [30 40 50]

# mean, std, var, argmax, argmin, sum, cumsum, diff, exp, log, sqrt
arr = np.array([1,2,3,4,5])
print(np.mean(arr))  # 3.0
print(np.std(arr))   # 1.41...

from numpy.linalg import inv, eig
A = np.array([[1,2],[3,4]])
print(inv(A))     # Ma trận nghịch đảo
vals, vecs = eig(A)
print(vals)       # Trị riêng

rand = np.random.randn(3,3)  # phân phối chuẩn
print(rand)
