class State:
    """
        A class used to represent a game state for algorithms

        ...

        Attributes
        ----------
        board : matrix representing the game board
        moves : set used to store the moves already used for that board state
    """

    def __init__(self, board):
        self.board = board
        self.moves = set()


