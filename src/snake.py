class Snake:
    def __init__(self):
        self.path = []
        self.counters = {}

    def update_path(self, position):
        self.path.append(position)

    def undo_last_movement(self):
            self.path.pop(-1)

    def restart_snake(self):
        self.path=[self.path[0]]