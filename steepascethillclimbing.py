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

def hill_climbing(start, goal):

    current = start
    step = 1

    print("Step",step,": Start at",current,"h =",heuristic[current])

    while True:

        if current == goal:
            print("Goal reached:",current)
            return

        neighbors = graph[current]

        print("\nStep",step)
        print("Current:",current)
        print("Neighbors:",neighbors)

        if not neighbors:
            print("No neighbors left. Stop at",current)
            return

        best = current

        for node in neighbors:
            print("Check",node,"h =",heuristic[node])

            if heuristic[node] < heuristic[best]:
                best = node

        if best == current:
            print("No better state found. Stop at",current)
            return

        print("Move:",current,"->",best)

        current = best
        step += 1


hill_climbing('A','G')