# '''
import time
import display
import board
import copy
import state
import sys


class DFS:
    def __init__(self, level):
        self.game = board.Board("./levels/level" + level + ".txt", True)
        self.solution = self.game.snake.path
        self.visited = []
        temp = copy.deepcopy(self.game.board)
        self.visited.append(state.State(temp))
        self.possible_moves = ["w", "a", "s", "d"]
        self.done = False
        self.counter = 0
        sys.setrecursionlimit(99999999)

    def dfs(self,screen):  # function for dfs
        screen.update_board(self.game.board)
        if self.done:
            return
        print(self.game.printBoard())

        temp = copy.deepcopy(self.game.board)
        if not self.check_visited(temp):
            self.visited.append(state.State(temp))

        if not self.game.gameIsOn and self.game.checkSum():
            print("done")
            self.done = True
            return

        if not self.game.checkAvailableMoves() or not self.game.gameIsOn or len(
                self.get_state(self.game.board).moves) == 4:
            screen.delete_square(self.game.actualX, self.game.actualY)
            self.game.undoLastMovement()
            self.game.board[0][self.game.size - 1] = 'f'
            self.game.gameIsOn = True
            self.dfs(screen)

        for x in self.possible_moves:
            if self.done:
                return
            if x in self.get_state(self.game.board).moves:
                continue
            self.add_move(x, self.game.board)
            if self.game.processInput(x):
                if self.check_visited(self.game.board) and x not in self.get_state(self.game.board).moves:
                    screen.delete_square(self.game.actualX, self.game.actualY)
                    self.game.undoLastMovement()
                    screen.delete_square(self.game.actualX, self.game.actualY)
                    self.game.undoLastMovement()
                    self.game.board[0][self.game.size - 1] = 'f'
                self.dfs(screen)
            if len(self.get_state(self.game.board).moves) == 4:
                self.dfs(screen)

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
