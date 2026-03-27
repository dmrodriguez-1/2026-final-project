import os, random, tkinter as tk
from tkinter import messagebox, simpledialog
import pygame
from pathlib import Path
import winsound  # For simple sound effects on Windows

def check_win(board, p):
    wins = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]
    return any(all(board[i]==p for i in w) for w in wins)

def hint(board):
    for i in range(9):
        if board[i]==" ": return i+1
    return None

def computer_move(board, p, difficulty):
    empties=[i for i,v in enumerate(board) if v==" "]
    if not empties: return None
    if difficulty=="easy":
        idx=hint(board)
        if idx is not None: return idx-1
        return random.choice(empties)
    if difficulty=="medium":
        opp="O" if p=="X" else "X"
        for i in empties:
            board[i]=p
            if check_win(board,p): board[i]=" "; return i
            board[i]=" "
        for i in empties:
            board[i]=opp
            if check_win(board,opp): board[i]=" "; return i
            board[i]=" "
        return random.choice(empties)
    opp="O" if p=="X" else "X"
    def minimax(b,player):
        if check_win(b,p): return 1
        if check_win(b,opp): return -1
        if " " not in b: return 0
        scores=[]
        for j in range(9):
            if b[j]==" ":
                b[j]=player
                score=minimax(b,opp if player==p else p)
                b[j]=" "
                scores.append(score)
        return max(scores) if player==p else min(scores)
    best_score=-2; best_move=None
    for i in empties:
        board[i]=p
        score=minimax(board,opp)
        board[i]=" "
        if score>best_score:
            best_score=score; best_move=i
    return best_move

def main():
    root = tk.Tk()
    root.withdraw()

    def show_title_screen():
        """Display full-screen title screen"""
        root.title("TIC TAC TOE")
        root.attributes('-fullscreen', True)
        root.configure(bg='#1a1a1a')
        root.deiconify()
        
        # Main frame for title
        title_frame = tk.Frame(root, bg='#1a1a1a')
        title_frame.pack(fill=tk.BOTH, expand=True)
        
        # Main title
        title_label = tk.Label(title_frame, text="TIC TAC TOE", font=("Arial", 120, "bold"), fg="#00FF00", bg='#1a1a1a')
        title_label.pack(expand=True)
        
        # Subtitle
        subtitle_label = tk.Label(title_frame, text="Click or Press Any Key to Start", font=("Arial", 28), fg="#00AA00", bg='#1a1a1a')
        subtitle_label.pack(pady=20)
        
        def close_title(event=None):
            try:
                root.unbind('<Button-1>')
                root.unbind('<Key>')
                title_frame.destroy()
                root.attributes('-fullscreen', True)  # Keep full screen for main game
            except:
                pass
        
        title_frame.bind('<Button-1>', close_title)
        root.bind('<Button-1>', close_title)
        root.bind('<Key>', close_title)
        
        # Auto close after 3 seconds if no interaction
        root.after(3000, close_title)
        
        # Wait for title frame to be destroyed
        root.wait_window(title_frame)

    show_title_screen()

    mode = simpledialog.askstring("Mode", "Choose mode: 1=Two players, 2=Computer", parent=root)
    if mode not in ("1", "2"):
        messagebox.showerror("Error", "Invalid mode; defaulting to Computer.")
        mode = "2"

    difficulty = "hard"
    if mode == "2":
        diff = simpledialog.askstring("Difficulty", "Choose difficulty:\n1=Easy\n2=Medium\n3=Hard", parent=root)
        difficulty = {"1": "easy", "2": "medium", "3": "hard"}.get(diff, "hard")

    player1_name = simpledialog.askstring("Name", "Enter Player 1 name:", parent=root) or "Player 1"
    if mode == "1":
        player2_name = simpledialog.askstring("Name", "Enter Player 2 name:", parent=root) or "Player 2"
    else:
        player2_name = "Computer"

    human_symbol = "X"
    computer_symbol = "O"
    if mode == "2":
        sch = simpledialog.askstring("Symbol", "Pick your symbol X/O (computer gets other)", parent=root)
        if sch and sch.upper() in ("X", "O"):
            human_symbol = sch.upper()
            computer_symbol = "O" if human_symbol == "X" else "X"

    root.deiconify()
    root.update()  # Ensure window updates properly
    board = [" "] * 9
    buttons = []
    score = {"X": 0, "O": 0, "Ties": 0}
    turn = "X"
    sound_enabled = True  # Track if sounds are enabled

    # Initialize pygame mixer for potential future music
    pygame.mixer.init()
    music_file = os.path.join("assets", "background_music.mp3")
    if os.path.exists(music_file):
        try:
            pygame.mixer.music.load(music_file)
            pygame.mixer.music.play(-1)  # -1 means loop infinitely
            pygame.mixer.music.set_volume(0.5)
        except:
            pass  # If music file fails to load, continue without music

    img_x = tk.PhotoImage(file=os.path.join("assets", "pixil-frame-0.png"))
    img_o = tk.PhotoImage(file=os.path.join("assets", "pixil-frame-0 (1).png"))
    empty_img = tk.PhotoImage(width=1, height=1)

    def update_title():
        mode_label = "CPU" if mode == "2" else "2-player"
        current_name = player1_name if turn == "X" else player2_name
        root.title(f"{current_name} ({turn}) - {mode_label} | X:{score['X']} O:{score['O']} T:{score['Ties']}")

    def refresh_hint():
        hint_label.config(text=f"Hint: {hint(board)}")

    def reset_board():
        nonlocal board, turn
        board = [" "] * 9
        for b in buttons:
            b.config(image=empty_img)
        turn = "X"
        update_title()
        refresh_hint()
        if mode == "2" and turn == computer_symbol:
            root.after(200, cpu_move)

    def show_end_screen(winner):
        """Display full-screen end game screen with Play Again and End buttons"""
        end_window = tk.Toplevel(root)
        end_window.title("Game Over")
        end_window.attributes('-fullscreen', True)
        end_window.configure(bg='#1a1a1a')
        end_window.grab_set()
        
        # Create message
        if winner in ("X", "O"):
            winner_name = player1_name if winner == "X" else player2_name
            message = f"{winner_name} ({winner}) WINS!"
            color = "#00FF00"
            if sound_enabled:
                winsound.Beep(800, 200)  # Win sound
        else:
            message = "It's a TIE!"
            color = "#FFFF00"
            if sound_enabled:
                winsound.Beep(500, 200)  # Tie sound
        
        title_label = tk.Label(end_window, text=message, font=("Arial", 100, "bold"), fg=color, bg='#1a1a1a')
        title_label.pack(pady=50, expand=True)
        
        score_label = tk.Label(end_window, text=f"Score - X:{score['X']} O:{score['O']} Ties:{score['Ties']}", font=("Arial", 32), fg="#00AA00", bg='#1a1a1a')
        score_label.pack(pady=30)
        
        # Button frame
        button_frame = tk.Frame(end_window, bg='#1a1a1a')
        button_frame.pack(pady=50, expand=True)
        
        def play_again():
            end_window.destroy()
            reset_board()
        
        def end_game_action():
            pygame.mixer.music.stop()
            end_window.destroy()
            root.quit()
        
        play_btn = tk.Button(button_frame, text="Play Again", font=("Arial", 28), command=play_again, width=20, bg='#00AA00', fg='#000000', activebackground='#00FF00')
        play_btn.grid(row=0, column=0, padx=30)
        
        end_btn = tk.Button(button_frame, text="Exit", font=("Arial", 28), command=end_game_action, width=20, bg='#AA0000', fg='#FFFFFF', activebackground='#FF0000')
        end_btn.grid(row=0, column=1, padx=30)

    def end_game(winner):
        if winner in ("X", "O"):
            score[winner] += 1
        else:
            score["Ties"] += 1
        show_end_screen(winner)

    def check_game_over():
        if check_win(board, turn):
            end_game(turn)
            return True
        if " " not in board:
            end_game(None)
            return True

    def play(i):
        nonlocal turn
        if board[i] != " ":
            return
        board[i] = turn
        buttons[i].config(image=img_x if turn == "X" else img_o)
        if sound_enabled:
            winsound.Beep(600, 50)  # Move sound
        if check_game_over():
            return
        turn = "O" if turn == "X" else "X"
        update_title()
        refresh_hint()
        if mode == "2" and turn == computer_symbol:
            root.after(250, cpu_move)

    def cpu_move():
        nonlocal turn
        move = computer_move(board, computer_symbol, difficulty)
        if move is None:
            return
        board[move] = computer_symbol
        buttons[move].config(image=img_x if computer_symbol == "X" else img_o)
        if sound_enabled:
            winsound.Beep(600, 50)  # Computer move sound
        if check_win(board, computer_symbol):
            end_game(computer_symbol)
            return
        if " " not in board:
            end_game(None)
            return
        turn = "O" if computer_symbol == "X" else "X"
        update_title()
        refresh_hint()

    def choose_symbol():
        nonlocal human_symbol, computer_symbol
        s = simpledialog.askstring("Choose symbol", "Pick X or O", parent=root)
        if s and s.upper() in ("X", "O"):
            human_symbol = s.upper()
            computer_symbol = "O" if human_symbol == "X" else "X"
            reset_board()
        else:
            messagebox.showwarning("Oops", "Choose X or O please.")

    def switch_mode():
        nonlocal mode
        mode = "1" if mode == "2" else "2"
        messagebox.showinfo("Mode switched", "2-player mode" if mode == "1" else "Computer mode")
        reset_board()

    # Menu functions
    def toggle_sounds():
        nonlocal sound_enabled
        sound_enabled = not sound_enabled
        messagebox.showinfo("Sounds", "Sounds " + ("enabled" if sound_enabled else "disabled"))

    def restart_game():
        reset_board()  # Restart by resetting the board

    def end_game_action():
        pygame.mixer.music.stop()
        root.quit()

    # Create popup menu for the Menu button
    popup_menu = tk.Menu(root, tearoff=0)
    popup_menu.add_command(label="Toggle Sounds", command=toggle_sounds)
    popup_menu.add_command(label="Restart", command=restart_game)  # Changed from "Resume" to "Restart"
    popup_menu.add_separator()
    popup_menu.add_command(label="End Game", command=end_game_action)

    def show_menu(event):
        popup_menu.post(event.x_root, event.y_root)

    # Create a main frame to hold the board and center it
    main_frame = tk.Frame(root, bg='#1a1a1a')
    main_frame.pack(expand=True)  # This centers the frame in the window

    for i in range(9):
        btn = tk.Button(main_frame, image=empty_img, width=120, height=120, command=lambda i=i: play(i), bg='#333333', activebackground='#555555')
        btn.grid(row=i//3, column=i%3)
        buttons.append(btn)

    # Hint label and Menu button in the same row
    hint_label = tk.Label(main_frame, text=f"Hint: {hint(board)}", font=("Arial", 12), fg="#00AA00", bg='#1a1a1a')
    hint_label.grid(row=3, column=0, columnspan=2, pady=8, sticky='w')

    menu_button = tk.Button(main_frame, text="Menu", font=("Arial", 12), command=lambda: None, bg='#555555', fg='#FFFFFF')
    menu_button.grid(row=3, column=2, pady=8, sticky='e')
    menu_button.bind("<Button-1>", show_menu)

    update_title()
    root.mainloop()

if __name__ == "__main__":
    main()