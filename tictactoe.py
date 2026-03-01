import os
import random

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

# Main game loop
clear()
print("Welcome to Tic Tac Toe!")
p1 = input("Enter name for Player X: ")
p2 = input("Enter name for Player O: ")

while True:
    board = [" "] * 9
    turn = random.choice(["X", "O"])  # random first player

    while True:
        clear()
        print_board(board)
        print(f"Scoreboard: X={x_wins} | O={o_wins} | Ties={ties}")
        print(f"Hint: Try spot {hint(board)}")

        player_name = p1 if turn == "X" else p2
        move = input(f"{player_name}'s turn ({turn}). Choose 1-9 or 'end' to quit: ")

        if move.lower() == "end":
            clear()
            print("Thanks for playing!")
            exit()

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