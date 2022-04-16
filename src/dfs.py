# '''
import board
import copy


class DFS:
    def __init__(self, level):
        self.game = board.Board("./levels/level" + level + ".txt", True)
        self.solution = self.game.snake.path
        self.visited = []
        temp = copy.deepcopy(self.game.board)
        self.visited.append(temp)
        self.possible_moves = ["w", "a", "s", "d"]
        self.index = 0

    def dfs(self, board):  # function for dfs
        print(self.game.printBoard())


        temp = copy.deepcopy(self.game.board)
        if not self.check_visited(temp):
            self.visited.append(temp)

        if not self.game.gameIsOn and self.game.checkSum():
            print("done")
            return
        else:
            self.game.gameIsOn = True

        if not self.game.checkAvailableMoves() or not self.game.gameIsOn:
            self.game.undoLastMovement()
            self.game.board[0][self.game.size - 1] = 'f'
            temp = copy.deepcopy(self.game.board)
            self.dfs(temp)


        for x in self.possible_moves:
            if self.game.processInput(x):
                if self.check_visited(self.game.board):
                    self.game.undoLastMovement()
                    self.game.undoLastMovement()
                    self.game.board[0][self.game.size - 1] = 'f'
                    temp = copy.deepcopy(self.game.board)
                    self.dfs(temp)
                temp = copy.deepcopy(self.game.board)
                self.dfs(temp)

    def check_visited(self, board):
        for i in self.visited:
            if i == board:
                return True
