import numpy as np
from collections import defaultdict


def compute_pairwise_preferences(ballots, candidates):
    """
    Compute the pairwise preference matrix.
    """
    num_candidates = len(candidates)
    pairwise = np.zeros((num_candidates, num_candidates), dtype=int)
    candidate_indices = {candidate: i for i, candidate in enumerate(candidates)}

    for ballot in ballots:
        for i, higher in enumerate(ballot):
            for lower in ballot[i + 1:]:
                pairwise[candidate_indices[higher], candidate_indices[lower]] += 1
    return pairwise


def get_sorted_pairs(pairwise):
    """
    Create and sort pairs by strength of victory.
    """
    pairs = []
    num_candidates = pairwise.shape[0]
    for i in range(num_candidates):
        for j in range(i+1,num_candidates):
            margin = pairwise[i, j] - pairwise[j, i]
            if margin >= 0:
                pairs.append((i, j, margin))
            else:
                pairs.append((j,i,-margin))
    # Sort by margin descending, then by number of votes for in case of tie
    pairs.sort(key=lambda x: (-x[2], -pairwise[x[0], x[1]]))
    return pairs


def creates_cycle(locked, winner, loser, path=None):
    """
    Check if adding an edge from winner to loser creates a cycle.
    """
    if path is None:
        path = set()
    if winner == loser:
        return True
    path.add(winner)
    for next_candidate in locked[winner]:
        if next_candidate in path or creates_cycle(locked, next_candidate, loser, path.copy()):
            return True
    return False


def ranked_pairs(ballots, candidates):

    pairwise = compute_pairwise_preferences(ballots, candidates)
    pairs = get_sorted_pairs(pairwise) # ok you get all the pairs

    locked = defaultdict(set)

    for winner, loser, margin in pairs:
        if not creates_cycle(locked, winner, loser):
            if margin > 0:
                locked[winner].add(loser)

    print(locked)

    # I have all the preferences properly?

    # Find the candidate with no incoming edges
    all_candidates = set(range(len(candidates)))
    losers = set()
    for winners in locked.values():
        losers.update(winners)
    winners = all_candidates - losers

    # If there is a single source, return that candidate as winner
    if len(winners) == 1:
        return candidates[winners.pop()]
    else:
        return [candidates[i] for i in winners]  # multiple possible winners in rare ties


# Example usage
if __name__ == "__main__":
    candidates = ["A", "B", "C"]
    ballots = [
        ["A", "B", "C"],
        ["B", "C", "A"],
        ["C", "A", "B"]
    ]
    winner = ranked_pairs(ballots, candidates)
    print("Winner:", winner)