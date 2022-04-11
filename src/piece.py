class Pieces:
    def __init__(self, type, x, y):
        self.type = type
        self.position = (x, y)
        self.attacks = 0
        self.positions_attacked=[]

    def add_attack(self):
        self.attacks += 1

    def define_attacks(self, positions_attacked):
        self.positions_attacked = positions_attacked
