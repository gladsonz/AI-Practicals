from collections import deque

TOTAL_M = 3
TOTAL_C = 3


def is_valid(m_left, c_left):
    m_right = TOTAL_M - m_left
    c_right = TOTAL_C - c_left

    if m_left < 0 or c_left < 0 or m_left > TOTAL_M or c_left > TOTAL_C:
        return False

    if m_left > 0 and c_left > m_left:
        return False

    if m_right > 0 and c_right > m_right:
        return False

    return True


def bfs(initial_state):
    queue = deque()
    visited = set()

    
    queue.append((initial_state, [initial_state]))
    visited.add(initial_state)

    moves = [(2,0), (0,2), (1,1), (1,0), (0,1)]

    while queue:
        state, path = queue.popleft()
        m_left, c_left, boat = state

       
        if state == (0,0,0):
            return path

        for m, c in moves:
            if boat == 1:   
                new_state = (m_left - m, c_left - c, 0)
            else:           
                new_state = (m_left + m, c_left + c, 1)

            if new_state not in visited and is_valid(new_state[0], new_state[1]):
                visited.add(new_state)
                queue.append((new_state, path + [new_state]))

    return None


initial_state = (3, 3, 1)

solution = bfs(initial_state)

if solution:
    print("Shortest Solution Found:\n")
    for step in solution:
        print(step)
else:
    print("No Solution Found")