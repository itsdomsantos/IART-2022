# '''
import board
import copy
import state


class DFS:
    def __init__(self, level):
        self.game = board.Board("./levels/level" + level + ".txt", True)
        self.solution = self.game.snake.path
        self.visited = []
        temp = copy.deepcopy(self.game.board)
        self.visited.append(state.State(temp))
        self.possible_moves = ["w", "a", "s", "d"]
        self.index = 0

    def dfs(self):  # function for dfs
        print(self.game.printBoard())

        temp = copy.deepcopy(self.game.board)
        if not self.check_visited(temp):
            self.visited.append(state.State(temp))

        if not self.game.gameIsOn and self.game.checkSum():
            print("done")
            return
        else:
            self.game.gameIsOn = True

        if not self.game.checkAvailableMoves() or not self.game.gameIsOn or len(self.get_state(self.game.board).moves) == 4:
            self.game.undoLastMovement()
            self.game.board[0][self.game.size - 1] = 'f'
            self.dfs()


        for x in self.possible_moves:
            if x in self.get_state(self.game.board).moves:
                continue
            self.add_move(x, self.game.board)
            if self.game.processInput(x):
                if self.check_visited(self.game.board):
                    self.game.undoLastMovement()
                    self.game.undoLastMovement()
                    self.game.board[0][self.game.size - 1] = 'f'
                self.dfs()
            if len(self.get_state(self.game.board).moves) == 4:
                self.dfs()

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
