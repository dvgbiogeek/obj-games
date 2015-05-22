import random
from base import Board, Player, BaseGame


class TicTacToe(BaseGame):
    """Class for TicTacToe."""
    def __init__(self):
        """Initialize a game a Tic Tac Toe with 2 players and a 3x3 board."""
        self.num_players = 2

        self.board = Board(size=3)
        self.players = []
        for i in range(self.num_players):
            print("Player {}".format(i + 1))
            self.players.append(Player.add_player(self.players))

    def play_game(self):
        """Play TicTacToe."""
        print("Tic Tac Toe Time")
        self.board.game_board(player=None)
        turn = 0
        # For determining which player goes first
        turn_offset = random.randint(0, (self.num_players - 1))
        while(True):
            # Gets the player index in the player list for getting the player
            # whose turn it is.
            active_player = self.players[(turn + turn_offset) % self.num_players]
            self._player_turn(active_player)

            # First check if the active player has won
            if self._check_win(active_player):
                print("{} WON!".format(active_player.name))
                return
            # If active player did not win, check if the game is a stalemate
            if self._is_stalemate():
                print("It's a stalemate. Neither player has won!")
                return

            # Next players turn
            turn += 1

    def _player_turn(self, player):
        """Player takes their turn."""
        print("{}'s turn".format(player.name))
        while True:
            x, y = self._get_coords(player, coord_int=2, size=self.board.size)
            if self._validate_place(x, y):
                break
            print("Sorry that was not a valid move.")
        self.board.board[x][y] = player.mark
        self.board.game_board(player)

    def _validate_place(self, x, y):
        """Validates that the position is empty and returns True."""
        if self.board.board[x][y] is not None:
            print("Board position already taken. Choose another.")
            return False
        else:
            return True

    def _check_row(self, row, player):
        """Checks if a row consists of all the same player mark."""
        if len([i for i in row if i == player.mark]) == self.board.size:
            return True
        return False

    def _check_win(self, player):
        """Checks if a player has won the game."""
        # check diagonal
        diag = []
        for i in range(self.board.size):
            temp = self.board.board[i][i]
            diag.append(temp)
        if self._check_row(diag, player):
            return True
        # Generate a list with the other diagonal positions
        alt_diag = []
        for i in range(self.board.size):
            alt_temp = self.board.board[i][-i - 1]
            alt_diag.append(alt_temp)
        if self._check_row(alt_diag, player):
            return True
        # check horizontal rows
        for i in range(self.board.size):
            row = self.board.board[i]
            if self._check_row(row, player):
                return True
        # check vertical rows
        for i in range(self.board.size):
            row = [self.board.board[j][i] for j in range(self.board.size)]
            if self._check_row(row, player):
                return True
        return False

    def _is_stalemate(self):
        """If the board is full with no winner, then the game is a stalemate."""
        for i in range(self.board.size):
            if None in self.board.board[i]:
                return False
        return True
