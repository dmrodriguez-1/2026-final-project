import os
import random
import sys                     # **new** needed for sys.exit()

# Clear screen function
def clear():
    os.system("cls" if os.name == "nt" else "clear")

# Scoreboard
x_wins = 0
o_wins = 0
ties = 0

# Print board
def print_board(board):
    print(f"""
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

# **new** helper routines for player‑vs‑computer mode
def computer_move(board, p):
    """very simple AI – take the first free square (same as hint) or pick
    a random empty cell if the hint returned None."""
    idx = hint(board)
    if idx is not None:
        return idx - 1
    empties = [i for i, v in enumerate(board) if v == " "]
    return random.choice(empties)

def show_scoreboard():
    print(f"Scoreboard: X={x_wins} | O={o_wins} | Ties={ties}")

# Main game loop (modified/extended – original logic is unchanged, new
# code is marked)
clear()
print("Welcome to Tic Tac Toe!")

# **new**: mode selection and optional computer opponent
mode = ""
while mode not in ("1", "2"):
    mode = input("Choose mode: 1) Two players  2) Play against computer\n> ")
p1 = input("Enter name for Player X: ")
if mode == "1":
    p2 = input("Enter name for Player O: ")
else:
    p2 = "Computer"              # computer will always be O here

while True:
    board = [" "] * 9
    turn = random.choice(["X", "O"])  # random first player
    comp_symbol = "O" if mode == "2" else None   # track computer symbol

    while True:
        clear()
        print_board(board)
        show_scoreboard()          # **new**
        # only show hint to human player
        if not (mode == "2" and turn == comp_symbol):
            print(f"Hint: Try spot {hint(board)}")

        player_name = p1 if turn == "X" else p2

        # **new**: if it's the computer's turn, pick a move automatically
        if mode == "2" and turn == comp_symbol:
            move = computer_move(board, turn)
        else:
            move = input(f"{player_name}'s turn ({turn}). "
                         "Choose 1-9, 'score' to view scores or 'end' to quit: ")

            if move.lower() == "end":
                clear()
                print("Thanks for playing!")
                sys.exit()

            if move.lower() == "score":   # **new** command
                clear()
                show_scoreboard()
                input("press Enter to continue...")
                continue

            if not move.isdigit() or not 1 <= int(move) <= 9:
                continue
            move = int(move) - 1

        if board[move] != " ":
            continue

        board[move] = turn

        if check_win(board, turn):
            clear()
            print_board(board)
            print(f"{player_name} ({turn}) wins!")
            if turn == "X":
                x_wins += 1
            else:
                o_wins += 1
            break

        if " " not in board:
            clear()
            print_board(board)
            print("It's a tie!")
            ties += 1
            break

        turn = "O" if turn == "X" else "X"

    again = input("Play again? (yes/no): ").lower()
    if again != "yes":
        clear()
        print("Final Scoreboard:")
        print(f"X Wins: {x_wins}")
        print(f"O Wins: {o_wins}")
        print(f"Ties: {ties}")
        print("Thanks for playing!")
        break