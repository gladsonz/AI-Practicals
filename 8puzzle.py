import heapq

GOAL_STATE = (1, 2, 3, 4, 5, 6, 7, 8, 0)

MOVES = {
    "UP": -3,
    "DOWN": 3,
    "LEFT": -1,
    "RIGHT": 1
}

def manhattan_distance(state):
    distance = 0
    for i in range(9):
        if state[i] == 0:
            continue
        goal_pos = state[i] - 1
        x1, y1 = divmod(i, 3)
        x2, y2 = divmod(goal_pos, 3)
        distance += abs(x1 - x2) + abs(y1 - y2)
    return distance

def get_neighbors(state):
    neighbors = []
    zero_index = state.index(0)
    x, y = divmod(zero_index, 3)

    for move, delta in MOVES.items():
        new_index = zero_index + delta

        if move == "LEFT" and y == 0:
            continue
        if move == "RIGHT" and y == 2:
            continue
        if move == "UP" and x == 0:
            continue
        if move == "DOWN" and x == 2:
            continue

        new_state = list(state)
        new_state[zero_index], new_state[new_index] = new_state[new_index], new_state[zero_index]
        neighbors.append((tuple(new_state), move))

    return neighbors

def print_board(state):
    for i in range(0, 9, 3):
        print(state[i:i+3])
    print()

def solve_puzzle(start_state):
    visited = set()
    heap = []

   
    heapq.heappush(heap, (manhattan_distance(start_state), 0, start_state, [], [start_state]))

    while heap:
        f, g, current, path, states_path = heapq.heappop(heap)

        if current in visited:
            continue
        visited.add(current)

        if current == GOAL_STATE:
            return path, states_path

        for neighbor, move in get_neighbors(current):
            if neighbor not in visited:
                new_path = path + [move]
                new_states_path = states_path + [neighbor]
                new_g = g + 1
                new_h = manhattan_distance(neighbor)
                new_f = new_g + new_h

                heapq.heappush(heap, (new_f, new_g, neighbor, new_path, new_states_path))

    return None, None


start = (1, 2, 3,
         4, 0, 6,
         7, 5, 8)

path, states = solve_puzzle(start)

if path:
    print("=== Solution Found ===\n")
    
    for i, state in enumerate(states):
        print(f"Step {i}:")
        print_board(state)

        h = manhattan_distance(state)
        g = i
        f = g + h

        print(f"Move: {path[i-1] if i > 0 else 'START'}")
        print(f"g(n) = {g}, h(n) = {h}, f(n) = {f}")
        print("-" * 30)

    print("Total moves:", len(path))
else:
    print("No solution exists.")