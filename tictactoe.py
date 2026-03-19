import os, random, tkinter as tk
from tkinter import messagebox, simpledialog

def check_win(board,p):
    wins = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]
    return any(all(board[i]==p for i in w) for w in wins)

def hint(board):
    for i in range(9):
        if board[i]==" ": return i+1
    return None

def computer_move(board,p,difficulty):
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

root=tk.Tk(); root.withdraw()

mode=simpledialog.askstring("Mode","Choose mode: 1=Two players, 2=Computer",parent=root)
if mode not in ("1","2"):
    messagebox.showerror("Error","Invalid mode; defaulting to Computer.")
    mode="2"

difficulty="hard"
if mode=="2":
    diff=simpledialog.askstring("Difficulty","Choose difficulty:\n1=Easy\n2=Medium\n3=Hard",parent=root)
    difficulty={"1":"easy","2":"medium","3":"hard"}.get(diff,"hard")

player1_name=simpledialog.askstring("Name","Enter Player 1 name:",parent=root) or "Player 1"
if mode=="1":
    player2_name=simpledialog.askstring("Name","Enter Player 2 name:",parent=root) or "Player 2"
else:
    player2_name="Computer"

human_symbol="X"; computer_symbol="O"
if mode=="2":
    sch=simpledialog.askstring("Symbol","Pick your symbol X/O (computer gets other)",parent=root)
    if sch and sch.upper() in ("X","O"):
        human_symbol=sch.upper(); computer_symbol="O" if human_symbol=="X" else "X"

root.deiconify()
board=[" "]*9; buttons=[]; score={"X":0,"O":0,"Ties":0}; turn="X"

img_x=tk.PhotoImage(file=os.path.join("assets","pixil-frame-0.png"))
img_o=tk.PhotoImage(file=os.path.join("assets","pixil-frame-0 (1).png"))
empty_img=tk.PhotoImage(width=1,height=1)

def update_title():
    mode_label="CPU" if mode=="2" else "2-player"
    current_name=player1_name if turn=="X" else player2_name
    root.title(f"{current_name} ({turn}) - {mode_label} | X:{score['X']} O:{score['O']} T:{score['Ties']}")

def refresh_hint():
    hint_label.config(text=f"Hint: {hint(board)}")

def reset_board():
    global board, turn
    board=[" "]*9
    for b in buttons: b.config(image=empty_img)
    turn="X"; update_title(); refresh_hint()
    if mode=="2" and turn==computer_symbol:
        root.after(200,cpu_move)

def end_game(winner):
    if winner in ("X","O"):
        score[winner]+=1
        winner_name=player1_name if winner=="X" else player2_name
        messagebox.showinfo("Result",f"{winner_name} ({winner}) wins!")
    else:
        score["Ties"]+=1
        messagebox.showinfo("Result","Tie!")
    reset_board()

def check_game_over():
    if check_win(board,turn): end_game(turn); return True
    if " " not in board: end_game(None); return True
    return False

def play(i):
    global turn
    if board[i]!=" ": return
    board[i]=turn
    buttons[i].config(image=img_x if turn=="X" else img_o)
    if check_game_over(): return
    turn="O" if turn=="X" else "X"; update_title(); refresh_hint()
    if mode=="2" and turn==computer_symbol: root.after(250,cpu_move)

def cpu_move():
    global turn
    move=computer_move(board,computer_symbol,difficulty)
    if move is None: return
    board[move]=computer_symbol
    buttons[move].config(image=img_x if computer_symbol=="X" else img_o)
    if check_win(board,computer_symbol): end_game(computer_symbol); return
    if " " not in board: end_game(None); return
    turn="O" if computer_symbol=="X" else "X"; update_title(); refresh_hint()

def choose_symbol():
    global human_symbol, computer_symbol
    s=simpledialog.askstring("Choose symbol","Pick X or O",parent=root)
    if s and s.upper() in ("X","O"):
        human_symbol=s.upper(); computer_symbol="O" if human_symbol=="X" else "X"; reset_board()
    else:
        messagebox.showwarning("Oops","Choose X or O please.")

def switch_mode():
    global mode
    mode="1" if mode=="2" else "2"
    messagebox.showinfo("Mode switched","2-player mode" if mode=="1" else "Computer mode")
    reset_board()

for i in range(9):
    btn=tk.Button(root,image=empty_img,width=120,height=120,command=lambda i=i: play(i))
    btn.grid(row=i//3,column=i%3); buttons.append(btn)

hint_label=tk.Label(root,text=f"Hint: {hint(board)}")
hint_label.grid(row=3,column=0,columnspan=3,pady=8)

menu=tk.Menu(root); root.config(menu=menu)
m=tk.Menu(menu,tearoff=0); menu.add_cascade(label="Game",menu=m)
m.add_command(label="New Game",command=reset_board)
m.add_command(label="Switch Mode",command=switch_mode)
m.add_command(label="Choose Symbol",command=choose_symbol)
m.add_command(label="Quit",command=root.quit)

update_title(); root.mainloop()