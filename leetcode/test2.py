def valid(m,c):

    if m<0 or c<0 or m>3 or c>3:
        return False

    if m>0 and m<c:
        return False

    if (3-m)>0 and (3-m)<(3-c):
        return False

    return True


def dfs():

    start=(3,3,1)
    goal=(0,0,0)

    stack=[(start,[start])]
    visited={start}

    moves=[(1,0),(2,0),(0,1),(0,2),(1,1)]

    while stack:

        (m,c,b),path=stack.pop()

        if (m,c,b)==goal:

            print("Solution")

            for s in path:
                print(s)

            return

        for dm,dc in moves:

            if b:
                nxt=(m-dm,c-dc,0)
            else:
                nxt=(m+dm,c+dc,1)

            if valid(nxt[0],nxt[1]) and nxt not in visited:

                visited.add(nxt)

                stack.append((nxt,path+[nxt]))

dfs()