# N-Queens Problem using Backtracking

n = int(input("Enter number of queens (N): "))

board = [-1] * n     # board[i] = column position of queen in row i
solution_count = 0

def is_safe(row, col):
    for r in range(row):
        c = board[r]
        if c == col:                          # same column
            return False
        if abs(c - col) == abs(r - row):      # same diagonal
            return False
    return True

def print_board():
    for r in range(n):
        line = ""
        for c in range(n):
            line += "Q " if board[r] == c else ". "
        print(line)
    print()

def solve(row):
    global solution_count
    if row == n:
        solution_count += 1
        print(f"Solution {solution_count}:")
        print_board()
        return

    for col in range(n):
        if is_safe(row, col):
            board[row] = col
            solve(row + 1)
            board[row] = -1        # backtrack

solve(0)

if solution_count == 0:
    print("No solution exists")
else:
    print(f"Total solutions: {solution_count}")