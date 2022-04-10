import numpy as np

from piece import Piece


class Board:
    def __init__(self, file):
        self.pieces = {}
        f = open(file, 'rb')
        self.size = int(f.read(1))
        self.board = [['0' for col in range(self.size)] for row in range(self.size)]
        self.board[0][self.size - 1] = 'f'
        self.board[self.size - 1][0] = 's'
        self.actualY = self.size - 1;
        self.actualX = 0;
        lineIndex = 0

        for line in f:
            split = line.split()
            if lineIndex != 0:
                type = split[0].decode("utf-8")
                xPos = int(split[1])
                yPos = int(split[2])
                self.board[yPos][xPos] = type
                self.pieces[xPos, yPos] = self.posAttacked(xPos, yPos, type)
            lineIndex += 1
        f.close()

    def processInput(self, value):
        if value == "w":
            self.addSnakePiece(self.actualX, self.actualY-1)
        elif value == "s":
            self.addSnakePiece(self.actualX, self.actualY+1)
        elif value == "d":
            self.addSnakePiece(self.actualX+1, self.actualY)
        elif value == "a":
            self.addSnakePiece(self.actualX-1, self.actualY)
        else:
            print("Invalid Input")

    def addSnakePiece(self, x, y):
        if self.moveAllowed(x, y):
            self.board[y][x] = '1'
            self.actualX=x
            self.actualY=y
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
        if x < 0 or x >= self.size or y < 0 or y >= self.size:
            return False
        if self.board[y][x] == 'f':
            print("Path completed")
            return True
        if self.board[y][x] != '0':
            return False

        return True

    def printBoard(self):
        a = np.array(self.board)
        for line in a:
            print('  '.join(map(str, line)))
