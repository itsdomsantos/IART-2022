import pygame as pg


class Display:

    def __init__(self, size):
        self.board = [['  ' for i in range(size)] for i in range(size)]
        self.x = 0
        self.y = 0
        self.width = size * 100
        self.heigth = size * 100
        self.WHITE = (240, 240, 240)
        self.BLACK = (0, 0, 0)
        self.BLOCKSIZE = 100

    def draw_board(self):
        pg.init()
        screen = pg.display.set_mode((self.width, self.heigth))

        screen.fill('#BA8C63')
        for x in range(0, self.width, self.BLOCKSIZE):
            for y in range(0, self.heigth, self.BLOCKSIZE):
                rect = pg.Rect(x, y, self.BLOCKSIZE, self.BLOCKSIZE)
                pg.draw.rect(screen, self.BLACK, rect, 1)

        pg.display.update()

'''
class Piece:
    def __init__(self, team, type, image, killable=False):
        self.image = image
        self.team = team
        self.type = type
        self.killable = killable


bPawn = Piece('b', 'p', 'Pieces/bPawn.png')
wPawn = Piece('w', 'p', 'Pieces/wPawn.png')

bQueen = Piece('b', 'q', 'Pieces/bQueen.png')
wQueen = Piece('w', 'q', 'Pieces/wQueen.png')

bKnight = Piece('b', 'kn', 'Pieces/bKnight.png')
wKnight = Piece('w', 'kn', 'Pieces/wKnight.png')

bKing = Piece('b', 'k', 'Pieces/bKing.png')
wKing = Piece('w', 'k', 'Pieces/wKing.png')

bRook = Piece('b', 'r', 'Pieces/bRook.png')
wRook = Piece('w', 'r', 'Pieces/wRook.png')

bBishop = Piece('b', 'b', 'Pieces/bBishop.png')
wBishop = Piece('w', 'b', 'Pieces/wBishop.png')

startingOrder = {(0, 0): pg.image.load(wQueen.image), (1, 0): pg.image.load(wKing.image)}


def draw_board(self):
    self.board[0] = [Piece('w', 'q', 'Pieces/wQueen.png'), Piece('w', 'k', 'Pieces/wKing.png')]
    self.board[4] = [Piece('b', 'q', 'Pieces/bQueen.png'), Piece('b', 'k', 'Pieces/bKing.png')]

    pg.init()
    screen = pg.display.set_mode((self.width, self.heigth))

    screen.fill('#BA8C63')

    for x in range(0, self.width, self.BLOCKSIZE):
        for y in range(0, self.heigth, self.BLOCKSIZE):
            rect = pg.Rect(x, y, self.BLOCKSIZE, self.BLOCKSIZE)
            pg.draw.rect(screen, self.BLACK, rect, 1)
            bg = pg.image.load("Pieces/wKing.png");

    pg.display.update()
    
'''
