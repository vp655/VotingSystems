import numpy as np
import random as rand
from itertools import combinations

arr = np.ones(20)
print(arr)
for i in range(0,len(arr)):
    print(arr[i])


#python after so long!!!


def inside_out():
    count = 0
    arr2 = np.zeros(10)
    for i in range(0,len(arr2)):
        print(arr2[i]);
        count = count + 1
        if(count == 5):
            print("Count is 5")


def find_max(arr):
    max = - 10000
    for val in arr:
        if(val>max):
            max = val
    return max



inside_out();
max = find_max([1,2,3,400,32,12,3])
print(max)

array = ["wow","cool","practice"]
print(array[0])

cool = rand.randint(0,1)
print(cool)



abc = combinations(['A','B','C'],2)
print(list(abc))




