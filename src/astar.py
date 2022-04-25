import time

import board
import copy
import state
import sys
from queue import PriorityQueue


class ASTAR:
    """
        A class used to implement a-star algorithm

        ...

        Attributes
        ----------
        game : stores the initial game created
        solution : stores the solution of the level
        visited : stores the visited nodes
        possible_moves : list with all possible moves
        done : bool that indicates if the solution has been found or not
        heuristic : int that allows to select the choosen heuristic
        queue : stores the game states to use in the algorithm

        Methods
        -------
        a_star(self,screen):
            calculates the solution using the a-star algorithm and uses pygame
        a_start_terminal(self):
            calculates the solution using the a-star algorithm and uses terminal to print info
        heuristic_calculation(self, game, type):
            calculates the value used in the priority queue (defines the node to be expanded)
        check_visited(self, board):
            verifies if the node was already visited
        get_state(self, board):
            returns the state of the input board
        add_move(self, x, board):
            adds the x move (up, down, left, right) to the visited states

    """
    def __init__(self, level, heuristic):
        self.game = board.Board("./levels/level" + level + ".txt", True)
        self.solution = self.game.snake.path
        self.visited = []
        temp = copy.deepcopy(self.game.board)
        self.visited.append(state.State(temp))
        self.possible_moves = ["w", "a", "s", "d"]
        self.done = False
        self.heuristic = heuristic
        self.queue = PriorityQueue()
        self.queue.put((self.heuristic_calculation(self.game, self.heuristic), self.game))
        sys.setrecursionlimit(99999999)

    def a_star(self,screen):
        if self.done:
            return

        item = self.queue.get()
        current_state = item[1]
        screen.reset_board(current_state)
        screen.update_board(current_state.board)



        print(current_state.print_board())
        board = copy.deepcopy(current_state.board)

        if not self.check_visited(board):
            self.visited.append(state.State(board))

        if not current_state.gameIsOn and current_state.check_sum():
            print("done")
            self.solution = current_state.snake.path
            self.game = current_state
            self.done = True
            return

        if not current_state.check_available_moves or not current_state.gameIsOn or len(
                self.get_state(board).moves) == 4:
            self.a_star(screen)

        for x in self.possible_moves:
            temp = copy.deepcopy(current_state)
            if self.done:
                return
            if x in self.get_state(board).moves:
                continue
            self.add_move(x, board)
            if temp.process_input(x):
                self.queue.put((self.heuristic_calculation(temp, self.heuristic), temp))
        self.a_star(screen)


    def a_start_terminal(self):
        if self.done:
            return

        item = self.queue.get()
        current_state = item[1]



        print(current_state.print_board())
        board = copy.deepcopy(current_state.board)

        if not self.check_visited(board):
            self.visited.append(state.State(board))

        if not current_state.gameIsOn and current_state.check_sum():
            print("done")
            self.solution = current_state.snake.path
            self.game = current_state
            self.done = True
            return

        if not current_state.check_available_moves or not current_state.gameIsOn or len(
                self.get_state(board).moves) == 4:
            self.a_start_terminal()

        for x in self.possible_moves:
            temp = copy.deepcopy(current_state)
            if self.done:
                return
            if x in self.get_state(board).moves:
                continue
            self.add_move(x, board)
            if temp.process_input(x):
                self.queue.put((self.heuristic_calculation(temp, self.heuristic), temp))
        self.a_start_terminal()



    def heuristic_calculation(self, game, type):
        if type == 1:
            return game.manhattan_distance() + game.cost
        elif type == 2:
            return game.attack_diff() + game.cost
        elif type == 3:
            return game.manhattan_distance() + game.attack_diff() + game.cost

    def check_visited(self, board):
        for i in self.visited:
            if i.board == board:
                return True
        return False

    def get_state(self, board):
        for i in self.visited:
            if i.board == board:
                return i

    def add_move(self, x, board):
        for i in self.visited:
            if i.board == board:
                i.moves.add(x)
