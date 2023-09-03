import math
import random as rand
import numpy as np

def generate_IAC_pref(num_voters, num_cands):
    poss_ranks = math.factorial(num_cands)
    arr = np.zeros(poss_ranks)  # this has num_cands! elements
    end_range = num_voters + poss_ranks - 1
    vals = rand.sample(range(0,end_range),poss_ranks-1)  # 5 random vals from 0 to 15 for example
    sorted_vals = sorted(vals)  # sort the values
    arr[0] = sorted_vals[0]  # the first bar
    for i in range(1,len(sorted_vals)):
        arr[i] = sorted_vals[i] - sorted_vals[i-1] - 1
    arr[poss_ranks-1] = end_range - sorted_vals[poss_ranks-2] - 1

    return arr

wow = generate_IAC_pref(10,3)
print(wow)