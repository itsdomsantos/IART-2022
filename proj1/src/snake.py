class Snake:
    """
        A class used to represent the snake/path

        ...

        Attributes
        ----------
        path : list of tuples containing the positions occupied by the snake

        Methods
        -------
        update_path(self, position)
            adds a new tuple to the path
        undo_last_movement(self):
            deletes last coordinate added to the path
        restart_snake(self):
            deletes all the coordinates already entered except the initial tile
    """
    def __init__(self):
        self.path = []

    def update_path(self, position):
        self.path.append(position)

    def undo_last_movement(self):
        self.path.pop(-1)

    def restart_snake(self):
        self.path = [self.path[0]]