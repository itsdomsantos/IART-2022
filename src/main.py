import board
import numpy as np




def main():
    gameIsOn = True
    game = board.Board("level1.txt")
    while gameIsOn == True:
        print(game.pieces)
        a = np.array(game.board)
        for line in a:
            print('  '.join(map(str, line)))
        value = str(raw_input())
        if (value == "w" or value == "s" or value == "a" or value == "d"):
            game.processInput(value)


if __name__ == '__main__':
    main()
