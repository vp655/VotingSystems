class Candidate:
    def __init__(self, name, num_votes=0):

        self.name = name
        self.num_votes = num_votes
        self.condorcet_points = 0
        self.condorcet_wins = 0
        self.points = 0
        self.rank = 0
        self.round_elim = 0  # for instant runoff
        self.round_win = 0  # for Coombs

        self.condorcet_losses = 0
        self.last_place_votes = 0

        self.greatest_pairwise_defeat = 0  # for minimax

    # overloading operators to compare candidates
    def __eq__(self,other):
        return self.name == other.name

    def __ge__(self,other):
        return self.rank >= other.rank
