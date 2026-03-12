import os
import random
import sys

# Clear screen function
def clear():
    os.system("cls" if os.name == "nt" else "clear")

# Scoreboard
x_wins = 0
o_wins = 0
ties = 0

# Print board + move count
def print_board(board, move_count):
    print(f"""
Move #{move_count}
 {board[0]} | {board[1]} | {board[2]}
---+---+---
 {board[3]} | {board[4]} | {board[5]}
---+---+---
 {board[6]} | {board[7]} | {board[8]}
""")

# Win check
def check_win(board, p):
    wins = [
        [0,1,2],[3,4,5],[6,7,8],
        [0,3,6],[1,4,7],[2,5,8],
        [0,4,8],[2,4,6]
    ]
    return any(all(board[i] == p for i in w) for w in wins)

# Hint system (first open spot)
def hint(board):
    for i in range(9):
        if board[i] == " ":
            return i + 1
    return None

# computer move logic
def computer_move(board, p, difficulty):
    empties = [i for i, v in enumerate(board) if v == " "]

    if difficulty == "easy":
        idx = hint(board)
        if idx is not None:
            return idx - 1
        return random.choice(empties)

    if difficulty == "medium":
        opponent = "O" if p == "X" else "X"
        for i in empties:
            board[i] = p
            if check_win(board, p):
                board[i] = " "
                return i
            board[i] = " "
        for i in empties:
            board[i] = opponent
            if check_win(board, opponent):
                board[i] = " "
                return i
            board[i] = " "
        return random.choice(empties)

    opponent = "O" if p == "X" else "X"
    def minimax(b, player):
        if check_win(b, p): return 1
        if check_win(b, opponent): return -1
        if " " not in b: return 0
        scores = []
        for j in range(9):
            if b[j] == " ":
                b[j] = player
                score = minimax(b, opponent if player == p else p)
                b[j] = " "
                scores.append(score)
        return max(scores) if player == p else min(scores)

    best_score = -2
    best_move = None
    for i in empties:
        board[i] = p
        score = minimax(board, opponent)
        board[i] = " "
        if score > best_score:
            best_score = score
            best_move = i
    return best_move

def show_scoreboard():
    print(f"Scoreboard: X={x_wins} | O={o_wins} | Ties={ties}")

# main loop
clear()
print("Welcome to Tic Tac Toe!")

mode = ""
while mode not in ("1", "2"):
    mode = input("Choose mode: 1) Two players  2) Play against computer\n> ")
p1 = input("Enter name for Player 1: ")

# symbol choice
sym1 = ""
while sym1 not in ("X","O"):
    sym1 = input("Choose your symbol (X/O): ").upper()
sym2 = "O" if sym1 == "X" else "X"

if mode == "1":
    p2 = input("Enter name for Player 2: ")
    difficulty = None
else:
    p2 = "Computer"
    diff = ""
    while diff not in ("1","2","3"):
        diff = input("Choose difficulty: 1) Easy  2) Medium  3) Hard\n> ")
    difficulty = {"1":"easy","2":"medium","3":"hard"}[diff]

while True:
    board = [" "] * 9
    history = []
    move_count = 1
    turn = random.choice([sym1, sym2])
    comp_symbol = sym2 if mode == "2" else None

    while True:
        clear()
        print_board(board, move_count)
        show_scoreboard()
        if not (mode == "2" and turn == comp_symbol):
            print(f"Hint: Try spot {hint(board)}")

        player_name = p1 if turn == sym1 else p2

        if mode == "2" and turn == comp_symbol:
            move = computer_move(board, turn, difficulty)
        else:
            move = input(f"{player_name}'s turn ({turn}). "
                         "Choose 1-9, 'undo', 'score' or 'end': ")

            if move.lower() == "end":
                clear(); print("Thanks for playing!"); sys.exit()
            if move.lower() == "score":
                clear(); show_scoreboard(); input("press Enter to continue..."); continue
            if move.lower() == "undo" and history:
                board[history.pop()] = " "
                turn = "O" if turn == "X" else "X"
                move_count -= 1
                continue
            if not move.isdigit() or not 1 <= int(move) <= 9:
                continue
            move = int(move) - 1

        if board[move] != " ": continue

        history.append(move)
        board[move] = turn

        if check_win(board, turn):
            clear(); print_board(board, move_count)
            print(f"{player_name} ({turn}) wins!")
            if turn == "X": x_wins += 1
            else: o_wins += 1
            break

        if " " not in board:
            clear(); print_board(board, move_count)
            print("It's a tie!")
            ties += 1
            break

        turn = "O" if turn == "X" else "X"
        move_count += 1

    again = input("Play again? (yes/no): ").lower()
    if again != "yes":
        clear()
        print("Final Scoreboard:")
        print(f"X Wins: {x_wins}")
        print(f"O Wins: {o_wins}")
        print(f"Ties: {ties}")
        print("Thanks for playing!")
        break