import numpy as np
from itertools import *
from sympy.utilities.iterables import multiset_permutations


class Candidate:

    def __init__(self,name):
        list_of_candidates = []
        self.name = name
        self.number_of_votes = 0
        #self.list_of_candidates = []
        list_of_candidates.append(self)

class Plurality:
    def __init__(self):
        pass

    def determine_winner(self,pref_sc):
        pass

    def determine_Condorcet_winner(self,pref_sc):
        pass

    def determine_Condorcet_loser(self,pref_sc):
        pass

    def pref_without_alternatives(self,pref_sc):
        pass

    def majority_winner_exists(self,pref_sc):
        pass




list_of_combos = []

def generate_unique_permutation(n,k):
    unique = []
    a = np.zeros(n)
    b = np.ones(k-1)
    c = np.concatenate((a,b))
    unique = list(multiset_permutations(c))
    return unique

def obtain_combos(unique):
    global list_of_combos
    for val in unique:
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
    candidate_names = []
    c1 = Candidate("A")
    c2 = Candidate("B")
    c3 = Candidate("C")
    for candidate in list_of_candidates:
        candidate_names.append(candidate.name)
    possible_orders = list(permutations(candidate_names))
    #print(possible_orders)
    k = len(possible_orders)
    voters = 4
    arr = generate_unique_permutation(voters, 3)
    stuff = obtain_combos(arr)
    print(stuff)
    #print(len(stuff))

    #print(c1.number_of_votes)


    #print(list(combinations(candidate_names,2)))

    #we have preference orders plus each combo in orderings - can keep as two separate arrays - works


if __name__ == '__main__':
    main()




#pass an array of all candidates - get all the permutations - including k value which will be number of cand !





