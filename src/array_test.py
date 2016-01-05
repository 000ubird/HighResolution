'''
@author: BP12084
'''

import numpy as np

array = np.array([[1,2,3] , [4,5,6]])

print(array.shape[1])

print (array[1,:3]) #多次元配列へのアクセス

import matplotlib.pyplot as plt
mean = [0, 0]
cov = [[100, 0], [0, 1000]]  # diagonal covariance

x, y = np.random.multivariate_normal(mean, cov, 500).T
plt.plot(x, y, 'x')
plt.axis('equal')
plt.show()
