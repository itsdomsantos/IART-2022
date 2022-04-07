import board
import numpy as np


def main():
    game = board.Board("level1.txt")
    print(game.pieces)
    a = np.array(game.board)
    for line in a:
        print('  '.join(map(str, line)))


main()
