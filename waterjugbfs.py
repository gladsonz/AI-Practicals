from math import gcd
from collections import deque

def water_jug_two_solutions(capacity1, capacity2, target):

    if target > max(capacity1, capacity2):
        return []
    if target % gcd(capacity1, capacity2) != 0:
        return []

    def bfs(start_state):
        queue = deque()
        visited = set()

        queue.append((start_state, [start_state]))
        visited.add(start_state)

        while queue:
            (jug1, jug2), path = queue.popleft()

            if jug1 == target or jug2 == target:
                return path

            next_states = []

            next_states.append((capacity1, jug2))
            next_states.append((jug1, capacity2))

            next_states.append((0, jug2))
            next_states.append((jug1, 0))

            pour = min(jug1, capacity2 - jug2)
            next_states.append((jug1 - pour, jug2 + pour))

            pour = min(jug2, capacity1 - jug1)
            next_states.append((jug1 + pour, jug2 - pour))

            for state in next_states:
                if state not in visited:
                    visited.add(state)
                    queue.append((state, path + [state]))

        return None

    solutions = []

    sol1 = bfs((0, capacity2))
    if sol1:
        solutions.append([(0, 0)] + sol1)

    sol2 = bfs((capacity1, 0))
    if sol2:
        solutions.append([(0, 0)] + sol2)

    return solutions


capacity1 = int(input("Enter capacity of Jug 1: "))
capacity2 = int(input("Enter capacity of Jug 2: "))
target = int(input("Enter target amount: "))

solutions = water_jug_two_solutions(capacity1, capacity2, target)

if solutions:
    for i, sol in enumerate(solutions, 1):
        print(f"\nSolution {i}:")
        for step in sol:
            print(step)
else:
    print("No solution possible.")
