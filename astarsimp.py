import heapq
import math

graph = {
    'A':[('B',1),('C',4)],
    'B':[('D',2),('E',5)],
    'C':[('F',3)],
    'D':[('G',4)],
    'E':[('G',1)],
    'F':[('G',2)],
    'G':[]
}

h = {
    'A':7,
    'B':6,
    'C':4,
    'D':4,
    'E':1,
    'F':2,
    'G':0
}

def astar(start, goal):

    open_list = [(h[start], 0, start, [start])]   # (f,g,node,path)
    closed = []
    g_score = {start:0}

    while open_list:

        print("\nOPEN :", [(n,f) for f,g,n,p in open_list])
        print("CLOSED:", closed)

        f,g,node,path = heapq.heappop(open_list)

        if node == goal:
            print("\nPath :", " -> ".join(path))
            print("Cost :", g)
            return

        if node in closed:
            continue

        closed.append(node)

        for nxt,cost in graph[node]:

            new_g = g + cost

            if nxt not in g_score or new_g < g_score[nxt]:

                g_score[nxt] = new_g
                new_f = new_g + h[nxt]

                heapq.heappush(
                    open_list,
                    (new_f, new_g, nxt, path+[nxt])
                )

astar('A','G')