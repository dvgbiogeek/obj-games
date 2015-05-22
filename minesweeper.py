import random
from base import Board, Player, BaseGame


class TileBoard(Board):
    """Board class for game boards requiring tile objects with different visibilities."""
    def __init__(self, size=None, owner=None):
        self.size = size
        if self.size <= 10:
            self.width = 2
        else:
            self.width = len(str(self.size))
        self.owner = owner
        self.board = [[Tile() for i in range(size)] for j in range(size)]

    def _board_detail(self, i, j, player=None):
        """Prints visible and flagged tiles on the Minesweeper board."""
        if self.board[i][j].is_visible:
            return self.board[i][j].value
        elif self.board[i][j].is_flagged:
            return "{}".format(player.mark)
        else:
            return " "


class Tile(object):
    """Tile class for the Minesweeper board."""
    def __init__(self):
        self.is_flagged = False
        self.is_mine = False
        self.is_visible = False
        self.value = None


class Minesweeper(BaseGame):
    """Class for Minesweeper."""

    def __init__(self):
        """Initialize a game with 1 player, an 8x8 board."""
        self.num_players = 1

        self.board = TileBoard(size=8)

        self.players = []
        for i in range(self.num_players):
            self.players.append(Player.add_player(self.players))

    def play_game(self):
        """Main function for playing Minesweeper."""
        print("Minesweeper")
        self._set_mines()
        self._mine_counts()
        player = self.players[0]
        print(self.board.game_board(player))
        while True:
            self._player_turn(player)
            return

    def _set_mines(self):
        """Places the desired number of mines on the board."""
        while True:
            try:
                n_mines = int(input("How many mines?: "))
                if n_mines >= self.board.size ** 2:
                    raise InvalidInput("Too many mines. Enter a smaller value.")
                break
            except ValueError:
                print("Be sure to add numeric values only.")
            except Exception as e:
                print(e)
        # Place mines.
        added_mines = set()
        while len(added_mines) < n_mines:
            # Get coordinates.
            temp = (random.randint(0, self.board.size - 1),
                    random.randint(0, self.board.size - 1),)
            added_mines.add(temp)
            self.board.board[temp[0]][temp[1]].value = "*"
            self.board.board[temp[0]][temp[1]].is_mine = True
        return

    def _mine_counts(self):
        """Determines how many mines are adjacent to a location on the board and sets the value."""
        for x in range(self.board.size):
            for y in range(self.board.size):
                if self.board.board[x][y].value is None:
                    mine_count = 0
                    for i in self._get_adjacent_positions(x, y):
                        if self.board.board[i[0]][i[1]].value == "*":
                            mine_count += 1
                    if mine_count > 0:
                        self.board.board[x][y].value = str(mine_count)
                    else:
                        self.board.board[x][y].value = "-"

    def _get_adjacent_positions(self, x_coord, y_coord):
        """Gets the neighboring position of an x, y coordinate and returns the list of positions."""
        positions = []
        # the adjacency matrix, This could be done once and cloned.
        adjacency = [(i, j) for i in (-1, 0, 1) for j in (-1, 0, 1) if not (i == j == 0)]
        for x, y in adjacency:
            # boundaries check
            if 0 <= x_coord + x and x_coord + x <= self.board.size - 1 and \
                    0 <= y_coord + y and y_coord + y <= self.board.size - 1:
                pos = (x_coord + x, y_coord + y)
                positions.append(pos)
        return positions

    def _player_turn(self, player):
        """Function for a players turn."""
        print("{} choose a location.".format(player.name))
        while True:
            x, y, f = self._get_coords(player, coord_int=3, size=self.board.size)
            self._process(x, y, f)
            print(self.board.game_board(player))
            if self._dead_or_alive(x, y, player):
                return
            if self._check_win(player):
                return

    def _user_coords(self, player):
        """Gets the user input.

        Used with get_coords()."""
        u_input = input("{} enter coordinates and y or n to flag a mine (row, col, f): "
                .format(player.name))
        return u_input

    def _process(self, x, y, f, auto=False):
        """If a location has no surrounding bombs, sets surrounding locations are visible."""
        if self.board.board[x][y].is_visible:
            return
        flag_or_visible = self._flagging(x, y, f, auto)
        self._no_bombs(x, y, f)

    def _flagging(self, x, y, f, auto=False):
        """Allows a player to set a flag for a given location on the board."""
        if auto:
            f = "n"
        if f == "y":
            self.board.board[x][y].is_flagged = True
        else:
            self.board.board[x][y].is_visible = True

    def _no_bombs(self, x, y, f):
        """If a location has no neighboring bombs, this gets the positions and processes them."""
        if self.board.board[x][y].value == "-":
            for i in self._get_adjacent_positions(x, y):
                new_x, new_y = i
                self._process(new_x, new_y, f, auto=True)

    def _dead_or_alive(self, x, y, player):
        """Detemines if the player has stepped on a bomb and died, returns boolean."""
        if self.board.board[x][y].is_mine is True and self.board.board[x][y].is_visible is True:
            print("Ow. {} has stepped on a mine. :(".format(player.name))
            return True
        return False

    def _check_win(self, player):
        """Checks if a player has won.

        Checks if all tiles are visible minus the number of bombs on the board."""
        num_mines = 0
        num_visible = 0
        for i in range(self.board.size):
            for j in range(self.board.size):
                if self.board.board[i][j].is_visible is True:
                    num_visible += 1
                if self.board.board[i][j].is_mine is True:
                    num_mines += 1
        if num_visible == self.board.size ** 2 - num_mines:
            print("{} has won!".format(player.name))
            return True
