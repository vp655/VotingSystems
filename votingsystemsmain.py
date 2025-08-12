"""
This program models various voting systems. It calculates how often the voting systems violate certain social choice
criterion. Each Voting System is its own class, and is derived from the Voting Systems abstract base class. The checks
for the criterion are all in the Voting System class. Each derived class has its own method to determine the winner and
create a societal preference order. The simulations are run in the main function and the data gathered.
"""


import time
from candidate import Candidate
from systems import *


def main():

    c1 = Candidate('A')
    c2 = Candidate('B')
    c3 = Candidate('C')

    list_of_cand_objects = [c1, c2, c3]

    c = Plurality(3, 3, list_of_cand_objects)
    c.find_IIA_violations(100, "IC")
    print(f"IIA violations: {c.IIAv}")


if __name__ == '__main__':
    main()




