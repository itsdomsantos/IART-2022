import board
from snake import Snake
import numpy as np


def main():
    print("Welcome to Chess Snake Game")
    print("Select the desired mode: ")
    print("Computer (c)    Multiplayer (m)")
    menuchoice = str(input())
    if menuchoice == "m":
        return 0
    if menuchoice == "c":
        snake = Snake()
        game = board.Board("level1.txt", snake)
        while game.gameIsOn:
            game.printBoard()
            print(game.manhattan_distance())
            for x in game.chess_pieces:
                print(x.type, x.attacks)
            value = str(input())
            if value == "w" or value == "s" or value == "a" or value == "d":
                game.processInput(value)
        if game.checkSum():
            print("All pieces attack an equal number of squares")
        else:
            print("Pieces have a different number of squares attacked")
        for x in game.chess_pieces:
            print(x.type, x.attacks)


if __name__ == '__main__':
    main()
