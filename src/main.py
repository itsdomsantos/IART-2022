import board
import numpy as np




def main():
    gameIsOn = True
    game = board.Board("level1.txt")
    while gameIsOn == True:
        game.printBoard()
        value = str(input())
        if (value == "w" or value == "s" or value == "a" or value == "d"):
            game.processInput(value)


if __name__ == '__main__':
    main()
