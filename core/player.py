"""Contains basic Player class."""
from . import field_utils


class Player:
    """
    Basic Player class.

    Can be used as a base for AI or as a "dummy" player against AI.


    METHODS:
    hit - place a hit on instance's field at specified coords
    has_lost - check if all ships are sunk
    get_field - returns field of the instance
    get_shiplist - returns shiplist of the instance
    """

    def __init__(self):
        """Initialize the instance, doesn't require arguments."""
        # create field and shiplist
        self.__field, self.__shiplist = field_utils.create_random()

    def hit(self, coords):
        """
        Hit a spot in instance's field, return data of success.

        ARGUMENTS:
        coords - coords to hit, expects [x, y] format

        RETURNS(tuple):
        ship_hit - boolean, True if a part of ship was hit
        ship_sunk - boolean, True if the ship was ship_sunk
        ship_length - int, length of sunken ship, 0 if not ship_sunk
        """
        x = coords[0]
        y = coords[1]
        # reflect hit in field
        self.__field[x][y]["hit"] = True
        # check ship status
        if self.__field[x][y]["content"] == "ship":
            ship_id = self.__field[x][y]["shipID"]
            ship_sunk = field_utils.check_ship(self.__field,
                                               self.__shiplist[ship_id])
            # default length to zero unless ship sunken
            length = 0
            if ship_sunk:
                length = self.__shiplist[ship_id]["length"]
            return True, ship_sunk, length
        else:
            return False, False, 0

    def has_lost(self):
        """Check if player has lost(all ships sunk), return boolean."""
        ship_status = []
        # check if sunk for every ship
        for ship in self.__shiplist:
            ship_status.append(field_utils.check_ship(self.__field, ship))
        # if all ships sunk
        if sum(ship_status) == 5:
            return True
        else:
            return False

    def get_field(self):
        """Return field of the instance."""
        return self.__field

    def get_shiplist(self):
        """Return shiplist of the instance."""
        return self.__shiplist
