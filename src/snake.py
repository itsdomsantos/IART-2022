class Snake:
    def __init__(self):
        self.path = []
        self.counters = {}
        self.prevMov = '0'

    def update_path(self, position):
        self.path.append(position)

    def undo_last_movement(self):
            self.path.pop(-1)
            self.getPrevMov()

    def getPrevMov(self):
        if len(self.path) == 1:
            self.prevMov = '0'
        elif self.path[-1][0] == self.path[-2][0] + 1 and self.path[-1][1] == self.path[-2][1]:
            self.prevMov = 'd'
        elif self.path[-1][0] == self.path[-2][0] - 1 and self.path[-1][1] == self.path[-2][1]:
            self.prevMov = 'a'
        elif self.path[-1][0] == self.path[-2][0] and self.path[-1][1] == self.path[-2][1] + 1:
            self.prevMov = 's'
        elif self.path[-1][0] == self.path[-2][0] and self.path[-1][1] == self.path[-2][1] - 1:
            self.prevMov = 'w'
