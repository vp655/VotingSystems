"""
This program models various voting systems. It calculates how often the voting systems violate certain social choice
criterion. Each Voting System is its own class, and is derived from the Voting Systems abstract base class. The checks
for the criterion are all in the Voting System class. Each derived class has its own method to determine the winner and
create a societal preference order. The simulations are run in the main function and the data gathered.
"""

# importing required libraries
import numpy as np
from abc import ABC, abstractmethod
from itertools import *
import random as rand
import math
import time
from sympy.utilities.iterables import multiset_permutations


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
        # for instant runoff
        self.round_elim = 0

        # for Coombs
        self.round_win = 0

        self.condorcet_losses = 0
        self.last_place_votes = 0

        self.greatest_pairwise_defeat = 0

    def __eq__(self,other):
        return self.name == other.name

    def __ge__(self,other):
        return self.rank >= other.rank


# abstract base class of the voting systems
class VotingSystem(ABC):
    def __init__(self, num_voters, num_cands, cand_objects):
        self.num_voters = num_voters
        self.num_cands = num_cands
        self.cand_objects = cand_objects  # these are the Candidates

        self.cand_names = []
        self.set_candidate_names()  # function that sets candidate names

        self.possible_orders = []
        self.generate_candidates_combos()  # generates all preference orders

        self.comparisons = list(combinations(self.cand_names, 2))
        self.three_element_comps = list(permutations(self.cand_names,3))
        # gives all the possible comparisons between the two candidates
        # for simple case gives [A,B] [B,C] [A,C]

        self.cwc_vio = 0  # how many Condorcet winner criterion violations there are
        self.clc_vio = 0
        self.IIAv = 0
        self.majority_vio = 0
        self.unam_vios = 0
        self.transitivity_vio = 0

        self.condorcet_count = 0

        self.joint = 0



        #self.test = []

    # this function sets all the candidate names from the candidate objects
    def set_candidate_names(self):
        for cand in self.cand_objects:
            self.cand_names.append(cand.name)

    # this function generates all the possible orderings
    def generate_candidates_combos(self):
        # the following line can be computationally heavy - permutation of all the candidate names
        self.possible_orders = list(permutations(self.cand_names))
        # for instance [(A,B,C),(A,C,B),(B,A,C),(B,C,A),(C,A,B),(C,B,A)]

    # this function finds the Condorcet candidate
    # returns None if it does not exist
    def find_Condorcet_candidate(self, pref_schedule):
        for cand in self.cand_objects:
            cand.condorcet_wins = 0
        for comp in self.comparisons:
            cand_winner = self.compare(comp, pref_schedule, self.possible_orders)
            if cand_winner is not None:
                cand_winner.condorcet_wins += 1
        for cand in self.cand_objects:
            if cand.condorcet_wins == self.num_cands - 1:
                self.condorcet_count += 1
                return cand
        return None

    # compares the two candidates to see which is preferred head to head
    # returns the name of the candidate that is more preferred, if tied returns None (empty string)
    def compare(self, comp, pref_schedule, ordering):
        cand1 = self.find_which_candidate_w_name(comp[0])
        cand2 = self.find_which_candidate_w_name(comp[1])
        # resets condorcet points for all candidates (just to be sure)
        for cand in self.cand_objects:
            cand.condorcet_points = 0
        for i in range(0, len(pref_schedule)):
            order = ordering[i]
            index_one = self.find_index_of(comp[0], order)
            index_two = self.find_index_of(comp[1], order)
            # whichever candidate has a lower index (more preferred) gets the condorcet_points
            if (index_one < index_two):
                cand1.condorcet_points += pref_schedule[i]
            elif (index_one > index_two):
                cand2.condorcet_points += pref_schedule[i]
        if (cand1.condorcet_points > cand2.condorcet_points):
            return cand1
        elif (cand2.condorcet_points > cand1.condorcet_points):
            return cand2
        # if they have the same amount of points, then neither is a condorcet candidate
        elif (cand1.condorcet_points == cand2.condorcet_points):
            return None

    def find_Condorcet_loser(self, pref_schedule):
        for cand in self.cand_objects:
            cand.condorcet_losses = 0
        for comp in self.comparisons:
            cand_loser = self.compare_loser(comp, pref_schedule, self.possible_orders)
            if cand_loser is not None:
                cand_loser.condorcet_losses += 1
        for cand in self.cand_objects:
            if cand.condorcet_losses == self.num_cands - 1:
                return cand
        return None


    def compare_loser(self, comp, pref_schedule, ordering):
        cand1 = self.find_which_candidate_w_name(comp[0])
        cand2 = self.find_which_candidate_w_name(comp[1])
        # resets condorcet points for all candidates (just to be sure)
        for cand in self.cand_objects:
            cand.condorcet_points = 0
        for i in range(0, len(pref_schedule)):
            order = ordering[i]
            index_one = self.find_index_of(comp[0], order)
            index_two = self.find_index_of(comp[1], order)
            # whichever candidate has a lower index (more preferred) gets the condorcet_points
            if (index_one < index_two):
                cand1.condorcet_points += pref_schedule[i]
            elif (index_one > index_two):
                cand2.condorcet_points += pref_schedule[i]
        if (cand1.condorcet_points < cand2.condorcet_points):
            return cand1
        elif (cand2.condorcet_points < cand1.condorcet_points):
            return cand2
        # if they have the same amount of points, then neither is a condorcet loser candidate
        elif (cand1.condorcet_points == cand2.condorcet_points):
            return None

    # helper functions
    def find_which_candidate_w_name(self, name):
        for cand in self.cand_objects:
            if cand.name == name:
                return cand
        return None

    def find_index_of(self, val, ordering):
        for i in range(0, len(ordering)):
            if (val == ordering[i]):
                return i
        return -1

    # abstract method that are implemented in the derived classes

    @abstractmethod
    def determine_winner(self, pref_schedule, cand_obj, poss_order):
        pass

    @abstractmethod
    def create_societal_rank(self,pref_schedule, cand_obj, poss_order):
        pass

    @abstractmethod
    def set_votes(self, pref_schedule, poss_order):
        pass

    @abstractmethod
    def type(self):
        pass




    def violates_condorcet(self, pref_schedule):
        cand_win = self.determine_winner(pref_schedule, self.cand_objects, self.possible_orders)
        cand_condorcet = self.find_Condorcet_candidate(pref_schedule)

        # compares the winner and the condorcet winner (using derived class implementation)
        # if there is a Condorcet candidate
        if cand_condorcet is not None:
            # and no candidate wins
            if cand_win is None:  # can potentially have no winner if we return None in case of ties
                # instead of randomly breaking the tie
                return True
            elif cand_win.name != cand_condorcet.name:
                return True

        return False


    # function generates random preference schedules in accordance to distribution then finds all condorcet violations
    # appends the member variable
    def find_condorcet_vios(self, num_trials, distribution, weights = None):
        self.cwc_vio = 0 # to have multiple runs
        for i in range(0, num_trials):
            pref_schedule = []
            if distribution == "IC":
                pref_schedule = generate_IC_pref(self.num_voters, self.num_cands)
            elif distribution == "IAC":
                pref_schedule = generate_IAC_pref(self.num_voters, self.num_cands)
            elif distribution == "Custom":
                pref_schedule = custom_distribution(self.num_voters, self.num_cands, weights)

            vio_cond = self.violates_condorcet(pref_schedule)
            if(vio_cond):
                #print(pref_schedule)
                self.cwc_vio += 1


    def violates_condorcet_loser(self, pref_schedule):
        cand_win = self.determine_winner(pref_schedule, self.cand_objects, self.possible_orders)
        cand_condorcet_loser = self.find_Condorcet_loser(pref_schedule)

        # if there is no winner, it is impossible for the Condorcet loser to be elected
        if cand_win is None:
            return False


        # compares the winner and the condorcet winner (using derived class implementation)
        # if there is a Condorcet candidate
        if cand_condorcet_loser is not None:
            #if cand_condorcet_loser.num_votes == cand_win.num_votes:
            # and no candidate wins
            if cand_win.name == cand_condorcet_loser.name:
                #print(pref_schedule)
                return True
        return False


    def violates_condorcet_loser_paper(self, pref_schedule):
        cand_win = self.determine_winner(pref_schedule, self.cand_objects, self.possible_orders)
        cand_condorcet_loser = self.find_Condorcet_loser(pref_schedule)

        # if there is no winner, it is impossible for the Condorcet loser to be elected
        if cand_win is None:
            return False


        # compares the winner and the condorcet winner (using derived class implementation)
        # if there is a Condorcet candidate
        if cand_condorcet_loser is not None:
            if cand_condorcet_loser.num_votes == cand_win.num_votes:
            # and no candidate wins
            #if cand_win.name == cand_condorcet_loser.name:
                #print(pref_schedule)
                return True
        return False

    def find_condorcet_loser_vios(self, num_trials, distribution, weights = None):
        for i in range(0, num_trials):
            pref_schedule = []
            if distribution == "IC":
                pref_schedule = generate_IC_pref(self.num_voters, self.num_cands)
            elif distribution == "IAC":
                pref_schedule = generate_IAC_pref(self.num_voters, self.num_cands)
            elif distribution == "Custom":
                pref_schedule = custom_distribution(self.num_voters, self.num_cands, weights)

            #print(pref_schedule)
            vio_cond_loser = self.violates_condorcet_loser(pref_schedule)
            if(vio_cond_loser):
                #self.test.append(pref_schedule)
                self.clc_vio += 1




    def find_joint_violations(self, num_trials, distribution, weights = None):
        for i in range(0, num_trials):
            pref_schedule = []
            if distribution == "IC":
                pref_schedule = generate_IC_pref(self.num_voters, self.num_cands)
            elif distribution == "IAC":
                pref_schedule = generate_IAC_pref(self.num_voters, self.num_cands)
            elif distribution == "Custom":
                pref_schedule = custom_distribution(self.num_voters, self.num_cands, weights)

            cwc_vio = self.violates_condorcet(pref_schedule)
            if (cwc_vio):
                self.joint += 1
                continue
            ivio = self.violates_IIA(pref_schedule)
            if (ivio):
                #self.joint += 1
                continue
            clc_vio = self.violates_condorcet_loser(pref_schedule)
            if (clc_vio):
                self.joint += 1
                continue
            unm_vio = self.violates_unanimity(pref_schedule)
            if (unm_vio):
                self.joint += 1
                continue
            m_vio = self.violates_majority(pref_schedule)
            if (m_vio):
                self.joint += 1
                continue





    # similar to condorcet function, but this time finds IIA violations for certain range of num_trials
    def find_IIA_violations(self, num_trials, distribution, weights = None):
        self.IIAv = 0
        for i in range(0, num_trials):
            pref_schedule = []
            if distribution == "IC":
                pref_schedule = generate_IC_pref(self.num_voters, self.num_cands)
            elif distribution == "IAC":
                pref_schedule = generate_IAC_pref(self.num_voters, self.num_cands)
            elif distribution == "Custom":
                pref_schedule = custom_distribution(self.num_voters, self.num_cands, weights)

            ivio = self.violates_IIA_paper(pref_schedule)
            if(ivio):
                self.IIAv += 1
                print(pref_schedule)
            #else:
                #if 2 not in pref_schedule:
                 #   print(pref_schedule)

    # exact same as in plurality
    def simple_set(self,pref_schedule, poss_order):
        for cand in self.cand_objects:
            cand.num_votes = 0
        count = 0
        for val in pref_schedule:
            name_of_cand_getting_votes = poss_order[count][0]
            cand_get_votes = self.find_which_candidate_w_name(name_of_cand_getting_votes)
            cand_get_votes.num_votes += val
            count += 1


    def find_major_cand(self, pref_schedule):
        self.simple_set(pref_schedule, self.possible_orders)
        for cand in self.cand_objects:
            if(cand.num_votes > (self.num_voters/2)):
                return cand
        return None


    def violates_majority(self,pref_schedule):
        major_winner = self.find_major_cand(pref_schedule)
        real_winner = self.determine_winner(pref_schedule, self.cand_objects, self.possible_orders)
        if major_winner is not None:
            if major_winner.name != real_winner.name:
                return True
        return False


    def find_majority_violations(self, num_trials, distribution, weights = None):
        for i in range(0, num_trials):
            pref_schedule = []
            if distribution == "IC":
                pref_schedule = generate_IC_pref(self.num_voters, self.num_cands)
            elif distribution == "IAC":
                pref_schedule = generate_IAC_pref(self.num_voters, self.num_cands)
            elif distribution == "Custom":
                pref_schedule = custom_distribution(self.num_voters, self.num_cands, weights)

            vios_major = self.violates_majority(pref_schedule)
            if(vios_major):
                self.majority_vio += 1






    # this can be solely in the python model, that is fine

    # implements the IIA algorithm described in the paper found at link below
    # https://www.sciencedirect.com/science/article/pii/S0176268020300847
    def violates_IIA_paper(self, pref_schedule):
        IIA_violated = False
        for comp in self.comparisons:
            winner = 0
            map_cand = self.create_societal_rank(pref_schedule, self.cand_objects, self.possible_orders)
            one = self.find_which_candidate_w_name(comp[0])
            two = self.find_which_candidate_w_name(comp[1])
            # finds which candidate in comparison is more highly ranked (winner stays 0 if they are the same)
            if (one.rank < two.rank):
                winner = 1
            elif (one.rank > two.rank):
                winner = 2

            # this approach gives us all the candidates not in the comparison
            # however taking the name of the first name in modified cand only works with 3 candidates
            # need to find a way to make the algorithm scale for more candidates
            modified_cand = self.cand_objects[:]
            modified_cand.remove(one)
            modified_cand.remove(two)
            cand_name = modified_cand[0].name

            # moving C up and down 1 and 2 times
            poss_pref1 = self.move_up(self.possible_orders, cand_name, 1, one, two)
            vio1 = self.check_vio(pref_schedule, winner, one, two, poss_pref1)
            if(vio1 == True):
                IIA_violated = True
                break

            poss_pref2 = self.move_up(self.possible_orders, cand_name, 2, one, two)
            vio2 = self.check_vio(pref_schedule, winner, one, two, poss_pref2)
            if (vio2 == True):
                IIA_violated = True
                break

            poss_pref3 = self.move_down(self.possible_orders, cand_name, 1, one, two)
            vio3 = self.check_vio(pref_schedule, winner, one, two, poss_pref3)
            if (vio3 == True):
                IIA_violated = True
                break

            poss_pref4 = self.move_down(self.possible_orders, cand_name, 2, one, two)
            vio4 = self.check_vio(pref_schedule, winner, one, two, poss_pref4)
            if (vio4 == True):
                IIA_violated = True
                break

            # moving the pair being compared up and down 1 spot, first one then two
            poss_pref5 = self.move_up(self.possible_orders, one.name, 1, one, two)
            vio5 = self.check_vio(pref_schedule, winner, one, two, poss_pref5)
            if (vio5 == True):
                IIA_violated = True
                break

            poss_pref6 = self.move_down(self.possible_orders, one.name, 1, one, two)
            vio6 = self.check_vio(pref_schedule, winner, one, two, poss_pref6)
            if (vio6 == True):
                IIA_violated = True
                break

            poss_pref7 = self.move_up(self.possible_orders, two.name, 1, one, two)
            vio7 = self.check_vio(pref_schedule, winner, one, two, poss_pref7)
            if (vio7 == True):
                IIA_violated = True
                break

            poss_pref8 = self.move_down(self.possible_orders, two.name, 1, one, two)
            vio8 = self.check_vio(pref_schedule, winner, one, two, poss_pref8)
            if (vio8 == True):
                IIA_violated = True
                break

            # carrying out the simultaneous moves in two separate passes as described in the paper
            poss_pref9 = self.sim_move_1(winner, one, two)
            vio9 = self.check_vio(pref_schedule, winner, one, two, poss_pref9)
            if (vio9 == True):
                IIA_violated = True
                break

            poss_pref10 = self.sim_move_2(winner, one, two)
            vio10 = self.check_vio(pref_schedule, winner, one, two, poss_pref10)
            if (vio10 == True):
                IIA_violated = True
                break

        # good test to see which pref_schedules do not violate IIA
        return IIA_violated
        #if(violated==False):
         #  print(pref_schedule)


    # function takes an ordering and moves the candidate with cand_name up for every order
    # one and two are also parameters due to conditions of IIA (they cannot swap)
    # I could make move_up separate and overload it as well to get a move general function
    def move_up(self, ordering, cand_name, amt, one, two):

        new_pref = []
        copy_of_orders = ordering[:]
        for pref_order in copy_of_orders:
            list_order = list(pref_order)
            idx = list_order.index(cand_name)
            # this checking of one and two works only in the case of three candidates
            # it can be extended to more
            if (cand_name == one.name):
                idx_rival = list_order.index(two.name)
                if((idx_rival+1) == idx):
                    new_pref.append(tuple(list_order))
                    continue
            elif(cand_name == two.name):
                idx_rival = list_order.index(one.name)
                if ((idx_rival + 1) == idx):
                    new_pref.append(tuple(list_order))
                    continue

            if (idx >= amt):
                list_order.remove(cand_name)
                list_order.insert(idx - amt, cand_name)
            else:
                list_order.remove(cand_name)
                list_order.insert(0, cand_name)
            new_pref.append(tuple(list_order))
        return new_pref

    # analogous logic to move_up
    def move_down(self, ordering,  cand_name, amt, one, two):
        new_pref = []
        end = len(ordering) - 1
        copy_of_orders = ordering[:]
        for pref_order in copy_of_orders:
            list_order = list(pref_order)
            idx = list_order.index(cand_name)
            if (cand_name == one.name):
                idx_rival = list_order.index(two.name)
                if((idx_rival-1) == idx):
                    new_pref.append(tuple(list_order))
                    continue
            elif(cand_name == two.name):
                idx_rival = list_order.index(one.name)
                if ((idx_rival - 1) == idx):
                    new_pref.append(tuple(list_order))
                    continue
            if (idx <= (end - amt)):
                list_order.remove(cand_name)
                list_order.insert(idx + amt, cand_name)
            else:
                list_order.remove(cand_name)
                list_order.insert(end, cand_name)
            new_pref.append(tuple(list_order))
        return new_pref

    # implements the two specific simultaneous moves (more preferred down and less up) that the paper suggests

    def sim_move_1(self, winner,one, two):
        mpref_alt = None
        lpref_alt = None
        if(winner == 1):
            mpref_alt = one
            lpref_alt = two
        if(winner == 2):
            mpref_alt = two
            lpref_alt = one
        if(winner ==0):
            return self.possible_orders

        initial = self.move_down(self.possible_orders, mpref_alt.name, 1, one, two)
        final = self.move_up(initial, lpref_alt.name, 1, one, two)
        return final

    def sim_move_2(self, winner,one, two):
        mpref_alt = None
        lpref_alt = None
        if(winner == 1):
            mpref_alt = one
            lpref_alt = two
        if(winner == 2):
            mpref_alt = two
            lpref_alt = one
        if(winner ==0):
            return self.possible_orders

        initial = self.move_up(self.possible_orders, lpref_alt.name, 1, one, two)
        final = self.move_down(initial, mpref_alt.name, 1, one, two)
        return final



    # checks whether preference schedule has IIA violation
    def check_vio(self, pref_sc, winner, one, two, poss_pref):
        # creates the new societal preference order from the new preference schedule
        new_map = self.create_societal_rank(pref_sc, self.cand_objects,poss_pref)
        # for instance if the winner was one but now one is ranked equally or lower than two
        if winner == 1 and (one.rank >= two.rank):
            return True
        elif winner == 2 and (one.rank <= two.rank):
            return True
        elif winner == 0 and (one.rank != two.rank):
            return True
        return False




    # IIA aliter implemented which eliminates all candidates not in pair
    # not very efficient or effective
    # what you can do is add a case where we only eliminate candidates if they are truly irrevelant
    # as in if they get less than 10% of the vote
    # threshold can be a parameter here
    # but that would create even fewer IIA violations

    def IIA_aliter(self, pref_schedule):
        for comp in self.comparisons:
            winner = 0
            map_cand = self.create_societal_rank(pref_schedule, self.cand_objects, self.possible_orders)
            one = self.find_which_candidate_w_name(comp[0])
            two = self.find_which_candidate_w_name(comp[1])
            if (one.rank < two.rank):
                winner = 1
            elif (one.rank > two.rank):
                winner = 2
            to_use_cand = []
            to_use_cand.append(one)
            to_use_cand.append(two)
            modified_cand = self.cand_objects[:]
            modified_cand.remove(one)
            modified_cand.remove(two)
            copy_of_prefs = self.eliminate_cands(self.possible_orders,modified_cand[0].name)
            new_map = self.create_societal_rank(pref_schedule,to_use_cand,copy_of_prefs)
            if winner == 1 and (one.rank >= two.rank):
                self.IIAv += 1
                return
            elif winner == 2 and (one.rank <= two.rank):
                self.IIAv += 1
                return
            elif winner == 0 and (one.rank != two.rank):
                self.IIAv += 1

    # function that eliminates the candidate from a preference schedule
    # it takes in the ordering and eliminates element from each 'column' of the ordering
    def eliminate_cands(self, ordering, name_to_elim):
        copy_of_prefs = ordering[:]
        to_return_pref = []
        for pref_order in copy_of_prefs:
            list_pref = list(pref_order)
            list_pref.remove(name_to_elim)
            to_return_pref.append(tuple(list_pref))
        return to_return_pref







    # this is another algorithm to compute IIA violation for a given preference schedule
    # it generates 100 preference schedules where all the voters have the same relative ranking of a certain pair
    # if the societal ranking of the pair changes then there exists an IIA violation
    # can increase 100 to greater value if I want to catch more violations
    def violates_IIA(self, pref_schedule):
        for comp in self.comparisons:
            winner = 0
            map_cand = self.create_societal_rank(pref_schedule, self.cand_objects, self.possible_orders)
            one = self.find_which_candidate_w_name(comp[0])
            two = self.find_which_candidate_w_name(comp[1])
            if(one.rank < two.rank):
                winner = 1
            elif(one.rank > two.rank):
                winner = 2

            self.compare(comp,pref_schedule, self.possible_orders)
            # we use these local values since we call compare again and Condorcet winner changes
            # compare is called again in create societal rank function (I think specifically for Copeland?)
            one_c = one.condorcet_points
            two_c = two.condorcet_points

            # increasing this would increase percentages of violations caught at the cost of speed
            for j in range(0,300):

                new_pref = self.generate_pref_srr_v2(one, two, one_c, two_c)  # get a new pref with same relative ranks
                new_map = self.create_societal_rank(new_pref, self.cand_objects, self.possible_orders)
                # checks if the relative rank changed
                if winner == 1 and (one.rank>=two.rank):
                    return True
                elif winner == 2 and (one.rank<=two.rank):
                    return True
                elif winner == 0 and (one.rank != two.rank):
                    return True

        # good testing statement to see which pref_sc do not violate or 'slipped through'
        #print(pref_schedule)
        return False



    def generate_pref_srr(self,one, two, one_c, two_c):
        poss_ranks = math.factorial(self.num_cands)
        arr = np.zeros(poss_ranks,dtype = int)

        modified_cand = self.cand_objects[:]  # shallow copy
        modified_cand.remove(one)
        modified_cand.remove(two)

        # algorithm to generate a preference schedule with same relative rankings
        # starts with [A,B] --> then randomly inserts C into any index from 0 to 2, then inserts D, etc.
        for i in range(0,one_c):
            ordering = [one.name,two.name]
            poss_insertions = 2
            for cand in modified_cand:
                choice = rand.randint(0,poss_insertions)
                ordering.insert(choice,cand.name)
                poss_insertions += 1 # we need to increment this here, new candidate means one more slot (case of 4)
            index = self.find_pref_in_all(tuple(ordering))
            arr[index] += 1

        # does the same with all the voters who chose [B,A]
        for i in range(0,two_c):
            ordering = [two.name,one.name]
            poss_insertions = 2
            for cand in modified_cand:
                choice = rand.randint(0,poss_insertions)
                ordering.insert(choice,cand.name)
                poss_insertions += 1
            index = self.find_pref_in_all(tuple(ordering))
            arr[index] += 1

        return(arr)

    # finds which preference order in self.preference orders the ordering corresponds to
    def find_pref_in_all(self,pref_order):
        for i in range(0,len(self.possible_orders)):
            if pref_order == self.possible_orders[i]:
                return i

    # this is another method to create a new preference schedule that preserves the relative ranking of A and B
    # this one treats all preference schedules as equally likely
    # there are the same number of voters preferring A over B and B over A --> does not matter which voters
    def generate_pref_srr_v2(self, one, two, one_c, two_c):

        poss_ranks = len(self.possible_orders)
        arr = np.zeros(poss_ranks, dtype=int)  # this is the array we want to return

        o_index = self.find_index_first_g_second(one, two)  # all indexes where one is greater than two relatively
        t_index = self.find_index_first_g_second(two, one)  # analogous logic for two
        orders_one_g_two = poss_ranks / 2
        num_bounds = int(orders_one_g_two) - 1

        # this uses the 'IAC' method to generate random numbers
        # needs (num_bounds + 1) random numbers that sum to one_c and two_c
        end_range1 = num_bounds + one_c
        end_range2 = num_bounds + two_c


        # setting the values for the first candidate in comparison
        temp_arr = np.zeros(int(orders_one_g_two), dtype=int)
        vals = rand.sample(range(0, end_range1), num_bounds)  # 2 random vals from 0 to 7 for example (one_c = 6)
        sorted_vals = sorted(vals)  # sort the values
        temp_arr[0] = sorted_vals[0]  # the first bar
        for i in range(1, len(sorted_vals)):
            temp_arr[i] = sorted_vals[i] - sorted_vals[i - 1] - 1
        temp_arr[len(sorted_vals)] = end_range1 - sorted_vals[len(sorted_vals) - 1] - 1  # the last bar

        for i in range(0, len(o_index)):
            arr[o_index[i]] = temp_arr[i]

        # same logic but for B>A
        # setting the values for the second candidate in comparison
        temp_arr2 = np.zeros(int(orders_one_g_two), dtype=int)
        vals2 = rand.sample(range(0, end_range2), num_bounds)
        sorted_vals2 = sorted(vals2)  # sort the values
        temp_arr2[0] = sorted_vals2[0]  # the first bar
        for i in range(1, len(sorted_vals2)):
            temp_arr2[i] = sorted_vals2[i] - sorted_vals2[i - 1] - 1
        temp_arr2[len(sorted_vals2)] = end_range2 - sorted_vals2[len(sorted_vals2) - 1] - 1
        for i in range(0, len(t_index)):
            arr[t_index[i]] = temp_arr2[i]

        return arr





    # finds all indices where the first candidate is greater than the second candidate in the ordering
    def find_index_first_g_second(self, first, second):
        index_g = []
        for i in range(0,len(self.possible_orders)):
            pref_order = self.possible_orders[i]
            first_i = self.find_index_of(first.name,pref_order)
            second_i = self.find_index_of(second.name,pref_order)
            if(first_i < second_i):
                index_g.append(i)
        return index_g


    def find_unanimity_vios(self,num_trials, distribution, weights=None):
        for i in range(0, num_trials):
            pref_schedule = []
            if distribution == "IC":
                pref_schedule = generate_IC_pref(self.num_voters, self.num_cands)
            elif distribution == "IAC":
                pref_schedule = generate_IAC_pref(self.num_voters, self.num_cands)
            elif distribution == "Custom":
                pref_schedule = custom_distribution(self.num_voters, self.num_cands, weights)

            vios = self.violates_unanimity(pref_schedule)
            if(vios):
                self.unam_vios += 1


    def violates_unanimity(self, preference_schedule):
        for comp in self.comparisons:
            one = self.find_which_candidate_w_name(comp[0])
            two = self.find_which_candidate_w_name(comp[1])
            self.create_societal_rank(preference_schedule,self.cand_objects, self.possible_orders)
            # now we have relative ranking of one and two
            one_r = one.rank
            two_r = two.rank
            self.compare(comp,preference_schedule,self.possible_orders)
            if(one.condorcet_points == self.num_voters):
                if(one_r >= two_r):
                    #print(preference_schedule)
                    return True
            elif(two.condorcet_points == self.num_voters):
                if(two_r >= one_r):
                    #print(preference_schedule)
                    return True
        return False



    def find_transitivity_vios(self,num_trials, distribution, weights=None):
        for i in range(0, num_trials):
            pref_schedule = []
            if distribution == "IC":
                pref_schedule = generate_IC_pref(self.num_voters, self.num_cands)
            elif distribution == "IAC":
                pref_schedule = generate_IAC_pref(self.num_voters, self.num_cands)
            elif distribution == "Custom":
                pref_schedule = custom_distribution(self.num_voters, self.num_cands, weights)

            vios = False
            if self.type() == "Pairwise Majority":
                vios = self.pairwise_majority_violates_transitivity(pref_schedule) # this is for pairwise majority
                violin = self.pairwise_majority_violates_transitivity_strict(pref_schedule)
                if((violin == True) and (vios == False)):
                    print(pref_schedule)
            else:
                vios = self.violates_transitivity_real(pref_schedule)

            if(vios):
                #print(pref_schedule)
                self.transitivity_vio += 1



    def violates_transitivity_real(self, pref_schedule):
        for comp in self.three_element_comps:
            # get the three candidates for comparison
            one = self.find_which_candidate_w_name(comp[0])
            two = self.find_which_candidate_w_name(comp[1])
            three = self.find_which_candidate_w_name(comp[2])
            self.create_societal_rank(pref_schedule, self.cand_objects, self.possible_orders)
            if(one.rank<=two.rank and two.rank<=three.rank):
                if(one.rank > three.rank):
                    return True
        return False

    # pairwise majority satisfies all the other criterion, this is the only one we need to check
    def pairwise_majority_violates_transitivity(self, pref_schedule):

        if (self.find_Condorcet_candidate(pref_schedule) is not None): # the find condorcet candidates function actually appends condorcet count

            #need documentation

            summer = 1
            #self.condorcet_count += 1
        # checks to find a condorcet cycle in each three element subset
        for comp in self.three_element_comps:
            # get the three candidates for comparison
            one = self.find_which_candidate_w_name(comp[0])
            two = self.find_which_candidate_w_name(comp[1])
            three = self.find_which_candidate_w_name(comp[2])
            self.compare([comp[0], comp[1]], pref_schedule, self.possible_orders)
            if (one.condorcet_points >= two.condorcet_points):  # I defined the relational operator in the class
                self.compare([comp[1], comp[2]], pref_schedule, self.possible_orders)
                if (two.condorcet_points >= three.condorcet_points):
                    self.compare([comp[0], comp[2]], pref_schedule, self.possible_orders)
                    if ((one.condorcet_points >= three.condorcet_points) == False):
                        return True
        return False


    def pairwise_majority_violates_transitivity_strict(self, pref_schedule):

        #if (self.find_Condorcet_candidate(pref_schedule) is not None):
        #    return False
        # checks to find a condorcet cycle in each three element subset
        for comp in self.three_element_comps:
            # get the three candidates for comparison
            one = self.find_which_candidate_w_name(comp[0])
            two = self.find_which_candidate_w_name(comp[1])
            three = self.find_which_candidate_w_name(comp[2])
            self.compare([comp[0], comp[1]], pref_schedule, self.possible_orders)
            if (one.condorcet_points >= two.condorcet_points):  # I defined the relational operator in the class
                self.compare([comp[1], comp[2]], pref_schedule, self.possible_orders)
                if (two.condorcet_points > three.condorcet_points):
                    self.compare([comp[0], comp[2]], pref_schedule, self.possible_orders)
                    if ((one.condorcet_points > three.condorcet_points) == False):
                        return True
        return False










# start of derived classes (each one represents a voting system)
# can make these in a different file - especially in C++ (each with its own header file and cpp file)



class Plurality(VotingSystem):

    def __init__(self, num_voters, num_cands, cand_objects):
        super().__init__(num_voters, num_cands, cand_objects)

    # this function takes in a preference schedule (list of numbers of length factorial(num_cands) and computes the winner

    def set_votes(self,pref_schedule, poss_order):
        # setting all candidate votes to 0
        for cand in self.cand_objects:
            cand.num_votes = 0
        count = 0
        # for each value in the preference schedule
        for val in pref_schedule:
            # the first one is the one getting votes
            name_of_cand_getting_votes = poss_order[count][0]
            # using find candidate with name function here
            cand_get_votes = self.find_which_candidate_w_name(name_of_cand_getting_votes)
            cand_get_votes.num_votes += val
            count += 1

    def determine_winner(self, pref_schedule, cand_obj, poss_order):

        societal_order = self.create_societal_rank(pref_schedule,cand_obj, poss_order)
        num_top = len(societal_order[0])
        if(num_top==1):
            return societal_order[0][0]
        elif num_top > 1:
            cand_win = rand.choice(societal_order[0])
            return cand_win
        else:
            return None



    def create_societal_rank(self,pref_schedule, cand_obj, poss_order):
        self.set_votes(pref_schedule, poss_order)
        sorted_list = sorted(cand_obj,key=lambda v: v.num_votes, reverse = True)
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
            previous = cand.num_votes
            cand.rank = count



        return map_of_cands


    def type(self):
        return "Plurality"



class BordaCount(VotingSystem):

    def __init__(self, num_voters, num_cands, cand_objects):
        super().__init__(num_voters, num_cands, cand_objects)

    def set_votes(self,pref_schedule, poss_order):
        for cand in self.cand_objects:
            cand.points = 0
            cand.num_votes = 0

        count = 0
        for val in pref_schedule:
            ordering = poss_order[count]
            # this could cause error is poss_order has eliminated cands (made change in other systems)
            for i in range(0, self.num_cands):
                if (i == 0):
                    cand = self.find_which_candidate_w_name(ordering[0])
                    cand.num_votes += val
                # for consistency
                cand = self.find_which_candidate_w_name(ordering[i])
                cand.points += val * (self.num_cands - i)
            count += 1


    # this function takes in a preference schedule (list of numbers of length factorial(num_cands) and computes the winner
    def determine_winner(self, pref_schedule,cand_obj, poss_order):

        societal_order = self.create_societal_rank(pref_schedule, cand_obj, poss_order)
        num_top = len(societal_order[0])
        if (num_top == 1):
            return societal_order[0][0]
        elif num_top > 1:
            cand_win = rand.choice(societal_order[0])
            return cand_win
        else:
            return None

    def create_societal_rank(self,pref_schedule, cand_obj, poss_order):
        self.set_votes(pref_schedule, poss_order)
        sorted_list = sorted(cand_obj, key=lambda v: v.points, reverse=True)
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
            previous = cand.points
            cand.rank = count

        return map_of_cands



    def type(self):
        return "Borda Count"




class TruncatedBorda(VotingSystem):

    def __init__(self, num_voters, num_cands, cand_objects, num_rank):
        super().__init__(num_voters, num_cands, cand_objects)
        self.num_rank = num_rank


    def set_votes(self,pref_schedule, poss_order):
        for cand in self.cand_objects:
            cand.points = 0
            cand.num_votes = 0

        count = 0
        for val in pref_schedule:
            ordering = poss_order[count]
            for i in range(0,self.num_rank):
                if (i == 0):
                    cand = self.find_which_candidate_w_name(ordering[0])
                    cand.num_votes += val
                # for consistency
                cand = self.find_which_candidate_w_name(ordering[i])
                cand.points += val * (self.num_rank - i)
            count += 1




    # this function takes in a preference schedule (list of numbers of length factorial(num_cands) and computes the winner
    def determine_winner(self, pref_schedule,cand_obj, poss_order):

        societal_order = self.create_societal_rank(pref_schedule, cand_obj, poss_order)
        num_top = len(societal_order[0])
        if (num_top == 1):
            return societal_order[0][0]
        elif num_top > 1:
            cand_win = rand.choice(societal_order[0])
            return cand_win
        else:
            return None

    def create_societal_rank(self,pref_schedule, cand_obj, poss_order):
        self.set_votes(pref_schedule, poss_order)
        sorted_list = sorted(cand_obj, key=lambda v: v.points, reverse=True)
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
            previous = cand.points
            cand.rank = count

        return map_of_cands



    def type(self):
        return "Truncated Borda Count"







class InstantRunoff(VotingSystem):

    def __init__(self, num_voters, num_cands, cand_objects):
        super().__init__(num_voters, num_cands, cand_objects)
        self.candidates_remaining = self.cand_objects[:]
        self.current_pref_table = self.possible_orders[:]
        self.elec_round = 1

    # takes the same function as plurality
    def set_votes(self, pref_schedule, poss_order):
        # setting all candidate votes to 0
        for cand in self.cand_objects:
            cand.num_votes = 0
        count = 0
        # for each value in the preference schedule
        for val in pref_schedule:
            # the first one is the one getting votes
            name_of_cand_getting_votes = poss_order[count][0]
            # using find candidate with name function here
            cand_get_votes = self.find_which_candidate_w_name(name_of_cand_getting_votes)
            cand_get_votes.num_votes += val
            count += 1


    def run_election(self,pref_schedule, cand_obj, poss_order):

        if(len(cand_obj)==0):
            return
        else:
            self.set_votes(pref_schedule, poss_order)
            cands_to_elim = self.find_candidates_with_lowest(cand_obj)
            for cand in cands_to_elim:
                cand.round_elim = self.elec_round
                poss_order = self.eliminate_cands(poss_order, cand.name)
                cand_obj.remove(cand)
            self.elec_round += 1
            self.run_election(pref_schedule,cand_obj, poss_order)

    def find_candidates_with_lowest(self, cand_obj):
        cands_with_least_votes = []
        # this gets the candidates with the minimum votes and then take the votes of that candidate
        # a better way to do that may be to sort them and take the 0th ones votes
        # that may also save time
        cand_with_min = min(cand_obj, key=lambda v:v.num_votes)
        least_vote = cand_with_min.num_votes
        for cand in cand_obj:
            if cand.num_votes == least_vote:
                cands_with_least_votes.append(cand)
        return cands_with_least_votes


    def create_societal_rank(self, pref_schedule, cand_obj, poss_order):
        cand_process = cand_obj[:]
        self.elec_round = 1 #adding this so it does not add up to 20000 rounds
        self.run_election(pref_schedule, cand_process, poss_order)
        sorted_list = sorted(cand_obj, key=lambda v: v.round_elim, reverse=True)
        map_of_cands = {}
        # emulates do while
        count = 0
        previous = sorted_list[0].round_elim
        map_of_cands[count] = []
        # end of first iteration
        for cand in sorted_list:
            if (cand.round_elim == previous):
                map_of_cands[count].append(cand)
            else:
                count += 1
                map_of_cands[count] = []
                map_of_cands[count].append(cand)
            previous = cand.round_elim
            cand.rank = count

        return map_of_cands










    def determine_winner(self, pref_schedule, cand_obj, poss_order):
        cand_obj = cand_obj[:]  # I do not want to modify the actual self.cand_objects
        societal_order = self.create_societal_rank(pref_schedule, cand_obj, poss_order)
        num_top = len(societal_order[0])
        if (num_top == 1):
            return societal_order[0][0]
        elif num_top > 1:
            cand_win = rand.choice(societal_order[0])
            return cand_win
        else:
            return None



    def type(self):
        return "Instant Runoff"





class Coombs(VotingSystem):

    def __init__(self, num_voters, num_cands, cand_objects):
        super().__init__(num_voters, num_cands, cand_objects)
        self.candidates_remaining = self.cand_objects[:]
        self.current_pref_table = self.possible_orders[:]
        self.elec_round = 1

    # takes the same function as plurality
    def set_votes(self, pref_schedule, poss_order):
        temp_num_cands = len(poss_order[0])
        # setting all candidate votes to 0
        for cand in self.cand_objects:
            cand.last_place_votes = 0
        count = 0
        # for each value in the preference schedule
        for val in pref_schedule:
            # the first one is the one getting votes
            name_of_cand_getting_last_votes = poss_order[count][temp_num_cands - 1]
            # using find candidate with name function here
            cand_get_votes = self.find_which_candidate_w_name(name_of_cand_getting_last_votes)
            cand_get_votes.last_place_votes += val
            count += 1


    def run_election(self,pref_schedule, cand_obj, poss_order):

        if(len(cand_obj)==0):
            return
        else:
            self.set_votes(pref_schedule, poss_order)
            cands_to_elim = self.find_candidates_with_highest_last(cand_obj)
            for cand in cands_to_elim:
                cand.round_elim = self.elec_round
                poss_order = self.eliminate_cands(poss_order, cand.name)
                cand_obj.remove(cand)
            self.elec_round += 1
            self.run_election(pref_schedule,cand_obj, poss_order)

    # this is my custom function to determine the ordering of Coombs with majority
    # winner need a majority to win a round and candidates are eliminates until majority winner(s) are reached
    # there can be multiple in case of 50/50 split
    # then we eliminate that candidate since they already won and we go again with the rest
    # if at any time cand_obj is empty it means multiple were deleted at once - return
    def run_election_majority(self,pref_schedule, cand_obj, cand_win, poss_order, poss_order_win):
        # if all objects from cand_win are removed - each allocated majority
        if(len(cand_win)==0):
            return
        else:
            # if everyone is deleted then we need to exit this run
            if(len(cand_obj)==0):
                return

            self.set_votes(pref_schedule, poss_order)  # last place votes
            # includes all cands who have most last place votes
            cands_to_elim = self.find_candidates_with_highest_last(cand_obj)
            self.simple_set(pref_schedule,poss_order)
            cand_w_fifty_or_more = []
            for cand in cand_obj:
                if cand.num_votes >= self.num_voters/2:
                    cand_w_fifty_or_more.append(cand)
            # if there are candidate(s) with at least 50% of the vote they win in that round
            if len(cand_w_fifty_or_more) != 0:
                for cand in cand_w_fifty_or_more:
                    cand.round_win = self.elec_round
                    poss_order_win = self.eliminate_cands(poss_order_win, cand.name)
                    cand_win.remove(cand)
                self.elec_round += 1  # round goes to the next one
                # if there is a majority candidate, reset cand_obj and poss_order and go to next round
                cand_obj = cand_win[:]
                poss_order = poss_order_win[:]
                # recursively calls run_election
                self.run_election_majority(pref_schedule, cand_obj,cand_win,poss_order,poss_order_win)

            else:
                for cand in cands_to_elim:
                    poss_order = self.eliminate_cands(poss_order, cand.name)
                    cand_obj.remove(cand)
                # if every single candidate is to be eliminated then we assign each one this round
                # this is the round they were elected winner - exit the election since not possible to proceed
                if(len(cand_obj)==0):
                    for cand in cands_to_elim:
                        cand.round_win = self.elec_round
                self.run_election_majority(pref_schedule, cand_obj, cand_win, poss_order, poss_order_win)


    def find_candidates_with_highest_last(self, cand_obj):
        cands_with_most_last = []
        cand_with_max = max(cand_obj, key=lambda v: v.last_place_votes)
        most_last_vote = cand_with_max.last_place_votes
        for cand in cand_obj:
            if cand.last_place_votes == most_last_vote:
                cands_with_most_last.append(cand)
        return cands_with_most_last


    def create_societal_rank(self, pref_schedule, cand_obj, poss_order):
        cand_process = cand_obj[:]
        self.elec_round = 1
        self.run_election(pref_schedule, cand_process, poss_order)
        sorted_list = sorted(cand_obj, key=lambda v: v.round_elim, reverse=True)
        map_of_cands = {}
        # emulates do while
        count = 0
        previous = sorted_list[0].round_elim
        map_of_cands[count] = []
        # end of first iteration
        for cand in sorted_list:
            if (cand.round_elim == previous):
                map_of_cands[count].append(cand)
            else:
                count += 1
                map_of_cands[count] = []
                map_of_cands[count].append(cand)
            previous = cand.round_elim
            cand.rank = count

        return map_of_cands

    def create_societal_rank_aliter(self, pref_schedule, cand_obj, poss_order):
        cand_process = cand_obj[:]
        self.run_election_majority(pref_schedule, cand_process, cand_process[:], poss_order, poss_order[:])
        # the two [:] arguments unnecessary if doing other method
        sorted_list = sorted(cand_obj, key=lambda v: v.round_win)
        # sorted_list = sorted(cand_obj, key=lambda v: v.round_elim, reverse = True)
        map_of_cands = {}
        # emulates do while
        count = 0
        previous = sorted_list[0].round_win
        map_of_cands[count] = []
        # end of first iteration
        for cand in sorted_list:
            if (cand.round_win == previous):
                map_of_cands[count].append(cand)
            else:
                count += 1
                map_of_cands[count] = []
                map_of_cands[count].append(cand)
            previous = cand.round_win
            cand.rank = count

        return map_of_cands













    def determine_winner(self, pref_schedule, cand_obj, poss_order):
        cand_obj = cand_obj[:]  # I do not want to modify the actual self.cand_objects
        societal_order = self.create_societal_rank(pref_schedule, cand_obj, poss_order)
        num_top = len(societal_order[0])
        if (num_top == 1):
            return societal_order[0][0]
        elif num_top > 1:
            cand_win = rand.choice(societal_order[0])
            return cand_win
        else:
            return None



    def type(self):
        return "Coombs"




class Baldwin(VotingSystem):

    def __init__(self, num_voters, num_cands, cand_objects):
        super().__init__(num_voters, num_cands, cand_objects)
        self.candidates_remaining = self.cand_objects[:]
        self.current_pref_table = self.possible_orders[:]
        self.elec_round = 1

    #same rule as BordaCount
    def set_votes(self,pref_schedule, poss_order):
        for cand in self.cand_objects:
            cand.points = 0
            cand.num_votes = 0

        count = 0
        for val in pref_schedule:
            ordering = poss_order[count]
            # note Borda points would also change as rounds go on - check in the C++ model also
            for i in range(0, len(poss_order[0])):
                cand = self.find_which_candidate_w_name(ordering[i])  # find the candidate
                cand.points += val * (len(poss_order[0]) - i)
            count += 1


    def run_election(self,pref_schedule, cand_obj, poss_order):

        if(len(cand_obj)==0):
            return
        else:
            self.set_votes(pref_schedule, poss_order)
            cands_to_elim = self.find_candidates_with_lowest(cand_obj)
            for cand in cands_to_elim:
                cand.round_elim = self.elec_round
                poss_order = self.eliminate_cands(poss_order, cand.name)
                cand_obj.remove(cand)
            self.elec_round += 1
            self.run_election(pref_schedule,cand_obj, poss_order)

    def find_candidates_with_lowest(self, cand_obj):
        cands_with_least_points = []
        # this employs the other strategy - sorting and then taking the value of the 0th element
        sorted_cands = sorted(cand_obj, key=lambda v:v.points)
        least_points = sorted_cands[0].points
        for cand in cand_obj:
            if cand.points == least_points:
                cands_with_least_points.append(cand)
        return cands_with_least_points


    def create_societal_rank(self, pref_schedule, cand_obj, poss_order):
        cand_process = cand_obj[:]
        self.elec_round = 1
        self.run_election(pref_schedule, cand_process, poss_order)
        sorted_list = sorted(cand_obj, key=lambda v: v.round_elim, reverse=True)
        map_of_cands = {}
        # emulates do while
        count = 0
        previous = sorted_list[0].round_elim
        map_of_cands[count] = []
        # end of first iteration
        for cand in sorted_list:
            if (cand.round_elim == previous):
                map_of_cands[count].append(cand)
            else:
                count += 1
                map_of_cands[count] = []
                map_of_cands[count].append(cand)
            previous = cand.round_elim
            cand.rank = count

        return map_of_cands










    def determine_winner(self, pref_schedule, cand_obj, poss_order):
        cand_obj = cand_obj[:]  # I do not want to modify the actual self.cand_objects
        societal_order = self.create_societal_rank(pref_schedule, cand_obj, poss_order)
        num_top = len(societal_order[0])
        if (num_top == 1):
            return societal_order[0][0]
        elif num_top > 1:
            cand_win = rand.choice(societal_order[0])
            return cand_win
        else:
            return None



    def type(self):
        return "Baldwin"





# this is also called Copeland

class PairwiseComparison(VotingSystem):

    def __init__(self, num_voters, num_cands, cand_objects):
        super().__init__(num_voters, num_cands, cand_objects)

    def set_votes(self, pref_schedule,poss_order):
        for cand in self.cand_objects:
            cand.num_votes = 0

        for comp in self.comparisons:
            cand_win = self.compare(comp, pref_schedule, poss_order)
            if cand_win is None:
                for name in comp:
                    cand = self.find_which_candidate_w_name(name)
                    cand.num_votes += 0.5
            else:
                cand_win.num_votes += 1

    def create_societal_rank(self,pref_schedule,cand_obj, poss_order):
            self.set_votes(pref_schedule, poss_order)
            sorted_list = sorted(cand_obj, key=lambda v: v.num_votes, reverse=True)
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
                previous = cand.num_votes
                cand.rank = count

            return map_of_cands

    def determine_winner(self, pref_schedule,cand_obj, poss_order):
        societal_order = self.create_societal_rank(pref_schedule, cand_obj, poss_order)
        num_top = len(societal_order[0])
        if (num_top == 1):
            return societal_order[0][0]
        elif num_top > 1:
            cand_win = rand.choice(societal_order[0])
            return cand_win
        else:
            return None


    def type(self):
        return "Pairwise Comparison"


# really need to see whether this is the right implementation
# the transitivity function is good though - this is the only system that violates transitivity
class PairwiseMajority(VotingSystem):

    def __init__(self, num_voters, num_cands, cand_objects):
        super().__init__(num_voters, num_cands, cand_objects)

    # fillers functions for now

    def set_votes(self, pref_schedule, poss_order):
        cond_cand = self.find_Condorcet_candidate(pref_schedule)
        return cond_cand
    # how can I return here - is that consistent with definition

    def create_societal_rank(self,pref_schedule, cand_obj, poss_order):
        # this cannot create a transitive one
        cond_cand = self.set_votes(pref_schedule, poss_order)
        return cond_cand

    def determine_winner(self, pref_schedule, cand_obj, poss_order):
        cond_cand = self.create_societal_rank(pref_schedule, cand_obj, poss_order)
        return cond_cand




    def type(self):
        return "Pairwise Majority"



class Dowdall(VotingSystem):

    def __init__(self, num_voters, num_cands, cand_objects):
        super().__init__(num_voters, num_cands, cand_objects)

    def set_votes(self,pref_schedule, poss_order):
        for cand in self.cand_objects:
            cand.num_votes = 0

        count = 0
        for val in pref_schedule:
            ordering = poss_order[count]
            for i in range(0, self.num_cands):
                cand = self.find_which_candidate_w_name(ordering[i])
                cand.num_votes += (val * 1/(i+1))
            count += 1


    # this function takes in a preference schedule (list of numbers of length factorial(num_cands) and computes the winner
    def determine_winner(self, pref_schedule,cand_obj, poss_order):

        societal_order = self.create_societal_rank(pref_schedule, cand_obj, poss_order)
        num_top = len(societal_order[0])


        if (num_top == 1):
            return societal_order[0][0]

        elif num_top > 1:
            cand_win = rand.choice(societal_order[0])

            return cand_win
        else:
            return None

    def create_societal_rank(self,pref_schedule, cand_obj, poss_order):
        self.set_votes(pref_schedule, poss_order)
        sorted_list = sorted(cand_obj, key=lambda v: v.num_votes, reverse=True)
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
            previous = cand.num_votes
            cand.rank = count

        return map_of_cands


    def type(self):
        return "Dowdall"



class Dictatorship(VotingSystem):

    def __init__(self, num_voters, num_cands, cand_objects):
        super().__init__(num_voters, num_cands, cand_objects)


    def set_votes(self, pref_schedule, poss_order):
        voter_dict = rand.randint(1,self.num_voters)


#difficult system to model given current framework
#on each run I need to know what position the dictator is in on the preference schedule


class ImposedRule(VotingSystem):
    def __init__(self, num_voters, num_cands, cand_objects):
        super().__init__(num_voters, num_cands, cand_objects)
        self.winner = rand.choice(self.cand_objects)  # the winner is decided before the election takes place

    def set_votes(self, pref_schedule, poss_order):
        print("No election")

    def create_societal_rank(self,pref_schedule, cand_obj, poss_order):
        for cand in cand_obj:
            if cand == self.winner:
                cand.rank = 0
            else:
                cand.rank = 1

    def determine_winner(self, pref_schedule, cand_obj, poss_order):
        self.create_societal_rank(pref_schedule, cand_obj, poss_order)
        return self.winner

    def type(self):
        return "Imposed Rule"













class Black(VotingSystem):

    def __init__(self, num_voters, num_cands, cand_objects):
        super().__init__(num_voters, num_cands, cand_objects)

    # set votes used based on Borda points
    def set_votes(self,pref_schedule, poss_order):
        for cand in self.cand_objects:
            cand.points = 0
            cand.num_votes = 0

        count = 0
        for val in pref_schedule:
            ordering = poss_order[count]
            for i in range(0, self.num_cands):
                if (i == 0):
                    cand = self.find_which_candidate_w_name(ordering[0])
                    cand.num_votes += val
                # for consistency
                cand = self.find_which_candidate_w_name(ordering[i])
                cand.points += val * (self.num_cands - i)
            count += 1


    def create_societal_rank(self,pref_schedule, cand_obj, poss_order):
        self.set_votes(pref_schedule, poss_order)
        sorted_list = sorted(cand_obj, key=lambda v: v.points, reverse=True)
        map_of_cands = {}
        cand_condorcet = self.find_Condorcet_candidate(pref_schedule)
        # if there is no Condorcet candidate we simply use Borda
        if cand_condorcet is None:
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
                previous = cand.points
                cand.rank = count


        elif cand_condorcet is not None:
            map_of_cands[0] = []
            map_of_cands[0].append(cand_condorcet)
            cand_condorcet.rank = 0
            sorted_list.remove(cand_condorcet)
            count = 1
            previous = sorted_list[0].points  # sorted list does not include the condorcet candidate
            map_of_cands[count] = []
            # end of first iteration
            for cand in sorted_list:
                if (cand.points == previous):
                    map_of_cands[count].append(cand)
                else:
                    count += 1
                    map_of_cands[count] = []
                    map_of_cands[count].append(cand)
                previous = cand.points
                cand.rank = count

        return map_of_cands



    def determine_winner(self, pref_schedule,cand_obj, poss_order):

        societal_order = self.create_societal_rank(pref_schedule, cand_obj, poss_order)
        num_top = len(societal_order[0])
        if (num_top == 1):
            return societal_order[0][0]
        elif num_top > 1:
            cand_win = rand.choice(societal_order[0])
            return cand_win
        else:
            return None




    def type(self):
        return "Black"










# this one is if there is condorcet, elect, otherwise use Borda - seems promising to reduce CWC_vio - check IIA
# however, it does not exactly produce a ranking - can make arbitrary ranking by your definition
# maybe Condorcet is 1st if exists - then rank rest by Borda after using eliminate cand
# if Condorcet is not there - completely rank by Borda

class TopTwo(VotingSystem):

    def __init__(self, num_voters, num_cands, cand_objects):
        super().__init__(num_voters, num_cands, cand_objects)

    def set_votes(self,pref_schedule, poss_order):
        # setting all candidate votes to 0
        for cand in self.cand_objects:
            cand.num_votes = 0
        count = 0
        # for each value in the preference schedule
        for val in pref_schedule:
            # the first one is the one getting votes
            name_of_cand_getting_votes = poss_order[count][0]
            # using find candidate with name function here
            cand_get_votes = self.find_which_candidate_w_name(name_of_cand_getting_votes)
            cand_get_votes.num_votes += val
            count += 1

    #exactly the same as plurality


    def create_societal_rank(self,pref_schedule, cand_obj, poss_order):
        self.set_votes(pref_schedule, poss_order)
        sorted_list = sorted(cand_obj, key=lambda v: v.num_votes, reverse=True)
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
            previous = cand.num_votes
            cand.rank = count

        # if there is a majority winner the election ends here; no need to conduct second round
        if(self.find_major_cand(pref_schedule) is not None):
            return map_of_cands

        # second round starts here

        # Note that if there is anyone in the Top Two, they are ranked above the rest of the candidates
        # we do not re-evaluate points relative to others
        # top two in separate category (even in case that 2 and 3 tie)
        # possibly few more IIA violations in my method
        # but it is more consistent than paper with how elections run in real world (think Warnock and Walker)

        else:
            r2_map_of_cands = {}
            top_two = []
            index = 0
            num_left = 2
            while (num_left != 0):
                if (len(map_of_cands[index]) <= num_left):
                    for cand in map_of_cands[index]:
                        top_two.append(cand)
                    num_left = num_left - len(map_of_cands[index])
                elif(len(map_of_cands[index]) > num_left):
                    ones_to_add = rand.sample(map_of_cands[index],num_left)  # this could actually be in both places
                    for cand in ones_to_add:
                        top_two.append(cand)
                    num_left = 0
                index += 1
            self.compare([top_two[0].name, top_two[1].name], pref_schedule, self.possible_orders)
            top_two[0].num_votes = top_two[0].condorcet_points
            top_two[1].num_votes = top_two[1].condorcet_points
            if top_two[0].num_votes > top_two[1].num_votes:
                r2_map_of_cands[0] = []
                r2_map_of_cands[0].append(top_two[0])
                top_two[0].rank = 0

                r2_map_of_cands[1] = []
                r2_map_of_cands[1].append(top_two[1])
                top_two[1].rank = 1
            elif top_two[0].num_votes < top_two[1].num_votes:
                r2_map_of_cands[0] = []
                r2_map_of_cands[0].append(top_two[1])
                top_two[1].rank = 0

                r2_map_of_cands[1] = []
                r2_map_of_cands[1].append(top_two[0])
                top_two[0].rank = 1
            else:
                r2_map_of_cands[0] = []
                r2_map_of_cands[0].append(top_two[0])
                r2_map_of_cands[0].append(top_two[1])
                top_two[0].rank = 0
                top_two[1].rank = 0
            max_rank = max(top_two[0].rank, top_two[1].rank)


            new_cand_obj = cand_obj[:]
            new_cand_obj.remove(top_two[0])
            new_cand_obj.remove(top_two[1])
            sorted_list = sorted(new_cand_obj, key=lambda v: v.num_votes, reverse=True)

            count = max_rank
            previous = -1
            for cand in sorted_list:
                if (cand.num_votes == previous):
                    r2_map_of_cands[count].append(cand)
                else:
                    count += 1
                    r2_map_of_cands[count] = []
                    r2_map_of_cands[count].append(cand)
                previous = cand.num_votes
                cand.rank = count

            return r2_map_of_cands


    def determine_winner(self, pref_schedule,cand_obj, poss_order):

        societal_order = self.create_societal_rank(pref_schedule, cand_obj, poss_order)
        num_top = len(societal_order[0])
        if (num_top == 1):
            return societal_order[0][0]
        elif num_top > 1:
            cand_win = rand.choice(societal_order[0])
            return cand_win
        else:
            return None





    def type(self):
        return "Top Two"



class Minimax(VotingSystem):

    def __init__(self, num_voters, num_cands, cand_objects):
        super().__init__(num_voters, num_cands, cand_objects)

    def set_votes(self, pref_schedule, poss_order):
        for cand in self.cand_objects:
            rival_cands = self.cand_objects[:]
            rival_cands.remove(cand)
            pairwise_defeats = []
            for rival in rival_cands:
                self.compare([cand.name,rival.name],pref_schedule,poss_order) # resets condorcet each time
                loss = rival.condorcet_points - cand.condorcet_points
                if(loss > 0):
                    pairwise_defeats.append(loss)
                else:
                    pairwise_defeats.append(0)
            cand.greatest_pairwise_defeat = max(pairwise_defeats)

    def create_societal_rank(self,pref_schedule, cand_obj, poss_order):
        self.set_votes(pref_schedule, poss_order)
        sorted_list = sorted(cand_obj,key=lambda v: v.greatest_pairwise_defeat)
        map_of_cands = {}
        #emulates do while
        count = 0
        previous = sorted_list[0].greatest_pairwise_defeat
        map_of_cands[count] = []
        #end of first iteration
        for cand in sorted_list:
            if(cand.greatest_pairwise_defeat == previous):
                map_of_cands[count].append(cand)
            else:
                count += 1
                map_of_cands[count] = []
                map_of_cands[count].append(cand)
            previous = cand.greatest_pairwise_defeat
            cand.rank = count



        return map_of_cands

    def determine_winner(self, pref_schedule, cand_obj, poss_order):

        societal_order = self.create_societal_rank(pref_schedule,cand_obj, poss_order)
        num_top = len(societal_order[0])
        if(num_top==1):
            return societal_order[0][0]
        elif num_top > 1:
            cand_win = rand.choice(societal_order[0])
            return cand_win
        else:
            return None


    def type(self):
        return "Minimax"


















# randomly select dictator?



# randomly select winning candidate? - but it has to be fixed throughout

# these last two should never violate IIA


# end of derived classes
            



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
    arr = np.zeros(poss_ranks, dtype=int)  # this has num_cands! elements
    end_range = num_voters + poss_ranks - 1
    vals = rand.sample(range(0,end_range),poss_ranks-1)  # 5 random vals from 0 to 15 for example
    sorted_vals = sorted(vals)  # sort the values
    arr[0] = sorted_vals[0]  # the first bar
    for i in range(1,len(sorted_vals)):
        arr[i] = sorted_vals[i] - sorted_vals[i-1] - 1
    arr[poss_ranks-1] = end_range - sorted_vals[poss_ranks-2] - 1

    return arr

def generate_IANC(num_voters, num_cands):
    pass



def custom_distribution(num_voters, num_cands, weights):
    poss_ranks = math.factorial(num_cands)
    arr = np.zeros(poss_ranks, dtype=int)
    result = 0
    new_arr = []
    for val in weights:
        result += val
        new_arr.append(result)

    for i in range(0,num_voters):
        chosen_val = rand.random()
        for j in range(0,len(new_arr)):
            if chosen_val <= new_arr[j]:
                arr[j] += 1
                break

    return arr


# few functions included for testing

#k is number of candidates factorial
def generate_unique_permutation(n,k):
    voters = np.zeros(n)
    candidates = np.ones(k-1) #not a good variable name, this is actually number of bars (one less than possible pref orders)
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
    list_of_cand_objects = []
    # similar to C++, these could be created in the constructor

    c1 = Candidate('A')
    c2 = Candidate('B')
    c3 = Candidate('C')
    c4 = Candidate('D')

    #list_of_cand_objects.append(Candidate('A'))
    list_of_cand_objects.append(c1)
    list_of_cand_objects.append(c2)
    list_of_cand_objects.append(c3)

    #list_of_cand_objects.append(c4)

    c = Plurality(1000, 3, list_of_cand_objects)
    c.find_condorcet_vios(10000,"IC")
    print(c.cwc_vio/100)











if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time()
    print(str(end - start) + "(s)")


#next steps are to add CLC then unanimty then transitivity before tomorrow

