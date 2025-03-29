import tkinter as tk
from tkinter import messagebox

def check_winner():
    for combo in [ [0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]:
        if buttons[combo[0]]["text"] == buttons[combo[1]]["text"] == buttons[combo[2]]["text"] !="":
            buttons[combo[0]].config(bg="green")
            buttons[combo[1]].config(bg="green")
            buttons[combo[2]].config(bg="green")
            messagebox.showinfo ("Tic-Tac-Toe", f"player {buttons [combo[0]]  ['text']}  Wins!" )
            root.quit()


#user button per click kre to user symbol display in screen
#check user to empty box

def button_click(index):
    if buttons [index]["text"] == "" and not winner:
        buttons [index]["text"] = current_player
        check_winner()
        toggle_player()

#toggle function used exchange of user symbol i.e (o or x)

def toggle_player():
    global current_player
    current_player = "X" if current_player == "O" else "O"
    label.config (text=f"player {current_player}'s turn")


#Root window
root = tk.Tk()
root.title("Tic-Tac-Toe")

#create 9 buttons 
buttons = [tk.Button(root, text= "",font =("normal",50),width=9,height=2,command=lambda i=i:button_click(i)) for i in range(9)]


#set button in row and column

for i,button in enumerate(buttons):
    button.grid(row = i // 3, column = i % 3)


current_player = "X"
winner = False
label = tk.Label(root,text=f"player {current_player}'s turn", font=("'normal",16))
label.grid(row=3 , column=0,columnspan=3)

root.mainloop()