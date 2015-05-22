from tic import TicTacToe
from battleship import Battleship
from minesweeper import Minesweeper

LIST_OF_GAMES = ["Tic Tac Toe", "Battleship", "Minesweeper"]


class GameHandler(object):
    def initialize_game(self):
        """Sets up a menu for playing a game, then initializes the picked game."""
        print("Games Games Games")
        for i, game in enumerate(LIST_OF_GAMES):
            print("{}. {}".format(i + 1, game))
        game = input("Which game do you want to play? (1, 2, 3): ")
        while True:
            if game == "1":
                tic = TicTacToe()
                tic.play_game()
                return
            elif game == "2":
                battle = Battleship()
                battle.play_game()
                return
            elif game == "3":
                mine = Minesweeper()
                mine.play_game()
                return
            else:
                raise InvalidInput("Please enter 1, 2, or 3 to play a game.")
