import board
import copy
import state
import sys
from queue import PriorityQueue

class ASTAR:
    def __init__(self, level, heuristic):
        self.game = board.Board("./levels/level" + level + ".txt", True)
        self.solution = self.game.snake.path
        self.open = set([])
        self.close = set([])
        self.possible_moves = ["w", "a", "s", "d"]
        self.done = False
        self.counter = 0
        self.heuristic = heuristic
        self.queue = PriorityQueue()
        sys.setrecursionlimit(99999999)

    def Astar(self, start_node, stop_node, screen):

        ###add starting state to list
        self.open.add(state.State(copy.deepcopy(self.game.board)))

        screen.update_board(self.game.board)
        if self.done:
            return
        print(self.game.printBoard())

        if not self.game.gameIsOn and self.game.checkSum():
            print("done")
            self.done = True
            return

        while len(self.open) > 0:
            n = None

            for v in self.open:
                if n == None or self.game.cost + self.game.attack_diff():
                    n = v

            if n == None:
                print("Path does not exist")
                return None

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