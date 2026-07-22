graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': [],
    'D': [],
    'E': ['G'],
    'G': []
}

heuristic = {
    'A': 6,
    'B': 3,
    'C': 5,
    'D': 4,
    'E': 1,
    'G': 0
}

def gradient_descent_hill_climbing(start, goal):

    current = start
    step = 1

    print("Step", step, ": Start at", current, "h =", heuristic[current])

    while True:

        if current == goal:
            print("Goal reached:", current)
            return

        neighbors = graph[current]

        print("\nStep", step)
        print("Current:", current)
        print("Neighbors:", neighbors)

        if not neighbors:
            print("No neighbors left. Stop at", current)
            return

        best = None
        max_drop = 0

        for node in neighbors:
            drop = heuristic[current] - heuristic[node]
            print("Check", node, "h =", heuristic[node], "drop =", drop)

            if drop > max_drop:
                max_drop = drop
                best = node

        if best is None:
            print("No improvement possible. Stop at", current)
            return

        print("Move:", current, "->", best, "(max drop =", max_drop, ")")

        current = best
        step += 1


gradient_descent_hill_climbing('A', 'G')