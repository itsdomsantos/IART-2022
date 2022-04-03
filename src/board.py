class Board:
    def __init__(self, file):
        pieces = {}
        f = open(file, 'r')
        self.size = int(f.read(1))
        for line in f:
            char = f.read(1)
            x = int(f.read(1))
            y = int(f.read(1))
            pieces[char] = (x, y)
        self.pieces = pieces
        f.close()
