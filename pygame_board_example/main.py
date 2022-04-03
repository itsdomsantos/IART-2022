import display
size = 0
def readBoard():
    f = open("level1.txt", 'r')
    size = f.read()
    print size
    f.close()


def main():
    readBoard()
    p1 = display.Display(5)

    while True:
        display.draw_board(p1)


main()
