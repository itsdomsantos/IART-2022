import numpy as np
import piece


class Board:
    def __init__(self, file, snake):
        self.gameIsOn = True
        self.chess_pieces = []
        self.openLevel(file)
        self.snake = snake

    def openLevel(self, file):
        f = open(file, 'rb')
        self.size = int(f.read(1))
        self.board = [['0' for col in range(self.size)] for row in range(self.size)]
        self.board[0][self.size - 1] = 'f'
        self.board[self.size - 1][0] = 's'
        self.actualY = self.size - 1
        self.actualX = 0
        lineIndex = 0

        for line in f:
            split = line.split()
            if lineIndex != 0:
                type = split[0].decode("utf-8")
                xPos = int(split[1])
                yPos = int(split[2])
                self.board[yPos][xPos] = type
                self.chess_pieces.append(piece.Pieces(type, xPos, yPos, self.posAttacked(xPos, yPos, type)))
            lineIndex += 1
        self.updateAttacks(0, self.size - 1)
        f.close()

    def processInput(self, value):
        if value == "w":
            if self.snake.horizontal:
                if self.checkDiagonal(self.actualX, self.actualY - 1):
                    self.addSnakePiece(self.actualX, self.actualY - 1)
                    self.snake.horizontal = False
            else:
                self.addSnakePiece(self.actualX, self.actualY - 1)
        elif value == "s":
            if self.snake.horizontal:
                if self.checkDiagonal(self.actualX, self.actualY + 1):
                    self.addSnakePiece(self.actualX, self.actualY + 1)
                    self.snake.horizontal = False
            else:
                self.addSnakePiece(self.actualX, self.actualY + 1)
        elif value == "d":
            if not self.snake.horizontal:
                if self.checkDiagonal(self.actualX + 1, self.actualY):
                    self.addSnakePiece(self.actualX + 1, self.actualY)
                    self.snake.horizontal = True
            else:
                self.addSnakePiece(self.actualX + 1, self.actualY)
        elif value == "a":
            if not self.snake.horizontal:
                if self.checkDiagonal(self.actualX - 1, self.actualY):
                    self.addSnakePiece(self.actualX - 1, self.actualY)
                    self.snake.horizontal = True
            else:
                self.addSnakePiece(self.actualX - 1, self.actualY)
        else:
            print("Invalid Input")

    def addSnakePiece(self, x, y):
        if self.moveAllowed(x, y):
            self.board[y][x] = '1'
            self.actualX = x
            self.actualY = y
            self.updateAttacks(x, y)
        else:
            print(" Move not allowed")

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
            return self.queenAttacks(x, y)
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
        cont = 1
        while cont < self.size:
            aux.append((x + cont, y + cont))
            aux.append((x + cont, y - cont))
            aux.append((x - cont, y + cont))
            aux.append((x - cont, y - cont))
            cont += 1
        return self.checkPos(np.array(aux))

    def rookAttacks(self, x, y):
        aux = []
        cont = 1
        while cont < self.size:
            aux.append((x + cont, y))
            aux.append((x - cont, y))
            aux.append((x, y - cont))
            aux.append((x, y + cont))
            cont += 1
        return self.checkPos(np.array(aux))

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
        for t in aux:
            print(t)

        print("##########################")
        return aux

    def moveAllowed(self, x, y):
        if not self.checkSize(x, y):
            return False
        if self.board[y][x] == 'f':
            print("Path completed")
            self.gameIsOn = False
            return True
        if self.board[y][x] != '0':
            return False

        return True

    def printBoard(self):
        a = np.array(self.board)
        for line in a:
            print('  '.join(map(str, line)))

    def checkDiagonal(self, x, y):
        if self.checkSize(x + 1, y - 1) and self.checkSize(x - 1, y + 1):
            if self.board[y - 1][x + 1] == '1' or self.board[y + 1][x - 1] == '1' or self.checkPiece(x + 1,
                                                                                                     y - 1) or self.checkPiece(
                x - 1, y + 1):
                return True
            else:
                print("Move not allowed")
                return False
        else:
            print("TESTE")
            return True

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

    def checkSum(self):
        temp = []
        for x in self.chess_pieces:
            temp.append(x.attacks)
        return all(element == temp[0] for element in temp)
