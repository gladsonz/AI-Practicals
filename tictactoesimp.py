import math

win = [
    [0,1,2],[3,4,5],[6,7,8],
    [0,3,6],[1,4,7],[2,5,8],
    [0,4,8],[2,4,6]
]

def winner(b):
    for i in win:
        if b[i[0]] == b[i[1]] == b[i[2]] != " ":
            return b[i[0]]
    if " " not in b:
        return "Draw"
    return None

def minimax(b, maxi):
    w = winner(b)
    if w == "X": return 1
    if w == "O": return -1
    if w == "Draw": return 0

    if maxi:
        best = -math.inf
        for i in range(9):
            if b[i] == " ":
                b[i] = "X"
                best = max(best, minimax(b, False))
                b[i] = " "
        return best
    else:
        best = math.inf
        for i in range(9):
            if b[i] == " ":
                b[i] = "O"
                best = min(best, minimax(b, True))
                b[i] = " "
        return best

def ai_move(b):
    best = math.inf
    move = -1

    for i in range(9):
        if b[i] == " ":
            b[i] = "O"
            score = minimax(b, True)
            b[i] = " "
            if score < best:
                best = score
                move = i
    return move

def show(b):
    for i in range(0,9,3):
        print(b[i:i+3])

board = [" "] * 9

while winner(board) is None:
    show(board)
    x = int(input("Enter position (1-9): ")) - 1

    if board[x] == " ":
        board[x] = "X"

        if winner(board):
            break

        board[ai_move(board)] = "O"

show(board)

if winner(board) == "X":
    print("You Win!")
elif winner(board) == "O":
    print("AI Wins!")
else:
    print("Draw!")