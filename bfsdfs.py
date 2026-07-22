def bfs(graph, start,visited=None):
    if visited is None:
        visited = []
        visited.append(start)
    queue = [start]
    while queue:
        vertex = queue.pop(0)
        for neighbor in graph[vertex]:
            if neighbor not in visited:
                visited.append(neighbor)
                queue.append(neighbor)
    
    return visited

def dfs(graph, start, visited=None):
    if visited is None:
        visited = []
    visited.append(start)
    for neighbour in graph[start]:
        if neighbour not in visited:
            dfs(graph, neighbour, visited)
    return visited

print("example graph")
graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [],
    'E': ['F'],
    'F': []
}   
print("Graph:", graph)  
print("BFS:", bfs(graph, 'A'))
print("DFS:", dfs(graph, 'A'))


print("user input")

user_graph = {}
num_edges = int(input("Enter number of edges in the graph: "))
for _ in range(num_edges):  
    edge = input("Enter edge (format: node1 node2): ").split()
    node1, node2 = edge[0], edge[1]
    if node1 not in user_graph:
        user_graph[node1] = []
    user_graph[node1].append(node2)
    if node2 not in user_graph:
        user_graph[node2] = []

print("User Graph:", user_graph)
start_node = input("Enter the starting node for traversal: ")
print("BFS:", bfs(user_graph, start_node))
print("DFS:", dfs(user_graph, start_node))  
  