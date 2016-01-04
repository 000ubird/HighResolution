'''
@author: BP12084
'''

import numpy as np

old = np.array([ [1, 2, 3], [4,5,6] ])
new = np.insert(old, 2 , [5,6,7] ,axis=0)
new = np.insert(new, 3 , [5,6,8] ,axis=0)
old = np.array([ [1, 2, 3], [4,5,6] ])

#print (old)
#print (new)

array = np.array([[1,1,1]],dtype=float)

array2 = np.array([],dtype=float)
array2 = np.insert(array2,0,0)
print(array2)
array2 = np.insert(array2,1,1)
print(array2)
array2 = np.insert(array2,2,2)
print(array2)

print("\n")
array = np.insert(array,1,array2,axis=0)
print(array)
array = np.insert(array,2,array2,axis=0)
print(array)