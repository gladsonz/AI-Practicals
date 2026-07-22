

TOTAL_M = 3
TOTAL_C = 3


def is_valid(m_left, c_left):
    m_right = TOTAL_M - m_left
    c_right = TOTAL_C - c_left

    
    if m_left < 0 or c_left < 0 or m_left > TOTAL_M or c_left > TOTAL_C:
        return False

    
    if (m_left > 0 and c_left > m_left):
        return False
    if (m_right > 0 and c_right > m_right):
        return False

    return True



def dfs(state, visited, path):
    m_left, c_left, boat = state

    
    if state == (0, 0, 0):
        path.append(state)
        return True

    visited.add(state)
    path.append(state)

    
    moves = [(2,0), (0,2), (1,1), (1,0), (0,1)]

    for m, c in moves:
        if boat == 1:  
            new_state = (m_left - m, c_left - c, 0)
        else:  
            new_state = (m_left + m, c_left + c, 1)

        if new_state not in visited and is_valid(new_state[0], new_state[1]):
            if dfs(new_state, visited, path):
                return True

    path.pop()
    return False


initial_state = (3, 3, 1)

visited = set()
path = []

if dfs(initial_state, visited, path):
    print("Solution Found:\n")
    for step in path:
        print(step)
else:
    print("No Solution Found")