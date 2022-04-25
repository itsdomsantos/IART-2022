import numpy as np
import piece
import snake


class Board:
    """
                      A class used to implement the game logic and its status

                      ...

                      Attributes
                      ----------
                      gameIsOn : bool used to verify if the final tile was added to the path
                      chess_pieces : chess pieces that are in the board
                      sol : stores the game solution
                      snake : snake object (path)
                      cost : cost(distance) of the path
                      ai : indicates whether or not the AI mode is on
                      heuristic : variable used to store the heurisitic used (default 0)
                      actualX : current column
                      actualY : current row

                      Methods
                      -------
                      open_level(self, file):
                          Used to read the puzzle file and start variables such as board, chess_pieces, current coordinate
                      process_input(self):
                         returns true or false depending on the move played, if it is valid or not
                      add_snake_piece(self, x, y):
                         Used to add a new snake piece to the path and update the board attributes
                      pos_attacked(self, x, y, char):
                         Used to update chess pieces variable 'positions_attacked'
                      pawn_attacks(self, x, y):
                         Used to calculate the attacks of the pieces which type is pawn
                      knight_attacks(self, x, y):
                         Used to calculate the attacks of the pieces which type is knight
                      bishop_attacks(self, x, y):
                         Used to calculate the attacks of the pieces which type is bishop
                      rook_attacks(self, x, y):
                         Used to calculate the attacks of the pieces which type is rook
                      queen_attacks(self, x, y):
                         Used to calculate the attacks of the pieces which type is queen
                      king_attacks(self, x, y):
                         Used to calculate the attacks of the pieces which type is king
                      check_pos(self, array):
                         Used to check if the positions attack of a chess piece belong to the size interval
                      valid_input(self, value):
                         Returns the bool corresponding if the move entered is allowed or not (verifies collisions)
                      move_allowed(self, x, y):
                         Returns the bool corresponding if the move entered is allowed or not (verifies if the move is
                      within the board limits and if the tile to be added to the path is not occupied by another object)

                      print_board(self):
                         Displays the board in terminal ia a human friendly way
                      check_size(self, x, y):
                         Returns true if the coordinate (x,y) is within the limits of the board
                      check_piece(self, x, y):
                         Returns true if in the coordinate (x,y) there is a chess piece of any type
                      update_attacks(self, x, y):
                         After a move is perform this function is called to update the attacks in the snake
                      delete_attacks(self, x, y):
                         After an undo of a movement this function is called to update the attacks in the snake
                      check_sum(self):
                         Returns true if all chess piecs attack an equal numbers of snake pieces
                      manhattan_distance(self):
                         Calculates the manhatan distance of the current position to the end tile
                      attack_diff(self):
                         Calculates the difference between the piece which performs the most attacks with the one which
                      has the less number of attacks

                      get_input(self, x, y):
                         Used to 'translate' a coordinate choose with mouse in pygame to the respective char
                      undo_last_movement(self):
                         Used to undo the last movement and update the board attributes
                      check_touches_up(self):
                         Verifies if the entered move will cause a collision between snake pieces
                      check_touches_down(self):
                         Verifies if the entered move will cause a collision between snake pieces
                      check_touches_left(self):
                         Verifies if the entered move will cause a collision between snake pieces
                      check_touches_right(self):
                         Verifies if the entered move will cause a collision between snake pieces
                      check_available_moves(self):
                         Returns true if in the current position there is an available an valid move otherwise returns false
                      reset_game(self):
                         Initializes all the game attributes
                      hint(self):
                         Returns an hint for the player if available otherwise returns -1
                      display_game_info(self):
                         Displays in the terminal the current game status such as attacks performed by each chess piece
                      __lt__(self, other):
                         Used to order the board objects according to the heuristic chose





    """

    def __init__(self, file, ai, heuristic=0):
        self.actualX = None
        self.actualY = None
        self.gameIsOn = True
        self.chess_pieces = []
        self.sol = []
        self.snake = snake.Snake()
        self.open_level(file)
        self.cost = 0
        self.ai = ai
        self.heuristic = heuristic

    def open_level(self, file):
        f = open(file, 'rb')
        self.size = int(f.read(1))
        self.board = [['0' for col in range(self.size)] for row in range(self.size)]
        self.board[0][self.size - 1] = 'f'
        self.board[self.size - 1][0] = 's'
        self.actualY = self.size - 1
        self.actualX = 0
        self.snake.update_path((self.actualX, self.actualY))
        lineIndex = 0

        for line in f:
            split = line.split()
            if lineIndex != 0:
                if split[0].decode("utf-8") == "sol":
                    break
                type = split[0].decode("utf-8")
                xPos = int(split[1])
                yPos = int(split[2])
                self.board[yPos][xPos] = type
                self.chess_pieces.append(piece.Pieces(type, xPos, yPos))
            lineIndex += 1
        for line in f:
            split = line.split()
            if lineIndex != 0:
                xPos = int(split[0])
                yPos = int(split[1])
                self.sol.append((xPos, yPos))
            lineIndex += 1
        for x in self.chess_pieces:
            x.define_attacks(self.pos_attacked(x.position[0], x.position[1], x.type))
        self.update_attacks(0, self.size - 1)
        f.close()

    def process_input(self, value):
        if not self.valid_input(value):
            return False
        else:
            self.cost += 1
            return True

    def add_snake_piece(self, x, y):
        if self.move_allowed(x, y):
            if self.board[y][x] == "f":
                self.gameIsOn = False
            self.board[y][x] = '1'
            self.actualX = x
            self.actualY = y
            self.update_attacks(x, y)
            self.snake.update_path((x, y))
            if not self.check_available_moves() and self.gameIsOn:
                if not self.ai:
                    self.reset_game()
            return True
        else:
            return False

    def pos_attacked(self, x, y, char):
        if char == 'p':
            return self.check_pos(self.pawn_attacks(x, y))
        elif char == 'n':
            return self.check_pos(self.knight_attacks(x, y))
        elif char == 'b':
            return self.check_pos(self.bishop_attacks(x, y))
        elif char == 'r':
            return self.check_pos(self.rook_attacks(x, y))
        elif char == 'q':
            return self.check_pos(self.queen_attacks(x, y))
        elif char == 'k':
            return self.check_pos(self.king_attacks(x, y))

    def pawn_attacks(self, x, y):
        return np.array([(x - 1, y - 1), (x + 1, y - 1)])

    def knight_attacks(self, x, y):
        aux = [(x - 1, y + 2),
               (x + 1, y + 2),
               (x - 1, y - 2),
               (x + 1, y - 2),
               (x - 2, y + 1),
               (x - 2, y - 1),
               (x + 2, y + 1),
               (x + 2, y - 1)]
        return np.array(aux)

    def bishop_attacks(self, x, y):
        aux = []
        tr_flag = 1
        tl_flag = 1
        br_flag = 1
        bl_flag = 1
        cont = 1
        while cont < self.size:
            if br_flag:
                aux.append((x + cont, y + cont))
                for cp in self.chess_pieces:
                    if cp.position == (x + cont, y + cont):
                        br_flag = 0
                        break
            if tr_flag:
                aux.append((x + cont, y - cont))
                for cp in self.chess_pieces:
                    if cp.position == (x + cont, y - cont):
                        tr_flag = 0
                        break
            if bl_flag:
                aux.append((x - cont, y + cont))
                for cp in self.chess_pieces:
                    if cp.position == (x - cont, y + cont):
                        bl_flag = 0
                        break
            if tl_flag:
                aux.append((x - cont, y - cont))
                for cp in self.chess_pieces:
                    if cp.position == (x - cont, y - cont):
                        tl_flag = 0
                        break
            cont += 1
        return np.array(aux)

    def rook_attacks(self, x, y):
        aux = []
        right_flag = 1
        left_flag = 1
        up_flag = 1
        down_flag = 1
        cont = 1
        while cont < self.size:
            if right_flag:
                aux.append((x + cont, y))
                for cp in self.chess_pieces:
                    if cp.position == (x + cont, y):
                        right_flag = 0
                        break
            if left_flag:
                aux.append((x - cont, y))
                for cp in self.chess_pieces:
                    if cp.position == (x - cont, y):
                        left_flag = 0
                        break
            if up_flag:
                aux.append((x, y - cont))
                for cp in self.chess_pieces:
                    if cp.position == (x, y - cont):
                        up_flag = 0
                        break
            if down_flag:
                aux.append((x, y + cont))
                for cp in self.chess_pieces:
                    if cp.position == (x, y + cont):
                        down_flag = 0
                        break
            cont += 1
        return np.array(aux)

    def queen_attacks(self, x, y):
        return np.concatenate((self.rook_attacks(x, y), self.bishop_attacks(x, y)), axis=0)

    def king_attacks(self, x, y):
        return np.array([(x + 1, y),
                         (x - 1, y),
                         (x, y + 1),
                         (x, y - 1),
                         (x + 1, y + 1),
                         (x + 1, y - 1),
                         (x - 1, y + 1),
                         (x - 1, y - 1)])

    def check_pos(self, array):
        aux = []
        for x in array:
            if self.size > x[0] >= 0 and self.size > x[1] >= 0:
                aux.append(x)
        return aux

    def valid_input(self, value):
        if value == "w":
            if self.check_touches_up():
                return self.add_snake_piece(self.actualX, self.actualY - 1)
        elif value == "s":
            if self.check_touches_down():
                return self.add_snake_piece(self.actualX, self.actualY + 1)
        elif value == "d":
            if self.check_touches_right():
                return self.add_snake_piece(self.actualX + 1, self.actualY)
        elif value == "a":
            if self.check_touches_left():
                return self.add_snake_piece(self.actualX - 1, self.actualY)
        else:
            return False

    def move_allowed(self, x, y):
        if not self.check_size(x, y):
            return False
        if self.board[y][x] == 'f':
            return True
        if self.board[y][x] != '0':
            return False
        return True

    def print_board(self):
        a = np.array(self.board)
        for line in a:
            print('  '.join(map(str, line)))

    def check_size(self, x, y):
        if self.size - 1 >= x >= 0 and self.size - 1 >= y >= 0:
            return True
        return False

    def check_piece(self, x, y):
        if self.board[y][x] == 'p' or self.board[y][x] == 'n' or self.board[y][x] == 'b' or self.board[y][x] == 'r' or \
                self.board[y][x] == 'q' or self.board[y][x] == 'k':
            return True

        return False

    def update_attacks(self, x, y):
        for cp in self.chess_pieces:
            for pos in cp.positions_attacked:
                if np.array_equal(np.array([x, y]), pos):
                    cp.attacks += 1

    def delete_attacks(self, x, y):
        for cp in self.chess_pieces:
            for pos in cp.positions_attacked:
                if np.array_equal(np.array([x, y]), pos):
                    cp.attacks -= 1

    def check_sum(self):
        temp = []
        for x in self.chess_pieces:
            temp.append(x.attacks)
        return all(element == temp[0] for element in temp)

    def manhattan_distance(self):
        return abs((self.size - 1) - self.actualX) + abs(0 - self.actualY)

    def attack_diff(self):
        temp = []
        for cp in self.chess_pieces:
            temp.append(cp.attacks)
        return max(temp) - min(temp)

    def get_input(self, x, y):
        if x == self.actualX - 1 and y == self.actualY:
            return "a"
        elif x == self.actualX + 1 and y == self.actualY:
            return "d"
        elif x == self.actualX and y == self.actualY - 1:
            return "w"
        elif x == self.actualX and y == self.actualY + 1:
            return "s"
        else:
            return "0"

    def undo_last_movement(self):
        self.delete_attacks(self.actualX, self.actualY)
        self.board[self.actualY][self.actualX] = "0"
        self.snake.undo_last_movement()
        self.actualX = self.snake.path[-1][0]
        self.actualY = self.snake.path[-1][1]

    def check_touches_up(self):
        points = []
        points.append((self.actualX - 1, self.actualY - 1))
        points.append((self.actualX - 1, self.actualY - 2))
        points.append((self.actualX, self.actualY - 2))
        points.append((self.actualX + 1, self.actualY - 2))
        points.append((self.actualX + 1, self.actualY - 1))
        flag = 0

        for p in points:
            if self.check_size(p[0], p[1]):
                flag = 1
                if self.board[p[1]][p[0]] == "1" or self.board[p[1]][p[0]] == "s":
                    return False
        if flag == 1:
            return True

    def check_touches_down(self):
        points = []
        points.append((self.actualX - 1, self.actualY + 1))
        points.append((self.actualX - 1, self.actualY + 2))
        points.append((self.actualX, self.actualY + 2))
        points.append((self.actualX + 1, self.actualY + 2))
        points.append((self.actualX + 1, self.actualY + 1))
        flag = 0

        for p in points:
            if self.check_size(p[0], p[1]):
                flag = 1
                if self.board[p[1]][p[0]] == "1" or self.board[p[1]][p[0]] == "s":
                    return False
        if flag == 1:
            return True

    def check_touches_right(self):
        points = []
        points.append((self.actualX + 1, self.actualY - 1))
        points.append((self.actualX + 2, self.actualY - 1))
        points.append((self.actualX + 2, self.actualY))
        points.append((self.actualX + 2, self.actualY + 1))
        points.append((self.actualX + 1, self.actualY + 1))
        flag = 0
        for p in points:
            if self.check_size(p[0], p[1]):
                flag = 1
                if self.board[p[1]][p[0]] == "1" or self.board[p[1]][p[0]] == "s":
                    return False
        if flag == 1:
            return True

    def check_touches_left(self):
        points = []
        points.append((self.actualX - 1, self.actualY - 1))
        points.append((self.actualX - 2, self.actualY - 1))
        points.append((self.actualX - 2, self.actualY))
        points.append((self.actualX - 2, self.actualY + 1))
        points.append((self.actualX - 1, self.actualY + 1))
        flag = 0

        for p in points:
            if self.check_size(p[0], p[1]):
                flag = 1
                if self.board[p[1]][p[0]] == "1" or self.board[p[1]][p[0]] == "s":
                    return False
        if flag == 1:
            return True

    def check_available_moves(self):
        if self.check_touches_left() and self.move_allowed(self.actualX - 1, self.actualY):
            return True
        elif self.check_touches_right() and self.move_allowed(self.actualX + 1, self.actualY):
            return True
        elif self.check_touches_up() and self.move_allowed(self.actualX, self.actualY - 1):
            return True
        elif self.check_touches_down() and self.move_allowed(self.actualX, self.actualY + 1):
            return True
        else:
            return False

    def reset_game(self):
        self.snake.restart_snake()
        for y in range(0, self.size):
            for x in range(0, self.size):
                if self.board[y][x] == "1":
                    self.board[y][x] = "0"

        self.cost = -1
        self.actualX = 0
        self.actualY = self.size - 1
        for cp in self.chess_pieces:
            cp.attacks = 0

    def hint(self):
        for i in range(0, len(self.sol)):
            if self.sol[i] == (self.actualX, self.actualY):
                return self.sol[i + 1]
        return -1

    def display_game_info(self):
        for x in self.chess_pieces:
            print(x.type, ":", x.attacks)
        print("============")

    def __lt__(self, other):
        if self.heuristic == 1:
            return (self.manhattan_distance() + self.cost) < (other.manhattan_distance() + other.cost)
        elif self.heuristic == 2:
            return (self.attack_diff() + self.cost) < (other.attack_diff() + other.cost)
        elif self.heuristic == 3:
            return (self.manhattan_distance() + self.attack_diff() + self.cost) < (
                    other.manhattan_distance() + other.attack_diff() + other.cost)
        else:
            return self.cost < other.cost
