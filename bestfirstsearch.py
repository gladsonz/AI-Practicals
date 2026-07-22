# graph = {
#     'A': {'B': 1, 'C': 4},
#     'B': {'D': 2, 'E': 5},
#     'C': {'F': 3},
#     'D': {},
#     'E': {'F': 1},
#     'F': {}
# }

# heuristics = {
#     'A': 7,
#     'B': 6,
#     'C': 2,
#     'D': 1,
#     'E': 0,
#     'F': 0
# }
graph = {
    'A': {'B': 1, 'C': 1},
    'B': {'E': 1},
    'C': {'G': 1},
    'E': {},
    'G': {}
}
heuristics = {
    'A': 4,
    'B': 2,
    'C': 3,
    'E': 1,
    'G': 0
}



def heuristic(node):
    return heuristics.get(node, float('inf'))

def bestfs(graph, start, goal):
    open_list = [start]
    closed_list = []
    parent = {start: None}
    step = 1

    while open_list:
        print("\nStep", step)
        print("OPEN:", open_list)
        print("CLOSED:", closed_list)

        current = min(open_list, key=heuristic)
        print("Selected node:", current)

        if current == goal:
            path = []
            while current is not None:
                path.append(current)
                current = parent[current]
            return path[::-1]

        open_list.remove(current)
        closed_list.append(current)

        for neighbor in graph[current]:
            if neighbor not in open_list and neighbor not in closed_list:
                parent[neighbor] = current
                open_list.append(neighbor)

        step +=1

    return None

def main():
    start = input("Enter start node: ")
    goal = input("Enter goal node: ")

    if start not in graph or goal not in graph:
        print("Invalid node")
        return

    path = bestfs(graph, start, goal)

    if path:
        print("\nPath found:", " -> ".join(path))
    else:
        print("No path found")

main()