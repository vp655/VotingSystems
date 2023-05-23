
#this code shows the simple plurality model
#imperative to add comments and do through it again
#maybe this class can inherit from a superclass called voting systems with parameters num_cands and num_voters ...
#that may be a good idea

import numpy as np
from itertools import *
from sympy.utilities.iterables import multiset_permutations
import random as rand

class Candidate:
    def __init__(self,name,num_votes,list_of_cand):
        self.name = name
        self.num_votes = num_votes
        list_of_cand.append(self)
        self.num_of_wins = 0
        self.condorcet_points = 0
        self.condorcet_wins = 0




class Plurality:
    def __init__(self,num_voters,num_cands, cand_objects, list_cands):
        self.num_voters = num_voters
        self.num_cands = num_cands
        self.list_cands = list_cands
        self.cand_objects = cand_objects
        self.possible_preference_schedules = []
        self.possible_orders = []
        self.comparisons = []
        self.cwc_vio = 0



    def generate_preference_schedules(self):
        unique_permutations = generate_unique_permutation(self.num_voters, self.num_cands)
        self.possible_preference_schedules = obtain_combos(unique_permutations)

    def generate_candidates_combos(self):
        self.possible_orders = list(permutations(self.list_cands))

    def determine_winner(self,pref_schedule):
        for cand in self.cand_objects:
            cand.num_votes = 0
        count =0
        for val in pref_schedule:
            cand_getting_votes = self.possible_orders[count][0]
            for cand in self.cand_objects:
                if(cand.name == cand_getting_votes):
                    cand.num_votes += val

            count += 1
        vote_array = []
        for cand in self.cand_objects:
            vote_array.append(cand.num_votes)
        index = self.most_votes_aliter(vote_array)
        if(index == -1):
            return None
        return self.cand_objects[index]


    def most_votes(self,vote_array):
        max = -1
        max_index = -1
        for i in range(0,len(vote_array)):
            if(vote_array[i]>max):
                max = vote_array[i]
                max_index = i
            elif(vote_array[i] == max):
                randomized = rand.randint(0,1)
                if(randomized == 1):
                    max_index = i

        return max_index

    def most_votes_aliter(self,vote_array):
        max = -1
        max_index = -1
        are_we_tied = 0
        tied_index = []
        for i in range(0,len(vote_array)):
            if(vote_array[i]>max):
                max = vote_array[i]
                max_index = i
                tied_index.clear()
                tied_index.append(i)
                are_we_tied = 0
            elif(vote_array[i] == max):
                tied_index.append(i)
                are_we_tied = 1

        if(are_we_tied==1):
            max_index = rand.choice(tied_index)
            #max_index = -1
            #if I wanted random ties, cut the -1 line and put in the rand_choice line

            #it randomly gets a few right


        return max_index




    def find_Condorcet_candidate(self,pref_schedule):
        for cand in self.cand_objects:
            cand.condorcet_wins = 0
        self.comparisons = list(combinations(self.list_cands,2))
        #print(self.comparisons)
        for comp in self.comparisons:
            cand_win_head_to_head = self.compare(comp,pref_schedule)
            if(cand_win_head_to_head == None):
                continue
            cand_win_head_to_head.condorcet_wins += 1
        for cand in self.cand_objects:
            if(cand.condorcet_wins == self.num_cands - 1):
               return cand
        return None




    def compare(self,comp, pref_schedule):
        cand1 = self.find_which_candidate_w_name(comp[0])
        cand2 = self.find_which_candidate_w_name(comp[1])
        for cand in self.cand_objects:
            cand.condorcet_points = 0
        for i in range(0,len(pref_schedule)):
            order = self.possible_orders[i]
            index_one = self.find_index_of(comp[0],order)
            index_two = self.find_index_of(comp[1],order)
            if(index_one < index_two):
                cand1.condorcet_points += pref_schedule[i]
            elif(index_one > index_two):
                cand2.condorcet_points += pref_schedule[i]
        if(cand1.condorcet_points > cand2.condorcet_points):
            return cand1
        elif(cand2.condorcet_points > cand1.condorcet_points):
            return cand2
        elif(cand1.condorcet_points == cand2.condorcet_points):
            return None




    def find_which_candidate_w_name(self,name):
        for cand in self.cand_objects:
            if cand.name == name:
                return cand
        return 0


    def find_index_of(self,val,ordering):
        for i in range(0,len(ordering)):
            if(val==ordering[i]):
                return i
        return -1




    def find_all_winners(self):
        for pref_schedule in self.possible_preference_schedules:
            cand_win = self.determine_winner(pref_schedule)
            cand_condorcet = self.find_Condorcet_candidate(pref_schedule)
            if(cand_condorcet!= None):
                if(cand_win == None):
                    self.cwc_vio += 1
                elif(cand_win.name != cand_condorcet.name):
                    self.cwc_vio += 1

            if(cand_win!=None):
                cand_win.num_of_wins += 1


            """
            print(pref_schedule)
            if(cand_condorcet!=None):
                print(cand_condorcet.name)

            print(cand_win.name)
            """
            #cand_win.num_of_wins += 1






def factorial(n):
    if(n==1):
        return 1
    else:
        return n * factorial(n-1)



def generate_unique_permutation(voters,candidates):
    n = voters
    k = factorial(candidates)
    unique = []
    a = np.zeros(n)
    b = np.ones(k-1)
    c = np.concatenate((a,b))
    unique = list(multiset_permutations(c))
    return unique

def obtain_combos(unique):
    list_of_combos = []
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
    number_of_voters = 10
    number_of_cands = 3
    list_of_cand_objects = []
    c1 = Candidate('A',0,list_of_cand_objects)
    c2 = Candidate('B',0,list_of_cand_objects)
    c3 = Candidate('C',0,list_of_cand_objects)
    list_of_cand_names = []
    for candidate in list_of_cand_objects:
        list_of_cand_names.append(candidate.name)

    election = Plurality(number_of_voters,number_of_cands,list_of_cand_objects, list_of_cand_names)
    election.generate_preference_schedules()
    election.generate_candidates_combos()
    print(election.possible_preference_schedules)
    print(election.possible_orders)

    election.find_all_winners()
    print(election.cwc_vio)
    print(len(election.possible_preference_schedules))
    print((election.cwc_vio/len(election.possible_preference_schedules) )*100)
    print(c1.num_of_wins)
    print(c2.num_of_wins)
    print(c3.num_of_wins)




    """
    cando = election.find_Condorcet_candidate([5,0,0,2,6,0])
    candoo= election.determine_winner([5,0,0,2,6,0])
    if(cando != None):
        print(cando.name)
    print(c1.condorcet_wins)
    print(c2.condorcet_wins)
    print(c3.condorcet_wins)
    print(candoo.name)



   
    

    #election.find_Condorcet_candidate(election.possible_preference_schedules[0])
    #print(election.possible_preference_schedules[0])
    #print(c3.condorcet_points)

    
    cand_win = election.determine_winner(election.possible_preference_schedules[177])
    print(cand_win.name)

    print(election.possible_preference_schedules[177])
    print(c1.num_votes)
    print(c2.num_votes)
    print(c3.num_votes)
    """



if __name__ == '__main__':
    main()


