from src.position import Position
import numpy as np


class Board:
    def __init__(self, file):
        self.pieces = {}
        f = open(file, 'r')
        self.size = int(f.read(1))
        self.board = [['0' for col in range(self.size)] for row in range(self.size)]
        self.board[0][self.size - 1] = 'f'
        self.board[self.size - 1][0] = 's'
        for line in f:
            char = f.read(1)
            x = int(f.read(1))
            y = int(f.read(1))
            #self.pieces = self.posAttacked(x, y, char)
            #print(self.pieces[0])
            #self.pieces[-(y + 1), x].append(self.posAttacked(x, y, char))
            self.pieces[x, y] = self.posAttacked(x, y, char)
            ##print(self.pieces) -----> funciona
            self.board[-(y + 1)][x] = char
        f.close()

    def add_snake_piece(self, x, y):
        self.board[-(y + 1)][x] = '1'

    def posAttacked(self, x, y, char):
        if char == 'p':
            return self.checkPos(self.pawnAttacks(x, y))
        elif char == 'k':
            return self.checkPos(self.knightAttacks(x, y))
        elif char == 'b':
            return self.checkPos(self.bishopAttacks(x, y))
        elif char == 'r':
            return self.checkPos(self.rookAttacks(x, y))
        elif char == 'q':
            return self.queenAttacks(x, y)
        elif char == 'K':
            return self.checkPos(self.kingAttacks(x, y))

    def pawnAttacks(self, x, y):
        return np.array([(x-1, y+1), (x+1, y+1)])

    def knightAttacks(self, x, y):
       aux = np.array([(x - 1, y + 2),
                         (x + 1, y + 2),
                         (x - 1, y - 2),
                         (x + 1, y - 2),
                         (x - 2, y + 1),
                         (x - 2, y - 1),
                         (x + 2, y + 1),
                         (x + 2, y - 1)])
       return aux


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
