import display
import board

def main():
    game = board.Board("level1.txt")
    print(game.pieces)
    p1 = display.Display(game.size)

    while True:
        p1.draw_board()


main()
