class Pieces:
    def __init__(self, type, x, y, positions_attacked):
        self.type = type
        self.position = (x, y)
        self.positions_attacked = positions_attacked
        self.attacks = 0

    def add_attack(self):
        self.attacks += 1
