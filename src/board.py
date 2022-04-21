import numpy as np
import piece
import snake


class Board:
    def __init__(self, file, ai):
        self.gameIsOn = True
        self.chess_pieces = []
        self.sol = []
        self.snake = snake.Snake()
        self.openLevel(file)
        self.cost = 0
        self.ai = ai

    def openLevel(self, file):
        f = open(file, 'rb')
        self.size = int(f.read(1))
        self.board = [['0' for col in range(self.size)] for row in range(self.size)]
        self.board[0][self.size - 1] = 'f'
        self.board[self.size - 1][0] = 's'
        self.actualY = self.size - 1
        self.actualX = 0
        self.snake.update_path((self.actualX, self.actualY))
        lineIndex = 0

        for line in f:
            split = line.split()
            if lineIndex != 0:
                if split[0].decode("utf-8") == "sol":
                    break
                type = split[0].decode("utf-8")
                xPos = int(split[1])
                yPos = int(split[2])
                self.board[yPos][xPos] = type
                self.chess_pieces.append(piece.Pieces(type, xPos, yPos))
            lineIndex += 1
        for line in f:
            split = line.split()
            if lineIndex != 0:
                xPos = int(split[0])
                yPos = int(split[1])
                self.sol.append((xPos, yPos))
            lineIndex += 1
        for x in self.chess_pieces:
            x.define_attacks(self.posAttacked(x.position[0], x.position[1], x.type))
        self.updateAttacks(0, self.size - 1)
        f.close()

    def processInput(self, value):
        if not self.validInput(value):
            return False
        else:
            self.cost += 1
            return True

    def addSnakePiece(self, x, y):
        if self.moveAllowed(x, y):
            if self.board[y][x] == "f":
                self.gameIsOn = False
            self.board[y][x] = '1'
            self.actualX = x
            self.actualY = y
            self.updateAttacks(x, y)
            self.snake.update_path((x, y))
            if not self.checkAvailableMoves() and self.gameIsOn:
                if not self.ai:
                    self.resetGame()
            return True
        else:
            return False

    def posAttacked(self, x, y, char):
        if char == 'p':
            return self.checkPos(self.pawnAttacks(x, y))
        elif char == 'n':
            return self.checkPos(self.knightAttacks(x, y))
        elif char == 'b':
            return self.checkPos(self.bishopAttacks(x, y))
        elif char == 'r':
            return self.checkPos(self.rookAttacks(x, y))
        elif char == 'q':
            return self.checkPos(self.queenAttacks(x, y))
        elif char == 'k':
            return self.checkPos(self.kingAttacks(x, y))

    def pawnAttacks(self, x, y):
        return np.array([(x - 1, y - 1), (x + 1, y - 1)])

    def knightAttacks(self, x, y):
        aux = [(x - 1, y + 2),
               (x + 1, y + 2),
               (x - 1, y - 2),
               (x + 1, y - 2),
               (x - 2, y + 1),
               (x - 2, y - 1),
               (x + 2, y + 1),
               (x + 2, y - 1)]
        return np.array(aux)

    def bishopAttacks(self, x, y):
        aux = []
        tr_flag = 1
        tl_flag = 1
        br_flag = 1
        bl_flag = 1
        cont = 1
        while cont < self.size:
            if br_flag:
                aux.append((x + cont, y + cont))
                for cp in self.chess_pieces:
                    if cp.position == (x + cont, y + cont):
                        br_flag = 0
                        break
            if tr_flag:
                aux.append((x + cont, y - cont))
                for cp in self.chess_pieces:
                    if cp.position == (x + cont, y - cont):
                        tr_flag = 0
                        break
            if bl_flag:
                aux.append((x - cont, y + cont))
                for cp in self.chess_pieces:
                    if cp.position == (x - cont, y + cont):
                        bl_flag = 0
                        break
            if tl_flag:
                aux.append((x - cont, y - cont))
                for cp in self.chess_pieces:
                    if cp.position == (x - cont, y - cont):
                        tl_flag = 0
                        break
            cont += 1
        return np.array(aux)

    def rookAttacks(self, x, y):
        aux = []
        right_flag = 1
        left_flag = 1
        up_flag = 1
        down_flag = 1
        cont = 1
        while cont < self.size:
            if right_flag:
                aux.append((x + cont, y))
                for cp in self.chess_pieces:
                    if cp.position == (x + cont, y):
                        right_flag = 0
                        break
            if left_flag:
                aux.append((x - cont, y))
                for cp in self.chess_pieces:
                    if cp.position == (x - cont, y):
                        left_flag = 0
                        break
            if up_flag:
                aux.append((x, y - cont))
                for cp in self.chess_pieces:
                    if cp.position == (x, y - cont):
                        up_flag = 0
                        break
            if down_flag:
                aux.append((x, y + cont))
                for cp in self.chess_pieces:
                    if cp.position == (x, y + cont):
                        down_flag = 0
                        break
            cont += 1
        return np.array(aux)

    def queenAttacks(self, x, y):
        return np.concatenate((self.rookAttacks(x, y), self.bishopAttacks(x, y)), axis=0)

    def kingAttacks(self, x, y):
        return np.array([(x + 1, y),
                         (x - 1, y),
                         (x, y + 1),
                         (x, y - 1),
                         (x + 1, y + 1),
                         (x + 1, y - 1),
                         (x - 1, y + 1),
                         (x - 1, y - 1)])

    def checkPos(self, array):
        aux = []
        for x in array:
            if self.size > x[0] >= 0 and self.size > x[1] >= 0:
                aux.append(x)
        return aux

    def validInput(self, value):
        if value == "w":
            if self.checkTouchesUp():
                return self.addSnakePiece(self.actualX, self.actualY - 1)
        elif value == "s":
            if self.checkTouchesDown():
                return self.addSnakePiece(self.actualX, self.actualY + 1)
        elif value == "d":
            if self.checkTouchesRight():
                return self.addSnakePiece(self.actualX + 1, self.actualY)
        elif value == "a":
            if self.checkTouchesLeft():
                return self.addSnakePiece(self.actualX - 1, self.actualY)
        else:
            return False

    def moveAllowed(self, x, y):
        if not self.checkSize(x, y):
            return False
        if self.board[y][x] == 'f':
            return True
        if self.board[y][x] != '0':
            return False
        return True

    def printBoard(self):
        a = np.array(self.board)
        for line in a:
            print('  '.join(map(str, line)))

    def checkSize(self, x, y):
        if self.size - 1 >= x >= 0 and self.size - 1 >= y >= 0:
            return True
        return False

    def checkPiece(self, x, y):
        if self.board[y][x] == 'p' or self.board[y][x] == 'n' or self.board[y][x] == 'b' or self.board[y][x] == 'r' or \
                self.board[y][x] == 'q' or self.board[y][x] == 'k':
            return True

        return False

    def updateAttacks(self, x, y):
        for cp in self.chess_pieces:
            for pos in cp.positions_attacked:
                if np.array_equal(np.array([x, y]), pos):
                    cp.attacks += 1

    def deleteAttacks(self, x, y):
        for cp in self.chess_pieces:
            for pos in cp.positions_attacked:
                if np.array_equal(np.array([x, y]), pos):
                    cp.attacks -= 1

    def checkSum(self):
        temp = []
        for x in self.chess_pieces:
            temp.append(x.attacks)
        return all(element == temp[0] for element in temp)

    def manhattan_distance(self):
        return abs((self.size - 1) - self.actualX) + abs(0 - self.actualY)

    def getInput(self, x, y):
        if x == self.actualX - 1 and y == self.actualY:
            return "a"
        elif x == self.actualX + 1 and y == self.actualY:
            return "d"
        elif x == self.actualX and y == self.actualY - 1:
            return "w"
        elif x == self.actualX and y == self.actualY + 1:
            return "s"
        else:
            return "0"

    def undoLastMovement(self):
        self.deleteAttacks(self.actualX, self.actualY)
        self.board[self.actualY][self.actualX] = "0"
        self.snake.undo_last_movement()
        self.actualX = self.snake.path[-1][0]
        self.actualY = self.snake.path[-1][1]

    def checkTouchesUp(self):
        points = []
        points.append((self.actualX - 1, self.actualY - 1))
        points.append((self.actualX - 1, self.actualY - 2))
        points.append((self.actualX, self.actualY - 2))
        points.append((self.actualX + 1, self.actualY - 2))
        points.append((self.actualX + 1, self.actualY - 1))
        flag = 0

        for p in points:
            if self.checkSize(p[0], p[1]):
                flag = 1
                if self.board[p[1]][p[0]] == "1" or self.board[p[1]][p[0]] == "s":
                    return False
        if flag == 1:
            return True

    def checkTouchesDown(self):
        points = []
        points.append((self.actualX - 1, self.actualY + 1))
        points.append((self.actualX - 1, self.actualY + 2))
        points.append((self.actualX, self.actualY + 2))
        points.append((self.actualX + 1, self.actualY + 2))
        points.append((self.actualX + 1, self.actualY + 1))
        flag = 0

        for p in points:
            if self.checkSize(p[0], p[1]):
                flag = 1
                if self.board[p[1]][p[0]] == "1" or self.board[p[1]][p[0]] == "s":
                    return False
        if flag == 1:
            return True

    def checkTouchesRight(self):
        points = []
        points.append((self.actualX + 1, self.actualY - 1))
        points.append((self.actualX + 2, self.actualY - 1))
        points.append((self.actualX + 2, self.actualY))
        points.append((self.actualX + 2, self.actualY + 1))
        points.append((self.actualX + 1, self.actualY + 1))
        flag = 0
        for p in points:
            if self.checkSize(p[0], p[1]):
                flag = 1
                if self.board[p[1]][p[0]] == "1" or self.board[p[1]][p[0]] == "s":
                    return False
        if flag == 1:
            return True

    def checkTouchesLeft(self):
        points = []
        points.append((self.actualX - 1, self.actualY - 1))
        points.append((self.actualX - 2, self.actualY - 1))
        points.append((self.actualX - 2, self.actualY))
        points.append((self.actualX - 2, self.actualY + 1))
        points.append((self.actualX - 1, self.actualY + 1))
        flag = 0

        for p in points:
            if self.checkSize(p[0], p[1]):
                flag = 1
                if self.board[p[1]][p[0]] == "1" or self.board[p[1]][p[0]] == "s":
                    return False
        if flag == 1:
            return True

    def checkAvailableMoves(self):
        if self.checkTouchesLeft() and self.moveAllowed(self.actualX - 1, self.actualY):
            return True
        elif self.checkTouchesRight() and self.moveAllowed(self.actualX + 1, self.actualY):
            return True
        elif self.checkTouchesUp() and self.moveAllowed(self.actualX, self.actualY - 1):
            return True
        elif self.checkTouchesDown() and self.moveAllowed(self.actualX, self.actualY + 1):
            return True
        else:
            return False

    def resetGame(self):
        self.snake.restart_snake()
        for y in range(0, self.size):
            for x in range(0, self.size):
                if self.board[y][x] == "1":
                    self.board[y][x] = "0"

        self.cost = -1
        self.actualX = 0
        self.actualY = self.size - 1
        for cp in self.chess_pieces:
            cp.attacks = 0

    def hint(self):
        for i in range(0, len(self.sol)):
            if self.sol[i] == (self.actualX, self.actualY):
                return self.sol[i + 1]
        return -1

    def display_game_info(self):
        for x in self.chess_pieces:
            print(x.type, ":", x.attacks)
        print("============")