# importing required libraries
import numpy as np
from abc import ABC, abstractmethod
from itertools import *
import random as rand
import math
import time


class Candidate:
    # constructor for the candidate class
    def __init__(self, name, num_votes=0):
        # member fields
        self.name = name
        self.num_votes = num_votes
        self.condorcet_points = 0
        self.condorcet_wins = 0
        self.points = 0
        self.rank = 0


# abstract base class of the voting systems
class VotingSystem(ABC):
    def __init__(self, num_voters, num_cands, cand_objects):
        self.num_voters = num_voters
        self.num_cands = num_cands
        self.cand_objects = cand_objects  # these are the Candidates

        self.cand_names = []
        self.set_candidate_names()

        self.possible_orders = []
        self.generate_candidates_combos()

        self.comparisons = list(combinations(self.cand_names, 2))  # all the possible comparisons between candidates
        # gives all the possible comparisons between the two candidates
        # for simple case gives [A,B] [B,C] [A,C]
        self.cwc_vio = 0  # how many Condorcet winner criterion violations there are

        self.IIAv = 0

    # this function sets all the candidate names from the candidate objects
    def set_candidate_names(self):
        for cand in self.cand_objects:
            self.cand_names.append(cand.name)
        # print(self.cand_names)

    # this function generates all the possible orderings, calls set_candidate_names
    def generate_candidates_combos(self):
        # the following line can be computationally heavy - permutation of all the candidates
        self.possible_orders = list(permutations(self.cand_names))
        # print(self.possible_orders)


    def find_Condorcet_candidate(self, pref_schedule):
        for cand in self.cand_objects:
            cand.condorcet_wins = 0
        for comp in self.comparisons:
            cand_win_name = self.compare(comp, pref_schedule)
            if cand_win_name is None:
                continue
            else:
                cand_winner = self.find_which_candidate_w_name(cand_win_name)
                cand_winner.condorcet_wins += 1
        for cand in self.cand_objects:
            if cand.condorcet_wins == self.num_cands - 1:
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
            return cand1.name
        elif (cand2.condorcet_points > cand1.condorcet_points):
            return cand2.name
        # if they have the same amount of points, then neither is a condorcet candidate
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

    @abstractmethod
    def determine_winner(self, pref_schedule):
        pass

    @abstractmethod
    def create_societal_rank(self,pref_schedule):
        pass

    @abstractmethod
    def set_votes(self, pref_schedule):
        pass

    def find_all_winners(self, num_trials):
        for i in range(0, num_trials):

            pref_schedule = generate_IC_pref(self.num_voters, self.num_cands)
            # print(pref_schedule)
            # print(pref_schedule)
            cand_win = self.determine_winner(pref_schedule)
            cand_condorcet = self.find_Condorcet_candidate(pref_schedule)

            self.IIA(pref_schedule)


            # if there is a Condorcet candidate
            if cand_condorcet is not None:
                # print(cand_condorcet.name)
                # and no candidate wins
                if cand_win is None:
                    self.cwc_vio += 1
                    # print("Violate")
                elif cand_win.name != cand_condorcet.name:
                    self.cwc_vio += 1
                    # print("Violate")
                # print(cand_win.name)


    def IIA(self, pref_schedule):
        for comp in self.comparisons:
            winner = 0
            map_cand = self.create_societal_rank(pref_schedule)
            one = self.find_which_candidate_w_name(comp[0])
            two = self.find_which_candidate_w_name(comp[1])
            if(one.rank < two.rank):
                winner = 1
            elif(one.rank > two.rank):
                winner = 2

            self.compare(comp,pref_schedule)
            # we can use these local values
            one_c = one.condorcet_points
            two_c = two.condorcet_points


            for j in range(0,100):
                new_pref = self.generate_pref_srr(one, two, one_c, two_c)
                new_map = self.create_societal_rank(new_pref)  # this runs through every comparison
                # note that this calls member function that is defined in the derived class (is that good practice)
                if winner == 1 and (one.rank>=two.rank):
                    #print(one.name + " " + two.name)
                    #print(new_pref)
                    self.IIAv += 1
                    return
                elif winner == 2 and (one.rank<=two.rank):
                    #print(one.name + " " + two.name)
                    #print(new_pref)
                    self.IIAv += 1
                    return
                elif winner == 0 and (one.rank != two.rank):
                    #print(one.name + " " + two.name)
                    #print(new_pref)
                    self.IIAv += 1
                    return

    def generate_pref_srr(self,one, two, one_c, two_c):
        poss_ranks = math.factorial(self.num_cands)
        arr = np.zeros(poss_ranks,dtype = int)


        modified_cand = self.cand_objects[:]
        modified_cand.remove(one)
        modified_cand.remove(two)



        for i in range(0,one_c):
            ordering = [one.name,two.name]
            poss_insertions = 2
            for cand in modified_cand:
                choice = rand.randint(0,poss_insertions)
                ordering.insert(choice,cand.name)
            index = self.find_pref_in_all(tuple(ordering))

            arr[index] += 1
            poss_insertions += 1

        for i in range(0,two_c):
            ordering = [two.name,one.name]
            poss_insertions = 2
            for cand in modified_cand:
                choice = rand.randint(0,poss_insertions)
                ordering.insert(choice,cand.name)
            index = self.find_pref_in_all(tuple(ordering))

            arr[index] += 1
            poss_insertions += 1


        return(arr)

    def find_pref_in_all(self,pref_order):
        for i in range(0,len(self.possible_orders)):
            if pref_order == self.possible_orders[i]:
                return i






class Plurality(VotingSystem):

    def __init__(self, num_voters, num_cands, cand_objects):
        super().__init__(num_voters, num_cands, cand_objects)

    # this function takes in a preference schedule (list of numbers of length factorial(num_cands) and computes the winner

    def set_votes(self,pref_schedule):
        # setting all candidate votes to 0
        for cand in self.cand_objects:
            cand.num_votes = 0
        count = 0
        # for each value in the preference schedule
        for val in pref_schedule:
            # the first one is the one getting votes
            cand_getting_votes = self.possible_orders[count][0]
            for cand in self.cand_objects:
                if (cand.name == cand_getting_votes):
                    cand.num_votes += val

            count += 1

    def determine_winner(self, pref_schedule):

        societal_order = self.create_societal_rank(pref_schedule)
        num_top = len(societal_order[0])
        if(num_top==1):
            return societal_order[0][0]
        elif num_top > 1:
            cand_win = rand.choice(societal_order[0])
            return cand_win
        else:
            return None



    def create_societal_rank(self,pref_schedule):
        self.set_votes(pref_schedule)
        sorted_list = sorted(self.cand_objects,key=lambda v: v.num_votes, reverse = True)
        map_of_cands = {}
        #emulates do while
        count = 0
        previous = sorted_list[0].num_votes
        map_of_cands[count] = []
        #end of first iteration
        for cand in sorted_list:
            if(cand.num_votes == previous):
                map_of_cands[count].append(cand)
            else:
                count += 1
                map_of_cands[count] = []
                map_of_cands[count].append(cand)
            cand.rank = count



        return map_of_cands

    # change determine winner now
    # it calls create societal preference and then picks the first one
    # if the size is more than 1 of the list, random selection
    # return the candidate





class BordaCount(VotingSystem):

    def __init__(self, num_voters, num_cands, cand_objects):
        super().__init__(num_voters, num_cands, cand_objects)

    def set_votes(self,pref_schedule):
        for cand in self.cand_objects:
            cand.points = 0

        count = 0
        for val in pref_schedule:
            ordering = self.possible_orders[count]
            for i in range(0, self.num_cands):
                if (i == 0):
                    cand = self.find_which_candidate_w_name(ordering[0])
                    cand.num_votes += val
                # for consistency
                cand = self.find_which_candidate_w_name(ordering[i])
                cand.points += val * (self.num_cands - i)
            count += 1


    # this function takes in a preference schedule (list of numbers of length factorial(num_cands) and computes the winner
    def determine_winner(self, pref_schedule):

        societal_order = self.create_societal_rank(pref_schedule)
        num_top = len(societal_order[0])
        if (num_top == 1):
            return societal_order[0][0]
        elif num_top > 1:
            cand_win = rand.choice(societal_order[0])
            return cand_win
        else:
            return None

    def create_societal_rank(self,pref_schedule):
        self.set_votes(pref_schedule)
        sorted_list = sorted(self.cand_objects, key=lambda v: v.points, reverse=True)
        map_of_cands = {}
        # emulates do while
        count = 0
        previous = sorted_list[0].points
        map_of_cands[count] = []
        # end of first iteration
        for cand in sorted_list:
            if (cand.points == previous):
                map_of_cands[count].append(cand)
            else:
                count += 1
                map_of_cands[count] = []
                map_of_cands[count].append(cand)
            cand.rank = count

        return map_of_cands


    # this should ideally overload a method in the abstract class
    # then determine winner just first the first in societal pref order







class PairwiseComparison(VotingSystem):

    def __init__(self, num_voters, num_cands, cand_objects):
        super().__init__(num_voters, num_cands, cand_objects)

    def set_votes(self, pref_schedule):
        for cand in self.cand_objects:
            cand.num_votes = 0

        for comp in self.comparisons:
            cand_win_name = self.compare(comp, pref_schedule)
            if cand_win_name is None:
                for name in comp:
                    cand = self.find_which_candidate_w_name(name)
                    cand.num_votes += 0.5
            else:
                cand_win_head_to_head = self.find_which_candidate_w_name(cand_win_name)
                cand_win_head_to_head.num_votes += 1

    def create_societal_rank(self,pref_schedule):
            self.set_votes(pref_schedule)
            sorted_list = sorted(self.cand_objects, key=lambda v: v.num_votes, reverse=True)
            map_of_cands = {}
            # emulates do while
            count = 0
            previous = sorted_list[0].num_votes
            map_of_cands[count] = []
            # end of first iteration
            for cand in sorted_list:
                if (cand.num_votes == previous):
                    map_of_cands[count].append(cand)
                else:
                    count += 1
                    map_of_cands[count] = []
                    map_of_cands[count].append(cand)
                cand.rank = count

            return map_of_cands

    def determine_winner(self, pref_schedule):
        societal_order = self.create_societal_rank(pref_schedule)
        num_top = len(societal_order[0])
        if (num_top == 1):
            return societal_order[0][0]
        elif num_top > 1:
            cand_win = rand.choice(societal_order[0])
            return cand_win
        else:
            return None


# here make methods to generate an IAC one and an IANC one among other cultures


# then add more classes which inherit from voting systems and implement their own determine winner implementation


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
    arr = np.zeros(poss_ranks)  # this has num_cands! elements
    end_range = num_voters + poss_ranks - 1
    vals = rand.sample(range(0,end_range),poss_ranks-1)  # 5 random vals from 0 to 15 for example
    sorted_vals = sorted(vals)  # sort the values
    print(sorted_vals)
    arr[0] = sorted_vals[0]  # the first bar
    for i in range(1,len(sorted_vals)):
        arr[i] = sorted_vals[i] - sorted_vals[i-1] - 1
    arr[poss_ranks-1] = end_range - sorted_vals[poss_ranks-2] - 1

    return arr



def main():

    number_of_voters = 3
    number_of_cands = 3
    list_of_cand_objects = []
    c1 = Candidate('A')
    c2 = Candidate('B')
    c3 = Candidate('C')
    c4 = Candidate('D')

    list_of_cand_objects.append(c1)
    list_of_cand_objects.append(c2)
    list_of_cand_objects.append(c3)
    #list_of_cand_objects.append(c4)


    #election = Plurality(number_of_voters, number_of_cands, list_of_cand_objects)
    #election.find_all_winners(10000)
    #print(election.cwc_vio)
    #print(election.IIAv)



    #election2 = BordaCount(4, 3, list_of_cand_objects)
    #election2.find_all_winners(10000)
    #print(election2.cwc_vio)
    #print(election2.IIAv)


    pc = PairwiseComparison(30,3,list_of_cand_objects)
    pc.find_all_winners(10000)
    print(pc.cwc_vio)
    print(pc.IIAv)

    # IIA method may not be scaling up - test it


    #pc.IIA([1,0,0,0,2,0])
    #print(pc.IIAv)


    # Pariwise Comparison or Copeland should violate IIA every time - paper results not fully accurate



    #wow = generate_IAC_pref(400, 4)
    #print(wow)
    #print(sum(wow))



if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time()
    print(str(end - start) + "(s)")


