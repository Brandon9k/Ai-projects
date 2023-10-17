#Tic Tac Toe game with artificial intelligence Min-Max Implementation 
import sys

# Tic-tac-toe game board
GameBoard = [[' ' for _ in range(3)] for _ in range(3)]

# Print current game board
def PrintGameBoard():
    print('-------------')
    for row in GameBoard:
        print('|', end=' ')
        for cell in row:
            print(cell, end=' | ')
        print('\n-------------')

# Check if game board is full
def GameBoardFull():
    for row in GameBoard:
        if ' ' in row:
            return False
    return True

# Check if a player has won
def CheckWinner(player):
    for i in range(3):
        # Rows
        if GameBoard[i][0] == GameBoard[i][1] == GameBoard[i][2] == player:
            return True
        # Columns
        if GameBoard[0][i] == GameBoard[1][i] == GameBoard[2][i] == player:
            return True
    # Diagonals
    if GameBoard[0][0] == GameBoard[1][1] == GameBoard[2][2] == player:
        return True
    if GameBoard[0][2] == GameBoard[1][1] == GameBoard[2][0] == player:
        return True
    return False

# Evaluate the score of a specific move
def Evaluate(GameBoard):
    if CheckWinner('X'):
        return -1
    elif CheckWinner('O'):
        return 1
    else:
        return 0

# Minimax
def Minimax(GameBoard, depth, maximizing):
    score = Evaluate(GameBoard)

    if score == 1:
        return score - depth
    elif score == -1:
        return score + depth
    elif GameBoardFull():
        return 0

    if maximizing:
        BestScore = -sys.maxsize
        for i in range(3):
            for j in range(3):
                if GameBoard[i][j] == ' ':
                    GameBoard[i][j] = 'O'
                    score = Minimax(GameBoard, depth + 1, False)
                    GameBoard[i][j] = ' '
                    BestScore = max(score, BestScore)
        return BestScore
    else:
        BestScore = sys.maxsize
        for i in range(3):
            for j in range(3):
                if GameBoard[i][j] == ' ':
                    GameBoard[i][j] = 'X'
                    score = Minimax(GameBoard, depth + 1, True)
                    GameBoard[i][j] = ' '
                    BestScore = min(score, BestScore)
        return BestScore

# Make a move using Minimax
def MakeMove():
    BestScore = -sys.maxsize
    BestMove = None

    for i in range(3):
        for j in range(3):
            if GameBoard[i][j] == ' ':
                GameBoard[i][j] = 'O'
                score = Minimax(GameBoard, 0, False)
                GameBoard[i][j] = ' '

                if score > BestScore:
                    BestScore = score
                    BestMove = (i, j)

    GameBoard[BestMove[0]][BestMove[1]] = 'O'

# Restart or quit the game
def Ending():
    while True:
        choice = input("Do you want to play again? (Y/N): ")
        if choice.upper() == 'Y':
            return True
        elif choice.upper() == 'N':
            return False
        else:
            print("Invalid choice. Please enter Y or N.")

# Run
def Main():
    print("Welcome to Tic-Tac-Toe!")
    print("You are 'X', and the computer is 'O'.")

    while True:
        PrintGameBoard()

        while not GameBoardFull():
            Row = int(input("Enter the row (1, 2, or 3): ")) - 1
            Column = int(input("Enter the column (1, 2, or 3): ")) - 1

            if Row < 0 or Row > 2 or Column < 0 or Column > 2 or GameBoard[Row][Column] != ' ':
                print("Invalid move. Try again.")
                continue

            GameBoard[Row][Column] = 'X'

            if CheckWinner('X'):
                PrintGameBoard()
                print("You won!")
                break

            if GameBoardFull():
                break

            MakeMove()

            if CheckWinner('O'):
                PrintGameBoard()
                print("You lost!")
                break

            PrintGameBoard()

        PrintGameBoard()
        if not Ending():
            break
        else:
            # Reset game board
            for i in range(3):
                for j in range(3):
                    GameBoard[i][j] = ' '

Main()
