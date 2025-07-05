"""
This program models various voting systems. It calculates how often the voting systems violate certain social choice
criterion. Each Voting System is its own class, and is derived from the Voting Systems abstract base class. The checks
for the criterion are all in the Voting System class. Each derived class has its own method to determine the winner and
create a societal preference order. The simulations are run in the main function and the data gathered.
"""

# importing required libraries

import time
from candidate import Candidate
from systems import Plurality


def main():
    list_of_cand_objects = []

    c1 = Candidate('A')
    c2 = Candidate('B')
    c3 = Candidate('C')
    c4 = Candidate('D')

    list_of_cand_objects.append(c1)
    list_of_cand_objects.append(c2)
    list_of_cand_objects.append(c3)


    c = Plurality(1000,3,list_of_cand_objects)
    c.find_condorcet_vios(10000, "IC")
    #print(c.violates_condorcet([1,3,3,1,2,0]))

    print(c.cwc_vio)











if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time()



