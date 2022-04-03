
class Position:
    def __init__(self, posX, posY, boardSize, attacked = False):
        if posX <= boardSize and posX >= 0 and posY <= boardSize and posY >= 0:
            self.x = posX
            self.y = posY
            self.attacked = attacked

    