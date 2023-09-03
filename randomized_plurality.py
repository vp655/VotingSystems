#importing required libraries
import numpy as np
from itertools import *
import random as rand
import math


class Candidate:
    #constructor
    def __init__(self, name, num_votes=0):
        #member fields
        self.name = name
        self.num_votes = num_votes
        self.num_of_wins = 0
        self.condorcet_points = 0
        self.condorcet_wins = 0



class Plurality:
    def __init__(self, num_voters, num_cands, cand_objects):
        #member fields of the plurality class
        self.num_voters = num_voters
        self.num_cands = num_cands
        self.cand_objects = cand_objects
        self.cand_names = []
        self.comparisons = []
        self.possible_orders = []
        self.cwc_vio = 0

    #this function sets all the candidate names from the candidate objects
    def set_candidate_names(self):
        for cand in self.cand_objects:
            self.cand_names.append(cand.name)

    #this function generates all the possible orderings, calls set_candidate_names
    def generate_candidates_combos(self):
        self.set_candidate_names()
        #the following line can be computationally heavy - permutation of all the candidates
        self.possible_orders = list(permutations(self.cand_names))

    #this function takes in a preference schedule (list of numbers of length factorial(num_cands) and computes the winner
    def determine_winner(self, pref_schedule):
        #setting all candidate votes to 0
        for cand in self.cand_objects:
            cand.num_votes = 0
        count = 0
        #for each value in the preference schedule
        for val in pref_schedule:
            #the first one is the one getting votes
            cand_getting_votes = self.possible_orders[count][0]
            for cand in self.cand_objects:
                if (cand.name == cand_getting_votes):
                    cand.num_votes += val

            count += 1
        vote_array = []
        for cand in self.cand_objects:
            vote_array.append(cand.num_votes)
        #computes the index of the winner --> corresponding to index of the object
        index = self.most_votes_aliter(vote_array)
        #if there is an error, or if there is a tie
        if (index == -1):
            return None
        #returns the object
        return self.cand_objects[index]

    #finds which candidate has the most votes
    #if it is tied then choose randomly
    def most_votes_aliter(self, vote_array):
        max = -1
        max_index = -1
        are_we_tied = 0
        tied_index = []
        for i in range(0, len(vote_array)):
            if (vote_array[i] > max):
                max = vote_array[i]
                max_index = i
                tied_index.clear()
                tied_index.append(i)
                are_we_tied = 0
            elif (vote_array[i] == max):
                tied_index.append(i)
                are_we_tied = 1

        if (are_we_tied == 1):
            max_index = rand.choice(tied_index)
            # max_index = -1
            # if I wanted random ties, cut the -1 line and put in the rand_choice line

        return max_index

    def find_Condorcet_candidate(self, pref_schedule):
        for cand in self.cand_objects:
            cand.condorcet_wins = 0
        #gives all the possible comparisons between the two candidates
        self.comparisons = list(combinations(self.cand_names, 2))
        #for simple case gives [A,B] [B,C] [A,C]
        for comp in self.comparisons:
            cand_win_head_to_head = self.compare(comp, pref_schedule)
            if (cand_win_head_to_head == None):
                continue
            cand_win_head_to_head.condorcet_wins += 1
        for cand in self.cand_objects:
            if (cand.condorcet_wins == self.num_cands - 1):
                return cand
        return None

    def compare(self, comp, pref_schedule):
        cand1 = self.find_which_candidate_w_name(comp[0])
        cand2 = self.find_which_candidate_w_name(comp[1])
        for cand in self.cand_objects:
            cand.condorcet_points = 0
        for i in range(0, len(pref_schedule)):
            order = self.possible_orders[i]
            index_one = self.find_index_of(comp[0], order)
            index_two = self.find_index_of(comp[1], order)
            if (index_one < index_two):
                cand1.condorcet_points += pref_schedule[i]
            elif (index_one > index_two):
                cand2.condorcet_points += pref_schedule[i]
        if (cand1.condorcet_points > cand2.condorcet_points):
            return cand1
        elif (cand2.condorcet_points > cand1.condorcet_points):
            return cand2
        #if they have the same amount of points, then neither is a condorcet candidate
        elif (cand1.condorcet_points == cand2.condorcet_points):
            return None

    def find_which_candidate_w_name(self, name):
        for cand in self.cand_objects:
            if cand.name == name:
                return cand
        return 0

    def find_index_of(self, val, ordering):
        for i in range(0, len(ordering)):
            if (val == ordering[i]):
                return i
        return -1

    def find_all_winners(self, num_trials):
        for i in range(0,num_trials):
            pref_schedule = generate_IC_pref(self.num_voters, self.num_cands)
            #print(pref_schedule)
            cand_win = self.determine_winner(pref_schedule)
            cand_condorcet = self.find_Condorcet_candidate(pref_schedule)
            #if there is a Condorcet candidate
            if (cand_condorcet != None):
                #and no candidate wins
                if (cand_win == None):
                    self.cwc_vio += 1
                    #print("Violate")
                elif (cand_win.name != cand_condorcet.name):
                    self.cwc_vio += 1
                    #print("Violate")


def generate_IC_pref(num_voters, num_cands):
    poss_ranks = math.factorial(num_cands)
    arr = np.zeros(poss_ranks)
    for i in range(0,num_voters):
        ind = rand.randrange(0, poss_ranks)
        arr[ind] = arr[ind] + 1
    return arr




def main():
    number_of_voters = 100
    number_of_cands = 4
    list_of_cand_objects = []
    c1 = Candidate('A')
    c2 = Candidate('B')
    c3 = Candidate('C')
    c4 = Candidate('D')
    #c5 = Candidate('E')
    #c6 = Candidate('F')
    list_of_cand_objects.append(c1)
    list_of_cand_objects.append(c2)
    list_of_cand_objects.append(c3)
    list_of_cand_objects.append(c4)
    #list_of_cand_objects.append(c5)
    #list_of_cand_objects.append(c6)
    election = Plurality(number_of_voters,number_of_cands,list_of_cand_objects)
    election.generate_candidates_combos()
    election.find_all_winners(10000)
    print(election.cwc_vio)




if __name__ == '__main__':
    main()


