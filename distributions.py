import numpy as np
import math
import random as rand

def generate_IC_pref(num_voters, num_cands):
    poss_ranks = math.factorial(num_cands)
    arr = np.zeros(poss_ranks, dtype = int)
    for i in range(0, num_voters):
        ind = rand.randrange(0, poss_ranks)
        arr[ind] = arr[ind] + 1
    #print(arr)
    return arr


def generate_IAC_pref(num_voters, num_cands):
    poss_ranks = math.factorial(num_cands)
    arr = np.zeros(poss_ranks, dtype=int)  # this has num_cands! elements
    end_range = num_voters + poss_ranks - 1
    vals = rand.sample(range(0,end_range),poss_ranks-1)  # 5 random vals from 0 to 15 for example
    sorted_vals = sorted(vals)  # sort the values
    arr[0] = sorted_vals[0]  # the first bar
    for i in range(1,len(sorted_vals)):
        arr[i] = sorted_vals[i] - sorted_vals[i-1] - 1
    arr[poss_ranks-1] = end_range - sorted_vals[poss_ranks-2] - 1

    return arr

def generate_IANC(num_voters, num_cands):
    pass



def custom_distribution(num_voters, num_cands, weights):
    poss_ranks = math.factorial(num_cands)
    arr = np.zeros(poss_ranks, dtype=int)
    result = 0
    new_arr = []
    for val in weights:
        result += val
        new_arr.append(result)

    for i in range(0,num_voters):
        chosen_val = rand.random()
        for j in range(0,len(new_arr)):
            if chosen_val <= new_arr[j]:
                arr[j] += 1
                break

    return arr