"""
This program models various voting systems. It calculates how often the voting systems violate certain social choice
criterion. Each Voting System is its own class, and is derived from the Voting Systems abstract base class. The checks
for the criterion are all in the Voting System class. Each derived class has its own method to determine the winner and
create a societal preference order. The simulations are run in the main function and the data gathered.
"""


import time
from candidate import Candidate
from systems import Nanson, RankedPairs
from itertools import *


def main():
    list_of_cand_objects = []

    c1 = Candidate('A')
    c2 = Candidate('B')
    c3 = Candidate('C')
    c4 = Candidate('D')

    list_of_cand_objects.append(c1)
    list_of_cand_objects.append(c2)
    list_of_cand_objects.append(c3)
    list_of_cand_objects.append(c4)


    c = RankedPairs(10,4,list_of_cand_objects)
    #c.violates_unanimity([3,0,0,0,0,0])
    #a = c.determine_winner([1,0,0,1,1,0],list_of_cand_objects,list(permutations(['A','B','C'])))
    #print(a.name)
    c.find_IIA_violations(100,"IC")
    # c.find_unanimity_vios(1000, "IC")

    print(c.IIAv)
    #print(c.unam_vios)



if __name__ == '__main__':
    main()




