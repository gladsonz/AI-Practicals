
from math import gcd

def water_jug_two_solutions(capacity1, capacity2, target):

    if target > max(capacity1, capacity2):
        return []
    if target % gcd(capacity1, capacity2) != 0:
        return []

    solutions = []

    def dfs(jug1, jug2, path, visited):
        if (jug1, jug2) in visited:
            return False

        visited.add((jug1, jug2))
        path.append((jug1, jug2))

        if jug1 == target or jug2 == target:
            solutions.append(path.copy())
            path.pop()
            visited.remove((jug1, jug2))
            return True  

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
            if dfs(state[0], state[1], path, visited):
                path.pop()
                visited.remove((jug1, jug2))
                return True

        path.pop()
        visited.remove((jug1, jug2))
        return False

    dfs(0, capacity2, [(0, 0)], {(0, 0)})
    dfs(capacity1, 0, [(0, 0)], {(0, 0)})

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
