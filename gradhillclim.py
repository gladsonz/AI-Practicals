def simple_hill_climbing(graph, start, heuristic_values):
    current = start
    path = [current]
    step = 1
    
    while True:
        neighbors = graph.get(current, [])
        next_node = None
        
        for neighbor in neighbors:
            if heuristic_values[neighbor] < heuristic_values[current]:
                    next_node = neighbor
                    break
                
        if next_node is None:
            break 
            
        current = next_node
        path.append(current)
        step += 1
        
    return path

if __name__ == "__main__":
    graph = {}
    heuristic_values = {}
    
    while True:
        node = input("Enter node (or 'done' to finish): ").strip()
        if node.lower() == 'done':
            break
        neighbors = input(f"Enter neighbors for {node}: ").strip()
        graph[node] = [n.strip() for n in neighbors if n.strip()]
    
    print("\nEnter heuristic values:")
    for node in graph:
        value = int(input(f"Heuristic value for {node}: "))
        heuristic_values[node] = value
    
    start_node = input("\nEnter start node: ").strip()
    final_path = simple_hill_climbing(graph, start_node, heuristic_values)
    
    print(" -> ".join(final_path))