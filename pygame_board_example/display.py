import pygame as pg


class Display:

    def __init__(self, size):
        self.width = size * 100
        self.heigth = size * 100
        self.WHITE = (240, 240, 240)
        self.BLACK = (0, 0, 0)
        self.BLOCKSIZE = 100


def draw_board(self):
    pg.init()
    screen = pg.display.set_mode((self.width, self.heigth))
    screen.fill(self.WHITE)
    for x in range(0, self.width, self.BLOCKSIZE):
        for y in range(0, self.heigth, self.BLOCKSIZE):
            rect = pg.Rect(x, y, self.BLOCKSIZE, self.BLOCKSIZE)
            pg.draw.rect(screen, self.BLACK, rect, 1)
    pg.display.update()

