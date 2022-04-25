import time
import board
import display
import pygame as pg
import sys
import dfs
import astar
import greedy

class Menu:
    """
                    A class used to implement graphic interface using pygame

                    ...

                    Attributes
                    ----------
                    pygameOn : indicates if graphic interface is on or not

                    Methods
                    -------
                    main_menu(self):
                        Used to select between graphic or terminal interface and to select either CPU or human user
                    single_player_mode(self):
                       Used to control the flow of the single player mode
                    ai_mode(self):
                       Used to select which algorithm implemented to use
                    select_heuristic(self, alg):
                       Used to select the heuristic for the selected algorithm (alg)
                    a_star_mode(self, heuristic):
                       Used to ruin AI mode using a-star algorithm for the selected heuristic (heuristic)
                    greedy_mode(self, heuristic):
                       Used to ruin AI mode using greedy algorithm for the selected heuristic (heuristic)
                    dfs_mode(self, heuristic):
                       Used to ruin AI mode using dfs algorithm
                    level_menu(self):
                       Used to select the puzzle (20 levels)


    """
    def __init__(self):
        self.pygameOn = False;
        sys.setrecursionlimit(100000)
        print("Welcome to Chess Snake Game")

    def main_menu(self):
        print("Select screening mode: ")
        print("Terminal  (t)   Pygame  (s)")
        screening = str(input())
        print("Select game mode: ")
        print("Computer (c)    Single Player (p)   Exit(x)")
        menuchoice = str(input())
        if screening == "t":
            self.pygameOn = False
        elif screening == "s":
            self.pygameOn = True
        else:
            print("Invalid Input!")
            self.main_menu(self)
            return
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

        if self.pygameOn:
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
                        value = game.get_input(clicked_row, clicked_col)
                        if value != "0":
                            game.process_input(value)
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
                                game.undo_last_movement()
                        elif event.key == pg.K_ESCAPE:
                            sys.exit()

            screen.update_board(game.board)
            screen.draw_chess_piece("f", (game.size - 1, 0))
            pg.display.update()
            if game.check_sum():
                print("All pieces attack an equal number of squares")
            else:
                print("Pieces have a different number of squares attacked")
            time.sleep(5)
            sys.exit()

        elif not self.pygameOn:
            while game.gameIsOn:
                game.display_game_info()

                print(game.print_board())

                print("Move Up (w)    Move Down (s)   Move Left  (a)    Move Right   (d)")
                value = str(input())
                game.process_input(value);
            if game.check_sum():
                print("All pieces attack an equal number of squares")
            else:
                print("Pieces have a different number of squares attacked")
            time.sleep(5)


    def ai_mode(self):
        print("Select algorithm: ")
        print("DFS (0)    A-Star (1)    Greedy (2)")
        menuchoice = str(input())
        if menuchoice == "0":
            self.dfs_mode(self)
            return
        elif menuchoice == "1":
            self.select_heuristic(self, 1)
            return
        elif menuchoice == "2":
            self.select_heuristic(self, 2)
            return
        else:
            print("Invalid Input!")
            self.main_menu(self)
            return

    def select_heuristic(self, alg):
        print("Select heuristic: ")
        print("Heuristic 1 (0)   Heuristic 2 (1)    Heuristic 3 (2)")
        menuchoice = str(input())
        if alg == 1:
            if menuchoice == "0":
                self.a_star_mode(self, 1);
            elif menuchoice == "1":
                self.a_star_mode(self, 2);
            elif menuchoice == "2":
                self.a_star_mode(self, 3);
            else:
                print("Invalid Input!")
                self.main_menu(self)
                return
        elif alg == 2:
            if menuchoice == "0":
                self.greedy_mode(self, 1);
            elif menuchoice == "1":
                self.greedy_mode(self, 2);
            elif menuchoice == "2":
                self.greedy_mode(self, 3);
            else:
                print("Invalid Input!")
                self.main_menu(self)
                return


    def a_star_mode(self, heuristic):
        level = self.level_menu(self)
        algorithm = astar.ASTAR(level, heuristic)

        if self.pygameOn:
            screen = display.Display(algorithm.game.size)
            screen.init_board()
            screen.update_board(algorithm.game.board)
            screen.draw_borders()
            screen.draw_pieces(algorithm.game.chess_pieces)
            screen.update_board(algorithm.game.board)
            algorithm.a_star(screen)
            screen.update_board(algorithm.game.board)
            time.sleep(10)

        if not self.pygameOn:
            algorithm.a_start_terminal()

    def greedy_mode(self, heuristic):
        level = self.level_menu(self)
        algorithm = greedy.Greedy(level, heuristic)

        if self.pygameOn:
            screen = display.Display(algorithm.game.size)
            screen.init_board()
            screen.update_board(algorithm.game.board)
            screen.draw_borders()
            screen.draw_pieces(algorithm.game.chess_pieces)
            screen.update_board(algorithm.game.board)
            algorithm.greedy(screen)
            screen.update_board(algorithm.game.board)
            time.sleep(10)

        if not self.pygameOn:
            algorithm.greedy_terminal()


    def dfs_mode(self):
        level = self.level_menu(self)
        algorithm = dfs.DFS(level)
        if self.pygameOn:
            screen = display.Display(algorithm.game.size)
            screen.init_board()
            screen.update_board(algorithm.game.board)
            screen.draw_borders()
            screen.draw_pieces(algorithm.game.chess_pieces)
            screen.update_board(algorithm.game.board)
            algorithm.dfs(screen)
            screen.update_board(algorithm.game.board)
            time.sleep(10)
        elif not self.pygameOn:
            algorithm.dfs_terminal()
            time.sleep(10)


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
