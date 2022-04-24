import board
import copy
import state
import sys


class DFS:
    """
            A class used to implement the dfs algorithm

            ...

            Attributes
            ----------
            game : stores the initial game created
            solution : stores the solution of the level
            visited : stores the visited nodes
            possible_moves : list with all possible moves
            done : bool that indicates if the solution has been found or not

            Methods
            -------
            dfs(self,screen):
                calculates the solution using the dfs algorithm and uses pygame
            dfs_terminal(self):
                calculates the solution using the dfs algorithm and uses terminal to print info
            check_visited(self, board):
                verifies if the node was already visited
            get_state(self, board):
                returns the state of the input board
            add_move(self, x, board):
                adds the x move (up, down, left, right) to the visited states

    """
    def __init__(self, level):
        self.game = board.Board("./levels/level" + level + ".txt", True)
        self.solution = self.game.snake.path
        self.visited = []
        temp = copy.deepcopy(self.game.board)
        self.visited.append(state.State(temp))
        self.possible_moves = ["w", "a", "s", "d"]
        self.done = False
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

    def dfs_terminal(self):  # function for dfs on terminal
        if self.done:
            return
        temp = copy.deepcopy(self.game.board)
        if not self.check_visited(temp):
            self.visited.append(state.State(temp))

        if not self.game.gameIsOn and self.game.checkSum():
            print("done")
            self.done = True
            return

        if not self.game.checkAvailableMoves() or not self.game.gameIsOn or len(
                self.get_state(self.game.board).moves) == 4:
            self.game.undoLastMovement()
            self.game.board[0][self.game.size - 1] = 'f'
            self.game.gameIsOn = True
            self.dfs_terminal()

        for x in self.possible_moves:
            if self.done:
                return
            if x in self.get_state(self.game.board).moves:
                continue
            self.add_move(x, self.game.board)
            if self.game.processInput(x):
                if self.check_visited(self.game.board) and x not in self.get_state(self.game.board).moves:
                    self.game.undoLastMovement()
                    self.game.undoLastMovement()
                    self.game.board[0][self.game.size - 1] = 'f'
                self.dfs_terminal()
            if len(self.get_state(self.game.board).moves) == 4:
                self.dfs_terminal()

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
