import board
from snake import Snake
import numpy as np

def main():
    snake = Snake()
    game = board.Board("level1.txt", snake)
    while game.gameIsOn:
        game.printBoard()
        value = str(input())
        if value == "w" or value == "s" or value == "a" or value == "d":
            game.processInput(value)


if __name__ == '__main__':
    main()
