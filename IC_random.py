from itertools import permutations
import random as rand
import numpy as np

#function to compute factorial
#I can instead use the factorial function in the math library
def factorial(n):
    if(n==1):
        return 1
    else:
        return n * factorial(n-1)

#five candidates
num_of_cands = 5
possible_pref = factorial(num_of_cands)  #total amount of possible preference combinations
list_of_cands = []
for i in range(0,num_of_cands):
    letter = chr(ord('A')+i)
    list_of_cands.append(letter)

#list of candidates is A,B,C,D,E (this can be a parameter to a function - a vector of cand names)

#all possible permutations
list1_per = list(permutations(list_of_cands,num_of_cands))
map = {}
for i in range(0, possible_pref):
    map[list1_per[i]] = 0 #initialize all to 0

all_of_them = [] #all the preference schedules
num_trials = 100
num_voters = 1000

for i in range(0,num_trials):
    map = dict.fromkeys(map,0)  #sets all values to 0
    pref_schedule = np.zeros(num_of_cands)
    #for each voter
    for i in range(0,num_voters):
        #generate their preference schedule
        voter_choice = rand.choice(list1_per)
        if(map.get(voter_choice)==None): #this line should not be needed in C++ code
            map[voter_choice] = 1
        else:
            map[voter_choice] += 1

    values = list(map.values())
    all_of_them.append(values)

for arr in all_of_them:
    print(arr)
#print(all_of_them)












""""
for arr in all_of_them:
    print(sum(arr))

    



print(pref_schedule)
"""


#it can handle 1000000 trials and 100 voters for 5 candidates - very good
#IAC will be able to handle more
#need to work more on efficiency

#pretty good with 100000 and 1000



#not working well with higher number of candidates
#maybe try working exclusively with dictionary type




#works with 10000 trials
#for 10 voters 8 candidates - not bad
#work on optimization from here - understand the math - use dictionaries - improve



