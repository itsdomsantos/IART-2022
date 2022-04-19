# <a href="https://www.flaticon.com/br/icones-gratis/letra-f" title="letra f ícones">Letra f ícones criados por Freepik - Flaticon</a>
# <a href="https://www.flaticon.com/br/icones-gratis/s" title="s ícones">S ícones criados por Freepik - Flaticon</a>
import pygame as pg


class Display:

    def __init__(self, size):
        self.size = size
        self.width = size * 100
        self.heigth = size * 100
        self.WHITE = (240, 240, 240)
        self.BLACK = (0, 0, 0)
        self.GREEN = (20, 200, 20)
        self.BLOCKSIZE = 100
        self.screen = 0
        self.king = pg.image.load("./Pieces/k.png")
        self.queen = pg.image.load("./Pieces/q.png")
        self.bishop = pg.image.load("./Pieces/b.png")
        self.rook = pg.image.load("./Pieces/r.png")
        self.knight = pg.image.load("./Pieces/n.png")
        self.pawn = pg.image.load("./Pieces/p.png")
        self.begin = pg.image.load("./Pieces/s.png")
        self.end = pg.image.load("./Pieces/f.png")

    def init_board(self):
        pg.init()
        self.screen = pg.display.set_mode((self.width, self.heigth))
        self.screen.fill(self.WHITE)
        pg.display.update()

    def update_board(self, board):
        for x in range(0, self.width, self.BLOCKSIZE):
            for y in range(0, self.heigth, self.BLOCKSIZE):
                if board[y // self.BLOCKSIZE][x // self.BLOCKSIZE] == "1":
                    self.add_square(x // self.BLOCKSIZE, y // self.BLOCKSIZE)
                else:
                    rect = pg.Rect(x, y, self.BLOCKSIZE, self.BLOCKSIZE)
                    pg.draw.rect(self.screen, self.BLACK, rect, 1)
        pg.display.update()

    def color_square(self, x, y, color):
        pg.draw.rect(self.screen, color,
                     pg.Rect(x * self.BLOCKSIZE + 1, y * self.BLOCKSIZE + 1, self.BLOCKSIZE - 2, self.BLOCKSIZE - 2))
        pg.display.update()

    def get_chess_piece(self, type):
        if type == 'p':
            return self.pawn
        elif type == 'n':
            return self.knight
        elif type == 'b':
            return self.bishop
        elif type == 'r':
            return self.rook
        elif type == 'q':
            return self.queen
        elif type == 'k':
            return self.king
        elif type == "s":
            return self.begin
        elif type == "f":
            return self.end

    def draw_chess_piece(self, type, position):
        image = self.get_chess_piece(type)
        pg.Surface.blit(self.screen, image, (position[0] * 100 + 21, position[1] * 100 + 21))
        pg.display.update()

    def delete_square(self, x, y):
        self.color_square(x, y, self.WHITE)
        if x == self.size-1 and y == 0:
            self.draw_chess_piece("f", (self.size - 1, 0))

    def add_square(self, x, y):
        self.color_square(x, y, self.GREEN)
        if x == self.size - 1 and y == 0:
            self.draw_chess_piece("f", (self.size - 1, 0))

    def draw_pieces(self, pieces):
        for x in pieces:
            self.draw_chess_piece(x.type, x.position)

    def draw_borders(self):
        self.add_square(0, self.size - 1)
        self.draw_chess_piece("s", (0, self.size - 1))
        self.draw_chess_piece("f", (self.size - 1, 0))

    def reset_board(self, board):
        self.screen.fill(self.WHITE)
        self.add_square(0, self.size - 1)
        self.draw_chess_piece("s", (0, self.size - 1))
        self.draw_chess_piece("f", (self.size - 1, 0))
        self.draw_pieces(board.chess_pieces)
        self.update_board(board.board)
