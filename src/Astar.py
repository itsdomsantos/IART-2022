import time

import board
import copy
import state
import sys
from queue import PriorityQueue


class ASTAR:
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

    def a_star(self,screen):  # function for a_star
        if self.done:
            return
        # verificar se está terminado

        # ir buscar o current state (criar função que definida a prioridade 'f = g + h')
        item = self.queue.get()
        current_state = item[1]
        screen.reset_board(current_state)
        screen.update_board(current_state.board)



        print(current_state.printBoard())
        board = copy.deepcopy(current_state.board)
        # adicionar o estado aos visited
        if not self.check_visited(board):
            self.visited.append(state.State(board))

        # se o jogo terminou e as peças atacam de igual maneira terminar
        if not current_state.gameIsOn and current_state.checkSum():
            print("done")
            self.solution = current_state.snake.path
            self.game = current_state
            print(self.solution)
            self.done = True
            return

        # se o current_state não tem moves possiveis volta a chamar o algoritmo
        if not current_state.checkAvailableMoves or not current_state.gameIsOn or len(
                self.get_state(board).moves) == 4:
            self.a_star(screen)

        # se tiver moves possiveis, adiciona cada estado do board a priority queue atualiza os moves no visited
        for x in self.possible_moves:
            temp = copy.deepcopy(current_state)
            if self.done:
                return
            if x in self.get_state(board).moves:
                continue
            self.add_move(x, board)
            if temp.processInput(x):
                self.queue.put((self.heuristic_calculation(temp, self.heuristic), temp))
            print(self.heuristic_calculation(temp, self.heuristic))
        self.a_star(screen)




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
