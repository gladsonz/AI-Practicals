from math import gcd

def water_jug_dfs(c1, c2, target):
    stack = [((0, 0), [])]
    visited = set()

    while stack:
        (a, b), path = stack.pop()

        if (a, b) in visited:
            continue
        visited.add((a, b))

        path = path + [(a, b)]

        if a == target or b == target:
            return path

        moves = [
            (c1, b),                     # Fill Jug1
            (a, c2),                     # Fill Jug2
            (0, b),                      # Empty Jug1
            (a, 0),                      # Empty Jug2
            (max(0, a-(c2-b)), min(c2, a+b)),  # Jug1 -> Jug2
            (min(c1, a+b), max(0, b-(c1-a)))   # Jug2 -> Jug1
        ]

        for move in moves:
            stack.append((move, path))

    return None


c1 = int(input("Jug1 Capacity: "))
c2 = int(input("Jug2 Capacity: "))
target = int(input("Target: "))

if target > max(c1, c2) or target % gcd(c1, c2) != 0:
    print("No Solution")
else:
    ans = water_jug_dfs(c1, c2, target)
    if ans:
        print("Steps:")
        for i, state in enumerate(ans):
            print(i, state)