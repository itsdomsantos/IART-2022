import time

import board
import display
from snake import Snake
import pygame as pg
import sys


class Menu:
    def __init__(self):
        print("Welcome to Chess Snake Game")

    def main_menu(self):
        print("Select game mode: ")
        print("Computer (c)    Single Player (p)   Exit(x)")
        menuchoice = str(input())
        if menuchoice == "p":
            self.single_player_mode(self)
        elif menuchoice == "c":
            self.ai_mode(self)
        elif menuchoice == "x":
            return
        else:
            print("Invalid Input!")
            self.main_menu(self)

    def single_player_mode(self):
        level = self.level_menu(self)
        snake = Snake()
        game = board.Board("./levels/level" + level + ".txt", snake)

        screen = display.Display(game.size)
        screen.draw_board()
        screen.color_square(0, game.size - 1)
        screen.draw_chess_piece("s", (0, game.size - 1))
        screen.draw_chess_piece("f", (game.size - 1, 0))
        for x in game.chess_pieces:
            screen.draw_chess_piece(x.type, x.position)
        while game.gameIsOn:
            for event in pg.event.get():
                if event.type == pg.QUIT or event.type == pg.K_ESCAPE:
                    sys.exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    print(game.manhattan_distance())
                    for x in game.chess_pieces:
                        print(x.type, x.attacks)
                    mouseX = event.pos[0]  # x
                    mouseY = event.pos[1]  # y
                    clicked_row = int(mouseX // screen.BLOCKSIZE)
                    clicked_col = int(mouseY // screen.BLOCKSIZE)
                    value = game.getInput(clicked_row, clicked_col)
                    if value != "0":
                        game.processInput(value, screen)
                    print(clicked_col, clicked_row)
        pg.display.update()
        if game.checkSum():
            print("All pieces attack an equal number of squares")
        else:
            print("Pieces have a different number of squares attacked")
        for x in game.chess_pieces:
            print(x.type, x.attacks)
        time.sleep(5)
        sys.exit()

    def ai_mode(self):
        print("Sorry this mode is not available at the moment")
        print("Enter 0 to return to main menu")
        menuchoice = str(input())
        while menuchoice != "0":
            print("Invalid Input!")
            print("Enter 0 to return to main menu")
            menuchoice = str(input())
        self.main_menu(self)

    def level_menu(self):
        print("Select number of puzzle: ")
        print("For puzzle with size 5x5 enter a number between 1-10")
        print("For puzzle with size 6x6 enter a number between 11-20")
        menuchoice = str(input())
        while 1 > int(menuchoice) > 20:
            print("Invalid Input!")
            print("For puzzle with size 5x5 enter a number between 1-10")
            print("For puzzle with size 6x6 enter a number between 11-20")
            menuchoice = str(input())
        return menuchoice
