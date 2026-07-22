import heapq

class Node:
    def __init__(self, state, g=0, h=0, parent=None):
        self.state = state
        self.g = g
        self.h = h
        self.f = g + h
        self.parent = parent

    def __lt__(self, other):
        return self.f < other.f

graph = {
    'A': [('B', 1), ('C', 4)],
    'B': [('D', 2), ('E', 5)],
    'C': [('F', 3)],
    'D': [('G', 4)],
    'E': [('G', 1)],
    'F': [('G', 2)],
    'G': []
}

heuristics = {
    'A': 7,
    'B': 6,
    'C': 4,
    'D': 4,
    'E': 1,
    'F': 2,
    'G': 0
}

def get_neighbors(state):
    return graph[state]

def heuristic(state):
    return heuristics[state]

def display_list(name, nodes):
    print(f"\n{name}:")
    
    if not nodes:
        print("Empty")
        return
    
    for node in nodes:
        src = node.parent.state if node.parent else "-"
        print(
            f"(dest={node.state}, src={src}, "
            f"g={node.g}, h={node.h}, f={node.f})"
        )

def a_star(start_state, goal_state):
    open_list = []
    closed_list = []
    closed_set = set()
    g_scores = {start_state: 0}

    start_node = Node(start_state, 0, heuristic(start_state))
    heapq.heappush(open_list, start_node)

    while open_list:
        display_list("OPEN", open_list)
        display_list("CLOSED", closed_list)

        current = heapq.heappop(open_list)

        if current.state in closed_set:
            continue

        print(f"\nSelected Node: {current.state}")

        if current.state == goal_state:
            path = []
            total_cost = current.g

            while current:
                path.append(current.state)
                current = current.parent

            path.reverse()

            print("\nGoal Reached")
            print("Path:", " -> ".join(path))
            print("Total Cost:", total_cost)
            return path

        closed_set.add(current.state)
        closed_list.append(current)

        for neighbor_state, cost in get_neighbors(current.state):
            tentative_g = current.g + cost

            if neighbor_state in g_scores and tentative_g >= g_scores[neighbor_state]:
                continue

            g_scores[neighbor_state] = tentative_g
            h = heuristic(neighbor_state)

            neighbor_node = Node(
                neighbor_state,
                tentative_g,
                h,
                current
            )

            heapq.heappush(open_list, neighbor_node)

    print("\nNo Path Found")
    return None

a_star('A', 'G')