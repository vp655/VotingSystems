"""
This program models various voting systems. It calculates how often the voting systems violate certain social choice
criterion. Each Voting System is its own class, and is derived from the Voting Systems abstract base class. The checks
for the criterion are all in the Voting System class. Each derived class has its own method to determine the winner and
create a societal preference order. The simulations are run in the main function and the data gathered.
"""


import time
from candidate import Candidate
from systems import Nanson
from itertools import *


def main():
    list_of_cand_objects = []

    c1 = Candidate('A')
    c2 = Candidate('B')
    c3 = Candidate('C')
    # c4 = Candidate('D')

    list_of_cand_objects.append(c1)
    list_of_cand_objects.append(c2)
    list_of_cand_objects.append(c3)


    c = Nanson(3,3,list_of_cand_objects)
    c.determine_winner([3,2,1,0,0,0],list_of_cand_objects,list(permutations(['A','B','C'])))
    c.find_IIA_violations(1000,"IC")
    c.find_unanimity_vios(10000, "IC")

    print(c.IIAv)
    print(c.unam_vios)



if __name__ == '__main__':
    main()




