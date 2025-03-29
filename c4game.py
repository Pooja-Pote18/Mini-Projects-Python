def print_board(board):
    for row in board:
        print(" ".join(row))
    print()

def check_winner(board,player):
    for row in board:
        for i in range(4):
            if all(piece == player for piece in row[i : i+4]):
                return True
            
    for col in range(7):
        for i in range(3):
            if all(row[col] == player for row in board [i : i+4]):
                return True
                
    for row in range(3):
        for i in range(3):
            if all(board[row+i] [col+i] == player for i in range(4)):
                return True
            
    for row in range(3,6):
        for col in range(4):
            if all(board[row-i] [col+i] == player for i in range(4)):
                return True
            
    return False
                     

def is_full(board):
    return all(piece != ' ' for row in board for piece in row)

def main():
    board = [[' ' for _ in range(7)] for _ in range(6)]
    player = 'X'

    while True:
        print_board(board)
        column = int(input(f"Player {player} enter a col 0-6  :"))

        if column < 0 or column > 6:
            print("Input is not Valid!")

        for row in range(5,-1,-1):
            if board[row] [column] == ' ':
                board[row] [column] = player
                break
            else:
                print("The column is Full!")
                continue

        if check_winner(board , player):
            print_board(board)
            print(f"Player {player} Wins!")
            break

        if is_full(board):
            print_board(board)
            print("Tie!")
            break

        player = 'O' if  player == 'X' else 'X'

main()    
            
