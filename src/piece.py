import numpy as np
from position import *

class Piece:
    def __init__(self, type, position, img):
        self.type = type
        self.position = position
        self.img = img
    
    def posAttacked(self, boardSize):
        if self.type == 'p':
            return self.pawnAttacks(boardSize)
        elif self.type == 'k':
            return self.knightAttacks(boardSize)
        elif self.type == 'b':
            return self.bishopAttacks(boardSize)
        elif self.type == 'r':
            return self.rookAttacks(boardSize)
        elif self.type == 'q':
            return self.queenAttacks(boardSize)
        elif self.type == 'K':
            return self.kingAttacks(boardSize)


    def knightAttacks(self, boardSize):
        return np.array([Position(self.position.x-1, self.position.y+2, boardSize,True), Position(self.position.x+1, self.position.y+2,boardSize ,True), 
        Position(self.position.x-1, self.position.y-2,boardSize ,True),Position(self.position.x+1, self.position.y-2,boardSize ,True), Position(self.position.x-2, self.position.y+1,boardSize ,True),
        Position(self.position.x-2, self.position.y-1, boardSize,True), Position(self.position.x+2, self.position.y-1,boardSize ,True), Position(self.position.x+2, self.position.y-1,boardSize ,True)])

    def bishopAttacks(self, boardSize):
        aux = np.array([])
        while(boardSize >= 0):
            np.insert(aux, Position(self.position.x+1, self.position.y+1, boardSize, True))
            np.insert(aux, Position(self.position.x-1, self.position.y+1, boardSize, True))
            np.insert(aux, Position(self.position.x+1, self.position.y-1, boardSize, True))
            np.insert(aux, Position(self.position.x-1, self.position.y+1, boardSize, True))
            boardSize -=1
        return aux

    def rookAttacks(self, boardSize):
        aux = np.array([])
        while(boardSize >= 0):
            np.insert(aux, Position(self.position.x+1, self.position.y, boardSize, True))
            np.insert(aux, Position(self.position.x-1, self.position.y, boardSize, True))
            np.insert(aux, Position(self.position.x, self.position.y-1, boardSize, True))
            np.insert(aux, Position(self.position.x, self.position.y+1, boardSize, True))
            boardSize -=1
        return aux

    def queenAttacks(self, boardSize):
        return np.concatenate((self.rookAttacks(self,boardSize), self.bishopAttacks(self,boardSize)), axis=0)

    def kingAttacks(self, boardSize):
        return np.array([Position(self.position.x+1, self.position.y, boardSize, True), Position(self.position.x-1, self.position.y, boardSize, True), Position(self.position.x, self.position.y+1, boardSize, True),
        Position(self.position.x, self.position.y-1, boardSize, True), Position(self.position.x+1, self.position.y+1, boardSize, True), Position(self.position.x+1, self.position.y-1, boardSize, True),
        Position(self.position.x-1, self.position.y+1, boardSize, True), Position(self.position.x-1, self.position.y-1, boardSize, True)])
    
    

    