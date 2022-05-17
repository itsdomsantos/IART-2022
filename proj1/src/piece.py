class Pieces:
    """
        A class used to represent the chess piece

        ...

        Attributes
        ----------
        type : variable used to identify the type of chess piece
        position : stores the position of the piece
        attacks : counts the number of attacks of the piece
        positions_attacked : stores the list of coordinates where the piece can attack

        Methods
        -------
        update_path(self, position)
            adds a new tuple to the path
        undo_last_movement(self):
            deletes last coordinate added to the path
        restart_snake(self):
            deletes all the coordinates already entered except the initial tile
    """
    def __init__(self, type, x, y):
        self.type = type
        self.position = (x, y)
        self.attacks = 0
        self.positions_attacked=[]

    def add_attack(self):
        self.attacks += 1

    def define_attacks(self, positions_attacked):
        self.positions_attacked = positions_attacked
