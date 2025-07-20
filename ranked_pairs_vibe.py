from collections import deque
from itertools import combinations

def tideman_ranking(ballots):
    # Step 1: Extract candidates and build pairwise preference matrix
    candidates = sorted({c for b in ballots for c in b})
    n = len(candidates)
    idx = {c: i for i, c in enumerate(candidates)}
    prefs = [[0]*n for _ in range(n)]
    for b in ballots:
        for i, ci in enumerate(b):
            for cj in b[i+1:]:
                prefs[idx[ci]][idx[cj]] += 1

    # Step 2: Create sorted list of winning pairs
    pairs = []
    for i, j in combinations(range(n), 2):
        if prefs[i][j] > prefs[j][i]:
            pairs.append((i, j, prefs[i][j] - prefs[j][i]))
        elif prefs[j][i] > prefs[i][j]:
            pairs.append((j, i, prefs[j][i] - prefs[i][j]))
    pairs.sort(key=lambda x: x[2], reverse=True)

    # Step 3: Lock in pairs without forming cycles
    locked = [[False]*n for _ in range(n)]

    def creates_cycle(start, end):
        visited = set()
        stack = [end]
        while stack:
            current = stack.pop()
            if current == start:
                return True
            for neighbor in range(n):
                if locked[current][neighbor] and neighbor not in visited:
                    visited.add(neighbor)
                    stack.append(neighbor)
        return False

    for winner, loser, _ in pairs:
        if not creates_cycle(winner, loser):
            locked[winner][loser] = True

    # Step 4: Topological sort
    in_degree = [0]*n
    for i in range(n):
        for j in range(n):
            if locked[i][j]:
                in_degree[j] += 1

    queue = deque([i for i in range(n) if in_degree[i] == 0])
    result = []

    while queue:
        u = queue.popleft()
        result.append(candidates[u])
        for v in range(n):
            if locked[u][v]:
                in_degree[v] -= 1
                if in_degree[v] == 0:
                    queue.append(v)

    return result

# Example usage
if __name__ == "__main__":
    ballots = [
        ['A', 'B'],
        ['B', 'A'],
    ]
    print("Full ranking:", tideman_ranking(ballots))
