import numpy as np
from sympy.utilities.iterables import multiset_permutations

def generate_unique_permutation(n,k):
    voters = np.zeros(n)
    candidates = np.ones(k-1)
    combined_arr = np.concatenate((voters,candidates))
    unique_perms = list(multiset_permutations(combined_arr))
    return unique_perms

def obtain_combos(unique_perms):
    list_of_combos = []
    for val in unique_perms:
        count = 0
        val_to_add = []
        for i in range(0, len(val)):
            if (val[i] == 0):
                count = count + 1
            if (val[i] == 1):
                val_to_add.append(count)
                count = 0
            if (i + 1 == len(val)):
                val_to_add.append(count)
        list_of_combos.append(val_to_add)
    return list_of_combos

def main():
    unique = generate_unique_permutation(3,6)
    list_of_combos = obtain_combos(unique)
    print(list_of_combos)
    print(len(list_of_combos))

if __name__ == '__main__':
    main()
