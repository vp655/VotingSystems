from votingsystemclass import VotingSystem
import random as rand
from collections import deque
from itertools import combinations

class Plurality(VotingSystem):

    def __init__(self, num_voters, num_cands, cand_objects):
        super().__init__(num_voters, num_cands, cand_objects)

    # this function takes in a preference schedule (list of numbers of length factorial(num_cands) and computes the winner

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

    def determine_winner(self, pref_schedule, cand_obj, poss_order):

        societal_order = self.create_societal_rank(pref_schedule, cand_obj, poss_order)
        num_top = len(societal_order[0])
        if (num_top == 1):
            return societal_order[0][0]
        elif num_top > 1:
            cand_win = rand.choice(societal_order[0])
            return cand_win
        else:
            return None

    def create_societal_rank(self, pref_schedule, cand_obj, poss_order):
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
        return "Plurality"



class AntiPlurality(VotingSystem):

    def __init__(self, num_voters, num_cands, cand_objects):
        super().__init__(num_voters, num_cands, cand_objects)

    def set_votes(self, pref_schedule, poss_order):
        for cand in self.cand_objects:
            cand.points = 0

        for i in range(len(pref_schedule)):
            ordering = poss_order[i]
            for j in range(0, self.num_cands):
                if j < self.num_cands - 1:
                    cand = self.find_which_candidate_w_name(ordering[j])
                    cand.points += pref_schedule[i]

    def determine_winner(self, pref_schedule, cand_obj, poss_order):
        societal_order = self.create_societal_rank(pref_schedule, cand_obj, poss_order)
        num_top = len(societal_order[0])
        if num_top == 1:
            return societal_order[0][0]
        elif num_top > 1:
            cand_win = rand.choice(societal_order[0])
            return cand_win
        else:
            return None

    def create_societal_rank(self, pref_schedule, cand_obj, poss_order):
        self.set_votes(pref_schedule, poss_order)
        sorted_list = sorted(cand_obj, key=lambda v: v.points, reverse=True)
        map_of_cands = {}
        count = 0
        previous = sorted_list[0].points
        map_of_cands[count] = []
        for cand in sorted_list:
            if cand.points == previous:
                map_of_cands[count].append(cand)
            else:
                count += 1
                map_of_cands[count] = []
                map_of_cands[count].append(cand)
            previous = cand.points
            cand.rank = count

        return map_of_cands

    def type(self):
        return "Anti-Plurality"




class BordaCount(VotingSystem):

    def __init__(self, num_voters, num_cands, cand_objects):
        super().__init__(num_voters, num_cands, cand_objects)

    def set_votes(self, pref_schedule, poss_order):
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
    def determine_winner(self, pref_schedule, cand_obj, poss_order):

        societal_order = self.create_societal_rank(pref_schedule, cand_obj, poss_order)
        num_top = len(societal_order[0])
        if (num_top == 1):
            return societal_order[0][0]
        elif num_top > 1:
            cand_win = rand.choice(societal_order[0])
            return cand_win
        else:
            return None

    def create_societal_rank(self, pref_schedule, cand_obj, poss_order):
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

    def set_votes(self, pref_schedule, poss_order):
        for cand in self.cand_objects:
            cand.points = 0
            cand.num_votes = 0

        count = 0
        for val in pref_schedule:
            ordering = poss_order[count]
            for i in range(0, self.num_rank):
                if (i == 0):
                    cand = self.find_which_candidate_w_name(ordering[0])
                    cand.num_votes += val
                # for consistency
                cand = self.find_which_candidate_w_name(ordering[i])
                cand.points += val * (self.num_rank - i)
            count += 1

    # this function takes in a preference schedule (list of numbers of length factorial(num_cands) and computes the winner
    def determine_winner(self, pref_schedule, cand_obj, poss_order):

        societal_order = self.create_societal_rank(pref_schedule, cand_obj, poss_order)
        num_top = len(societal_order[0])
        if (num_top == 1):
            return societal_order[0][0]
        elif num_top > 1:
            cand_win = rand.choice(societal_order[0])
            return cand_win
        else:
            return None

    def create_societal_rank(self, pref_schedule, cand_obj, poss_order):
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

    def run_election(self, pref_schedule, cand_obj, poss_order):

        if (len(cand_obj) == 0):
            return
        else:
            self.set_votes(pref_schedule, poss_order)
            cands_to_elim = self.find_candidates_with_lowest(cand_obj)
            for cand in cands_to_elim:
                cand.round_elim = self.elec_round
                poss_order = self.eliminate_cands(poss_order, cand.name)
                cand_obj.remove(cand)
            self.elec_round += 1
            self.run_election(pref_schedule, cand_obj, poss_order)

    def find_candidates_with_lowest(self, cand_obj):
        cands_with_least_votes = []
        # this gets the candidates with the minimum votes and then take the votes of that candidate
        # a better way to do that may be to sort them and take the 0th ones votes
        # that may also save time
        cand_with_min = min(cand_obj, key=lambda v: v.num_votes)
        least_vote = cand_with_min.num_votes
        for cand in cand_obj:
            if cand.num_votes == least_vote:
                cands_with_least_votes.append(cand)
        return cands_with_least_votes

    def create_societal_rank(self, pref_schedule, cand_obj, poss_order):
        cand_process = cand_obj[:]
        self.elec_round = 1  # adding this so it does not add up to 20000 rounds
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

    def run_election(self, pref_schedule, cand_obj, poss_order):

        if (len(cand_obj) == 0):
            return
        else:
            self.set_votes(pref_schedule, poss_order)
            cands_to_elim = self.find_candidates_with_highest_last(cand_obj)
            for cand in cands_to_elim:
                cand.round_elim = self.elec_round
                poss_order = self.eliminate_cands(poss_order, cand.name)
                cand_obj.remove(cand)
            self.elec_round += 1
            self.run_election(pref_schedule, cand_obj, poss_order)

    # this is my custom function to determine the ordering of Coombs with majority
    # winner need a majority to win a round and candidates are eliminates until majority winner(s) are reached
    # there can be multiple in case of 50/50 split
    # then we eliminate that candidate since they already won and we go again with the rest
    # if at any time cand_obj is empty it means multiple were deleted at once - return
    def run_election_majority(self, pref_schedule, cand_obj, cand_win, poss_order, poss_order_win):
        # if all objects from cand_win are removed - each allocated majority
        if (len(cand_win) == 0):
            return
        else:
            # if everyone is deleted then we need to exit this run
            if (len(cand_obj) == 0):
                return

            self.set_votes(pref_schedule, poss_order)  # last place votes
            # includes all cands who have most last place votes
            cands_to_elim = self.find_candidates_with_highest_last(cand_obj)
            self.simple_set(pref_schedule, poss_order)
            cand_w_fifty_or_more = []
            for cand in cand_obj:
                if cand.num_votes >= self.num_voters / 2:
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
                self.run_election_majority(pref_schedule, cand_obj, cand_win, poss_order, poss_order_win)

            else:
                for cand in cands_to_elim:
                    poss_order = self.eliminate_cands(poss_order, cand.name)
                    cand_obj.remove(cand)
                # if every single candidate is to be eliminated then we assign each one this round
                # this is the round they were elected winner - exit the election since not possible to proceed
                if (len(cand_obj) == 0):
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

    # same rule as BordaCount
    def set_votes(self, pref_schedule, poss_order):
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

    def run_election(self, pref_schedule, cand_obj, poss_order):

        if (len(cand_obj) == 0):
            return
        else:
            self.set_votes(pref_schedule, poss_order)
            cands_to_elim = self.find_candidates_with_lowest(cand_obj)
            for cand in cands_to_elim:
                cand.round_elim = self.elec_round
                poss_order = self.eliminate_cands(poss_order, cand.name)
                cand_obj.remove(cand)
            self.elec_round += 1
            self.run_election(pref_schedule, cand_obj, poss_order)

    def find_candidates_with_lowest(self, cand_obj):
        cands_with_least_points = []
        # this employs the other strategy - sorting and then taking the value of the 0th element
        sorted_cands = sorted(cand_obj, key=lambda v: v.points)
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


class Nanson(VotingSystem):
    def __init__(self, num_voters, num_cands, cand_objects):
        super().__init__(num_voters, num_cands, cand_objects)
        self.candidates_remaining = self.cand_objects[:]
        self.current_pref_table = self.possible_orders[:]
        self.elec_round = 1

    # still borda points
    def set_votes(self, pref_schedule, poss_order):
        for cand in self.cand_objects:
            cand.points = 0

        count = 0
        for val in pref_schedule:
            ordering = poss_order[count]
            for i in range(0, len(poss_order[0])):
                cand = self.find_which_candidate_w_name(ordering[i])
                cand.points += val * (len(poss_order[0]) - i)
            count += 1

    def run_election(self, pref_schedule, cand_obj, poss_order):

        if len(cand_obj) == 0:
            return
        else:
            self.set_votes(pref_schedule, poss_order)
            cands_to_elim = self.find_candidates_below_mean(cand_obj)
            for cand in cands_to_elim:
                cand.round_elim = self.elec_round
                poss_order = self.eliminate_cands(poss_order, cand.name)
                cand_obj.remove(cand)
            self.elec_round += 1
            self.run_election(pref_schedule, cand_obj, poss_order)

    def find_candidates_below_mean(self, cand_obj): # run of simulation currently
        total_pts = 0
        for cand in cand_obj:
            total_pts += cand.points

        mean_pts = total_pts / len(cand_obj)
        cands_to_eliminate = []
        for cand in cand_obj:
            if cand.points <= mean_pts:
                cands_to_eliminate.append(cand)
        return cands_to_eliminate

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

        # I think that doesnt work --> its still a shallow copy
        # but I can modify the list correctly
        # but still pointers to same place

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
        return "Nanson"



# this is also called Copeland

class PairwiseComparison(VotingSystem):

    def __init__(self, num_voters, num_cands, cand_objects):
        super().__init__(num_voters, num_cands, cand_objects)

    def set_votes(self, pref_schedule, poss_order):
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

    def create_societal_rank(self, pref_schedule, cand_obj, poss_order):
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

    def determine_winner(self, pref_schedule, cand_obj, poss_order):
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

    def create_societal_rank(self, pref_schedule, cand_obj, poss_order):
        # this cannot create a transitive one
        cond_cand = self.set_votes(pref_schedule, poss_order)
        return cond_cand

    def determine_winner(self, pref_schedule, cand_obj, poss_order):
        cond_cand = self.create_societal_rank(pref_schedule, cand_obj, poss_order)
        return cond_cand

    def type(self):
        return "Pairwise Majority"




class RankedPairs(VotingSystem):
    def __init__(self, num_voters, num_cands, cand_objects):
        super().__init__(num_voters, num_cands, cand_objects)
        self.pairwise_matrix = []
        self.name_to_index = {}
        self.index_to_cand = {}
    def set_votes(self, pref_schedule, poss_order):
        self.pairwise_matrix = [[0] * self.num_cands for _ in range(self.num_cands)]
        self.name_to_index = {cand.name: i for i, cand in enumerate(self.cand_objects)}
        self.index_to_cand = {i: cand for i, cand in enumerate(self.cand_objects)}

        for i in range(len(pref_schedule)):
            order = poss_order[i]
            for j in range(len(order)):
                for k in range(j + 1, len(order)):
                    winner = self.name_to_index[order[j]]
                    loser = self.name_to_index[order[k]]
                    self.pairwise_matrix[winner][loser] += pref_schedule[i]

    def determine_winner(self, pref_schedule, cand_obj, poss_order):
        societal_order = self.create_societal_rank(pref_schedule, cand_obj, poss_order)
        num_top = len(societal_order[0])
        if num_top == 1:
            return societal_order[0][0]
        elif num_top > 1:
            return rand.choice(societal_order[0])
        else:
            return None

    def create_societal_rank(self, pref_schedule, cand_obj, poss_order):
        self.set_votes(pref_schedule, poss_order)

        pairs = []
        for i, j in combinations(range(self.num_cands), 2):
            if self.pairwise_matrix[i][j] > self.pairwise_matrix[j][i]:
                margin = self.pairwise_matrix[i][j] - self.pairwise_matrix[j][i]
                pairs.append((i, j, margin))
            elif self.pairwise_matrix[j][i] > self.pairwise_matrix[i][j]:
                margin = self.pairwise_matrix[j][i] - self.pairwise_matrix[i][j]
                pairs.append((j, i, margin))

        pairs.sort(key=lambda x: x[2], reverse=True)
        locked = [[False] * self.num_cands for _ in range(self.num_cands)]

        def creates_cycle(start, end):
            visited = set()
            stack = [end]
            while stack:
                node = stack.pop()
                if node == start:
                    return True
                for nxt in range(self.num_cands):
                    if locked[node][nxt] and nxt not in visited:
                        visited.add(nxt)
                        stack.append(nxt)
            return False

        for winner, loser, _ in pairs:
            if not creates_cycle(winner, loser):
                locked[winner][loser] = True

        in_degree = [0] * self.num_cands
        for i in range(self.num_cands):
            for j in range(self.num_cands):
                if locked[i][j]:
                    in_degree[j] += 1

        queue = deque([i for i in range(self.num_cands) if in_degree[i] == 0])
        rank_list = []
        while queue:
            u = queue.popleft()
            rank_list.append(self.index_to_cand[u])
            for v in range(self.num_cands):
                if locked[u][v]:
                    in_degree[v] -= 1
                    if in_degree[v] == 0:
                        queue.append(v)

        for i, cand in enumerate(rank_list):
            cand.rank = i
        grouped = {}
        for cand in rank_list:
            r = cand.rank
            if r not in grouped:
                grouped[r] = []
            grouped[r].append(cand)
        return grouped

    def type(self):
        return "Ranked Pairs"


class Dowdall(VotingSystem):

    def __init__(self, num_voters, num_cands, cand_objects):
        super().__init__(num_voters, num_cands, cand_objects)

    def set_votes(self, pref_schedule, poss_order):
        for cand in self.cand_objects:
            cand.num_votes = 0

        count = 0
        for val in pref_schedule:
            ordering = poss_order[count]
            for i in range(0, self.num_cands):
                cand = self.find_which_candidate_w_name(ordering[i])
                cand.num_votes += (val * 1 / (i + 1))
            count += 1

    # this function takes in a preference schedule (list of numbers of length factorial(num_cands) and computes the winner
    def determine_winner(self, pref_schedule, cand_obj, poss_order):

        societal_order = self.create_societal_rank(pref_schedule, cand_obj, poss_order)
        num_top = len(societal_order[0])

        if (num_top == 1):
            return societal_order[0][0]

        elif num_top > 1:
            cand_win = rand.choice(societal_order[0])

            return cand_win
        else:
            return None

    def create_societal_rank(self, pref_schedule, cand_obj, poss_order):
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
        voter_dict = rand.randint(1, self.num_voters)


# difficult system to model given current framework
# on each run I need to know what position the dictator is in on the preference schedule


class ImposedRule(VotingSystem):
    def __init__(self, num_voters, num_cands, cand_objects):
        super().__init__(num_voters, num_cands, cand_objects)
        self.winner = rand.choice(self.cand_objects)  # the winner is decided before the election takes place

    def set_votes(self, pref_schedule, poss_order):
        print("No election")

    def create_societal_rank(self, pref_schedule, cand_obj, poss_order):
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
    def set_votes(self, pref_schedule, poss_order):
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

    def create_societal_rank(self, pref_schedule, cand_obj, poss_order):
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

    def determine_winner(self, pref_schedule, cand_obj, poss_order):

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

    # exactly the same as plurality

    def create_societal_rank(self, pref_schedule, cand_obj, poss_order):
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
        if (self.find_major_cand(pref_schedule) is not None):
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
                elif (len(map_of_cands[index]) > num_left):
                    ones_to_add = rand.sample(map_of_cands[index], num_left)  # this could actually be in both places
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

    def determine_winner(self, pref_schedule, cand_obj, poss_order):

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
                self.compare([cand.name, rival.name], pref_schedule, poss_order)  # resets condorcet each time
                loss = rival.condorcet_points - cand.condorcet_points
                if (loss > 0):
                    pairwise_defeats.append(loss)
                else:
                    pairwise_defeats.append(0)
            cand.greatest_pairwise_defeat = max(pairwise_defeats)

    def create_societal_rank(self, pref_schedule, cand_obj, poss_order):
        self.set_votes(pref_schedule, poss_order)
        sorted_list = sorted(cand_obj, key=lambda v: v.greatest_pairwise_defeat)
        map_of_cands = {}
        # emulates do while
        count = 0
        previous = sorted_list[0].greatest_pairwise_defeat
        map_of_cands[count] = []
        # end of first iteration
        for cand in sorted_list:
            if (cand.greatest_pairwise_defeat == previous):
                map_of_cands[count].append(cand)
            else:
                count += 1
                map_of_cands[count] = []
                map_of_cands[count].append(cand)
            previous = cand.greatest_pairwise_defeat
            cand.rank = count

        return map_of_cands

    def determine_winner(self, pref_schedule, cand_obj, poss_order):

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
        return "Minimax"

# randomly select dictator?


# randomly select winning candidate? - but it has to be fixed throughout

# these last two should never violate IIA


# end of derived classes



