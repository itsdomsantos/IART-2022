import board
from snake import Snake


class Menu:
    def __init__(self):
        print("Welcome to Chess Snake Game")

    def main_menu(self):
        print("Select game mode: ")
        print("Computer (c)    Single Player (p)   Exit(x)")
        menuchoice = str(input())
        if menuchoice == "p":
            self.single_player_mode(self)
        elif menuchoice == "c":
            self.ai_mode(self)
        elif menuchoice == "x":
            return
        else:
            print("Invalid Input!")
            self.main_menu(self)

    def single_player_mode(self):
        level = self.level_menu(self)
        snake = Snake()
        game = board.Board("./levels/level" + level + ".txt", snake)
        while game.gameIsOn:
            game.printBoard()
            print(game.manhattan_distance())
            for x in game.chess_pieces:
                print(x.type, x.attacks)
            value = str(input())
            if value == "w" or value == "s" or value == "a" or value == "d":
                game.processInput(value)
        if game.checkSum():
            print("All pieces attack an equal number of squares")
        else:
            print("Pieces have a different number of squares attacked")
        for x in game.chess_pieces:
            print(x.type, x.attacks)
        self.main_menu(self)

    def ai_mode(self):
        print("Sorry this mode is not available at the moment")
        print("Enter 0 to return to main menu")
        menuchoice = str(input())
        while menuchoice != "0":
            print("Invalid Input!")
            print("Enter 0 to return to main menu")
            menuchoice = str(input())
        self.main_menu(self)

    def level_menu(self):
        print("Select number of puzzle: ")
        print("For puzzle with size 5x5 enter a number between 1-10")
        print("For puzzle with size 6x6 enter a number between 11-20")
        menuchoice = str(input())
        while 1 > int(menuchoice) > 20:
            print("Invalid Input!")
            print("For puzzle with size 5x5 enter a number between 1-10")
            print("For puzzle with size 6x6 enter a number between 11-20")
            menuchoice = str(input())
        return menuchoice
