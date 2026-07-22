N = 4

board = [[0 for _ in range(N)] for _ in range(N)]

def is_safe(row, col):
    for i in range(col):
        if board[row][i] == 1:
            return False
    i = row
    j = col

    while i >= 0 and j >= 0:
        if board[i][j] == 1:
            return False
        i -= 1
        j -= 1

    i = row
    j = col

    while i < N and j >= 0:
        if board[i][j] == 1:
            return False
        i += 1
        j -= 1

    return True

def solve(col):
    if col >= N:
        return True

    for i in range(N):

        if is_safe(i, col):

            board[i][col] = 1

            if solve(col + 1):
                return True

            board[i][col] = 0

    return False

def print_solution():
    for i in range(N):
        for j in range(N):
            if board[i][j] == 1:
                print("Q", end=" ")
            else:
                print(".", end=" ")
        print()

if solve(0):
    print("Solution Found:\n")
    print_solution()
else:
    print("No Solution Exists")