import random
from base import Board, Player, BaseGame


class Ship(object):
    """Class for ship objects used in Battleship."""
    def __init__(self, name, length):
        self.name = name
        self.length = length
        self.health = self.length
        self.sunk = False


class BattleshipBoard(Board):
    """Board class for Battleship board objects."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _board_detail(self, i, j, player):
        if self.owner == player:
            if self.board[i][j] is not None:
                return self.board[i][j]
        else:
            if self.board[i][j] == "*" or self.board[i][j] == "$":
                return self.board[i][j]
        return " "


class Battleship(BaseGame):
    """Class for playing Battleship."""
    SHIP_TYPES = [
        {"name": "Aircraft Carrier", "length": 5},
        {"name": "Battleship", "length": 4},
        {"name": "Destroyer", "length": 3},
        {"name": "Submarine", "length": 3},
        {"name": "Patrol Boat", "length": 2},
    ]

    def __init__(self):
        """Initialize a game of Battleship with 2 players, a 10x10 board and 5 ships."""
        self.num_players = 2

        # Initialize players, board and boats added as attributes to the player.
        self.players = []
        for i in range(self.num_players):
            print("Player {}".format(i + 1))
            player = Player.add_player(self.players)
            setattr(player, 'board', BattleshipBoard(size=10, owner=player))
            setattr(player, 'ships', self._generate_ships())
            self.players.append(player)

    def play_game(self):
        """Main function for playing Battleship."""
        print("Welcome to Battleship")
        for player in self.players:
            print("{}, place your ships".format(player.name))
            self._place_ship(player)
        turn = 0
        turn_offset = random.randint(0, (self.num_players - 1))
        while True:
            active_player = self.players[(turn + turn_offset) % self.num_players]
            opponent = self.players[(turn + turn_offset + 1) % self.num_players]
            print("{}'s turn to shoot".format(active_player.name))
            opponent.board.game_board(active_player)
            self._player_turn(active_player, opponent)
            if self._check_win(active_player, opponent):
                return
            input("Hit ENTER to end your turn.")
            turn += 1

    def _place_ship(self, player):
        """Place ship on the board."""
        for ship in player.ships:
            valid = False
            while not valid:
                player.board.game_board(player)
                print("Placing {}".format(ship.name))
                x, y = self._get_coords(player, coord_int=2, size=player.board.size)
                orientation = self._v_or_h(ship)
                valid = self._validate_placement(player, ship, x, y, orientation)
                if not valid:
                    print("Cannot place a ship there. Try another location.")
                    input("Hit ENTER to continue.")
                    board.game_board(player)
            board = self._add_ship_to_board(player, ship, x, y, orientation)
            board.game_board(player)
        input("Done placing {}'s ships. Hit ENTER to continue.".format(player.name))

    def _v_or_h(self, ship):
        """Pick vertical or horizontal placement for the ship."""
        while True:
            placement = input("Is the {} place vertically or horizontally (v or h)?: ".format(
                    ship.name)).strip().lower()
            if placement == "v" or placement == "h":
                return placement
            else:
                print("Invalid input. Please enter either v or h.")

    def _validate_placement(self, player, ship, x, y, orientation):
        """Validate that the ship will fit on the board."""
        if orientation == "v" and ship.length + x > player.board.size:
            return False
        elif orientation == "h" and ship.length + y > player.board.size:
            return False
        else:
            if orientation == "v":
                for i in range(ship.length):
                    if player.board.board[x + i][y] is not None:
                        return False
            elif orientation == "h":
                for i in range(ship.length):
                    if player.board.board[x][y + i]:
                        return False
        return True

    def _add_ship_to_board(self, player, ship, x, y, orientation):
        """Place the ship onto the designated board."""
        marker = ship.name[0]
        if orientation == 'v':
            for i in range(ship.length):
                player.board.board[x + i][y] = marker
        elif orientation == 'h':
            for i in range(ship.length):
                player.board.board[x][y + i] = marker
        return player.board

    def _player_turn(self, player, opponent):
        """Player takes their turn."""
        while True:
            x, y = self._get_coords(player, coord_int=2, size=player.board.size)
            if self._validate_move(opponent, x, y):
                self._hit_or_miss(player, opponent, x, y)
                break
            print("Sorry that was not a valid move.")

    def _validate_move(self, opponent, x, y):
        """Check that the move has not already been made."""
        if opponent.board.board[x][y] == "*" or opponent.board.board[x][y] == "$":
            return False
        else:
            return True

    def _hit_or_miss(self, player, opponent, x, y):
        """Determine if shot was a hit or miss.

        If shot was a hit, determine which ship was hit, whether it is sunk,
        and place a hit marker on the board.
        """
        if opponent.board.board[x][y] is None:
            print("{}'s shot was a miss.".format(player.name))
            opponent.board.board[x][y] = "*"
        else:
            print("Hit!")
            ship = self._hit_ship(opponent, x, y)
            opponent.board.board[x][y] = "$"
            ship.health -= 1
            if ship.health == 0:
                ship.sunk = True
                print("{} has been sunk".format(ship.name))

    def _hit_ship(self, player, x, y):
        """Determines which ship has been hit."""
        for ship in player.ships:
            if player.board.board[x][y] == ship.name[0]:
                return ship

    def _generate_ships(self):
        """Initializes the boats for the game."""
        ships = [Ship(ship["name"], ship["length"]) for ship in self.SHIP_TYPES]
        return ships

    def _check_win(self, player, opponent):
        """Checks if a player has sunk all the opposing players ships."""
        for ship in opponent.ships:
            if ship.sunk is False:
                return False
        print("{} has won!".format(player.name))
        return True
