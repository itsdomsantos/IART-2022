import time
import board
import display
import pygame as pg
import sys
import dfs


class Menu:
    def __init__(self):
        sys.setrecursionlimit(100000)
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
        game = board.Board("./levels/level" + level + ".txt", False)
        screen = display.Display(game.size)
        screen.init_board()
        screen.update_board(game.board)
        screen.draw_borders()
        screen.draw_pieces(game.chess_pieces)
        while game.gameIsOn:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    sys.exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    game.display_game_info()
                    mouseX = event.pos[0]  # x
                    mouseY = event.pos[1]  # y
                    clicked_row = int(mouseX // screen.BLOCKSIZE)
                    clicked_col = int(mouseY // screen.BLOCKSIZE)
                    value = game.getInput(clicked_row, clicked_col)
                    if value != "0":
                        game.processInput(value)
                        screen.update_board(game.board)
                        if game.cost == 0:
                            screen.reset_board(game)
                    print(game.attack_diff())
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_h:
                        hint = game.hint()
                        if hint != -1:
                            screen.add_hint(hint[0], hint[1], True)
                        else:
                            screen.add_hint(game.actualX, game.actualY, False)

                    elif event.key == pg.K_u:
                        game.display_game_info()
                        if len(game.snake.path) > 1:
                            screen.delete_square(game.actualX, game.actualY)
                            game.undoLastMovement()
                    elif event.key == pg.K_ESCAPE:
                        sys.exit()

        screen.update_board(game.board)
        screen.draw_chess_piece("f", (game.size - 1, 0))
        pg.display.update()
        if game.checkSum():
            print("All pieces attack an equal number of squares")
        else:
            print("Pieces have a different number of squares attacked")
        time.sleep(5)
        sys.exit()



    def ai_mode(self):
        print("Select algorithm: ")
        print("DFS (0)    A-Star/Heuristic 1 (1)   A-Star/ Heuristic 2 (2) A-Star/Heuristic 3 (3)")
        menuchoice = str(input())
        if menuchoice == "0":
            self.dfs_mode(self)
        elif menuchoice == "1":
            print("Loading")
            self.ai_mode(self)
        elif menuchoice == "2":
            print("Loading")
            self.ai_mode(self)
        elif menuchoice == "3":
            print("Loading")
            self.ai_mode(self)
        else:
            print("Invalid Input!")
            self.main_menu(self)
    def dfs_mode(self):
        level = self.level_menu(self)
        algorithm = dfs.DFS(level)
        screen = display.Display(algorithm.game.size)
        screen.init_board()
        screen.update_board(algorithm.game.board)
        screen.draw_borders()
        screen.draw_pieces(algorithm.game.chess_pieces)
        screen.update_board(algorithm.game.board)
        algorithm.dfs(screen)
        screen.update_board(algorithm.game.board)
        time.sleep(10)

    def level_menu(self):
        print("Select number of puzzle: ")
        print("For puzzle with size 5x5 enter a number between 1-10")
        print("For puzzle with size 6x6 enter a number between 11-20")
        print("For puzzle with size 8x8 enter a number between 21 or 22")
        menuchoice = str(input())
        while 1 > int(menuchoice) > 22:
            print("Invalid Input!")
            print("For puzzle with size 5x5 enter a number between 1-10")
            print("For puzzle with size 6x6 enter a number between 11-20")
            print("For puzzle with size 8x8 enter a number between 21 or 22")
            menuchoice = str(input())
        return menuchoice
