import heapq

goal = (1,2,3,4,5,6,7,8,0)

# Heuristic (Manhattan Distance)
def h(state):
    d = 0
    for i in range(9):
        if state[i] != 0:
            x1, y1 = divmod(i, 3)
            x2, y2 = divmod(state[i]-1, 3)
            d += abs(x1-x2) + abs(y1-y2)
    return d

# Generate next states
def neighbors(state):
    pos = state.index(0)
    x, y = divmod(pos, 3)
    moves = []

    if x > 0: moves.append(pos-3)
    if x < 2: moves.append(pos+3)
    if y > 0: moves.append(pos-1)
    if y < 2: moves.append(pos+1)

    result = []
    for p in moves:
        s = list(state)
        s[pos], s[p] = s[p], s[pos]
        result.append(tuple(s))
    return result

# A* Search
def solve(start):
    pq = [(h(start), 0, start, [start])]
    visited = set()

    while pq:
        f, g, state, path = heapq.heappop(pq)

        if state == goal:
            return path

        if state in visited:
            continue
        visited.add(state)

        for nxt in neighbors(state):
            if nxt not in visited:
                heapq.heappush(pq, (g+1+h(nxt), g+1, nxt, path+[nxt]))

    return None

# Print Board
def show(state):
    for i in range(0, 9, 3):
        print(state[i:i+3])
    print()

# Main
start = (1,2,3,
         4,0,6,
         7,5,8)

path = solve(start)

if path:
    print("Solution Found!\n")
    for i, state in enumerate(path):
        print("Step", i)
        show(state)
    print("Total Moves:", len(path)-1)
else:
    print("No Solution")