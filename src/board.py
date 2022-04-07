class Board:
    def __init__(self, file):
        pieces = {}
        f = open(file, 'r')
        self.size = int(f.read(1))
        self.board = [['0' for col in range(self.size)] for row in range(self.size)]
        self.board[0][self.size - 1] = 'f'
        self.board[self.size - 1][0] = 's'
        for line in f:
            char = f.read(1)
            x = int(f.read(1))
            y = int(f.read(1))
            pieces[char] = (x, y)
            self.board[-(y + 1)][x] = char
        self.pieces = pieces
        f.close()

    def add_snake_piece(self, x, y):
        self.board[-(y + 1)][x] = '1'
