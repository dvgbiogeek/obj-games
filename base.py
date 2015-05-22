import random


class InvalidInput(Exception):
    pass


class BaseGame(object):
    """Stub class for games."""
    def __init__(self):
        self.num_players = None

    def play_game(self):
        pass

    def _user_coords(self, player):
        u_input = input("{} enter coordinates (row, col): ".format(player.name))
        return u_input

    def _get_coords(self, player, coord_int, size):
        """Gets the row, colomn for the players move and checks whether it is the

        right length, and composed of numbers between 1 and the size of the board.
        """
        while True:
            u_input = self._user_coords(player)
            try:
                coords = u_input.split(",")
                if len(coords) != coord_int:
                    raise InvalidInput("Too many or too few coordinates given.")
                coords[0] = int(coords[0]) - 1
                coords[1] = int(coords[1]) - 1
                if coords[0] < 0 or coords[0] > size or coords[1] < 0 or \
                        coords[1] > size:
                    raise InvalidInput("Please enter a value between 1 and {}.".format(
                            self.board.size))
                if coord_int == 3:
                    if coords[2] == "y" or coords[2] == "n":
                        break
                    else:
                        raise InvalidInput('"y" or "n" required.')
                break
            except ValueError:
                print("Be sure to enter numeric values only.")
            except InvalidInput as e:
                print(e)
            print("Sorry those coordinates were invalid please try again.")

        return coords

    def _check_win(self):
        pass


class Board(object):
    """Board class for game board objects."""
    def __init__(self, size=None, owner=None):
        self.size = size
        if self.size <= 10:
            self.width = 2
        else:
            self.width = len(str(self.size))
        self.owner = owner
        self.board = [[None] * size for i in range(size)]

    def _fixed_width_str(self, x, fill=' '):
        """Generates ' ' to line up the rows and columns with different sized boards."""
        x_str = str(x)
        l = len(x_str)
        pad = self.width - l
        if pad < 0:
            raise Exception("Your string is too long!")
        return fill * pad + x_str

    def _board_detail(self, i, j, player=None):
        """Function for showing a value on the board."""
        if self.board[i][j] is not None:
            return self.board[i][j]
        else:
            return ' '

    def game_board(self, player=None):
        """Prints a the board to screen."""
        # generate a list for the columns - values are padded for fixed width.
        column_name = [self._fixed_width_str(i) for i in range(1, self.size + 1)]
        # prints the top row of column values
        print('    {}  '.format('    '.join(column_name)))
        for i in range(self.size):
            # generates the row values for each column
            row_list = [self._board_detail(i, j, player) for j in range(self.size)]
            row = "  |  ".join(row_list)
            # prints each row of the board
            print('{}   {} '.format(column_name[i], row))
            # prints partition between the rows
            if i != (self.size - 1):
                print("   " + "------" * (self.size - 1) + "-----")
            else:
                # Print blank line.
                print()


class Player(object):
    """Player class for player objects."""
    def __init__(self, name='', mark=''):
        self.name = name
        self.mark = mark

    def display(self):
        """Displays the player name and mark for a single Player object."""
        print("----Player----")
        print("Player {} is using {} as their mark".format(self.name, self.mark))

    def prompt_init():
        return dict(name=input("Enter your name: "),
                    mark=input("Enter a single letter as a board marker: "))

    prompt_init = staticmethod(prompt_init)

    def add_player(players):
        """Adds a player object."""
        markers = [player.mark for player in players]
        while True:
            init_args = Player.prompt_init()
            # Check valid player.
            if init_args['mark'] in markers:
                print("Sorry someone already chose marker {}, please choose another.".format(
                        init_args['mark']))
                continue
            # Exit if valid player.
            break
        # If we get here then we have a valid player to add.
        return Player(**init_args)

    add_player = staticmethod(add_player)
