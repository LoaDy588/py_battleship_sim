"""Contains probailistic AI."""
import random
from . import player
from . import field_utils


class Probabilistic_AI(player.Player):
    """
    Probabilistic AI class.

    Inherits from Player class.

    Calculates probability field of all currently possible ship orientations,
    then picking the spot with highest probability.

    METHODS:
    turn - plays a one turn against oponnent
    __generate_target - creates target to hits, private
    __create_probab_field - creates probability field, Private
    __find_orientations - finds all currently possible orientations for a ship,
                          private
    __add_to_field - adds ship to probability field, private
    __generate_possible_points - finds all currently possible starting points
                                 for ships, Private
    __sink_ship - "sinks" specified ship in __enemy_field
    """

    def __init__(self):
        """Initialize the AI."""
        player.Player.__init__(self)  # init Player class

        # create variables for storing oponnent state
        self.__enemy_field = field_utils.create_field()
        self.__enemy_shiplist = field_utils.create_shiplist()

        # add a "sunk" key with default False for every point in __enemy_field
        for x in range(10):
            for y in range(10):
                self.__enemy_field[x][y]["sunk"] = False

    def turn(self, oponnent, debug=False):
        """
        Play one turn against opponent.

        ARGUMENTS:
        enemy - enemy object to play against, expects Player class or
                class inheriting from it.
        debug - default False, if True, display probability field before turn
        """
        # find a point to hit and change state of point to hit
        coords = self.__generate_target(debug)
        self.__enemy_field[coords[0]][coords[1]]["hit"] = True

        # play the turn and get answer from oponnent
        ship_hit, ship_sunk, length = oponnent.hit(coords)

        # if ship was hit, reflect state in __enemy_field
        if ship_hit:
            self.__enemy_field[coords[0]][coords[1]]["content"] = "ship"

        # if ship was sunk, reflect state in __enemy_field
        # and remove ship from shiplist
        if ship_sunk:
            self.__sink_ship(coords, length)
            for ship in self.__enemy_shiplist:
                if ship["length"] == length:
                    self.__enemy_shiplist.remove(ship)
                    break

    def __generate_target(self, debug):
        """
        Generate target for turn.

        Private method.

        ARGUMENTS:
        debug - if True, displays probability field before continuing
        """
        probability = self.__create_probab_field()
        if debug:  # debug
            display_probability(probability)
        target = find_highest(probability)

        # pick random item from list of possible spots
        if len(target) == 1:
            return target[0]
        else:
            # bad fix, cause of error is somewhere in probability field generation
            # prevents AI from hiting same spot more than once
            pointer = target[random.randint(0, len(target)-1)]
            while self.__enemy_field[pointer[0]][pointer[1]]["hit"]:
                pointer = target[random.randint(0, len(target)-1)]
            return pointer

    def __create_probab_field(self):
        """
        Generate probability field for the current state.

        Private method.
        """
        # find possible points and create empty probability field
        possible_points = self.__generate_possible_points()
        probab_field = [[0 for y in range(10)] for x in range(10)]

        # place all remaining ships at every possible point, at every possible orientation
        for ship in self.__enemy_shiplist:
            for point in possible_points:
                orientations, bonus = self.__find_orientations(point, ship["length"])
                for index, orientation in enumerate(orientations):
                    self.__add_to_field(probab_field, orientation, bonus[index],
                                        point, ship["length"])

        return probab_field

    def __find_orientations(self, coords, length):
        """
        Find every possible current orientation of a ship.

        Returns tuple of vectors(orientations) and tuple which contains, if
        orientation should have a bonus

        Orientation has a bonus when it passes through spot, which has been hit
        and is not a sunken ship.

        Private method.

        ARGUMENTS:
        coords - coordinates of the starting point of ship
        length - length of the ship
        """
        possible = []
        possible_bonus = []
        vectors = ((1, 0), (0, 1), (-1, 0), (0, -1))
        for vctr in vectors:
            # if outside the field, skip to next orientation
            if coords[0]+(length-1)*vctr[0] > 9:
                continue
            if coords[1]+(length-1)*vctr[1] > 9:
                continue
            if coords[0]+(length-1)*vctr[0] < 0:
                continue
            if coords[1]+(length-1)*vctr[1] < 0:
                continue
            temp = []
            bonus = False  # default bonus value

            # check if all spots in orientation are either not hit or hit, but
            # not sunken ship. If it passes through non-sunken ship, add bonus
            for i in range(length):
                pointer = self.__enemy_field[coords[0]+i*vctr[0]][coords[1]+i*vctr[1]]
                if not pointer["hit"]:
                    temp.append(True)
                elif pointer["hit"]:
                    if pointer["content"] == "ship" and not pointer["sunk"]:
                        temp.append(True)
                        bonus = True
            if sum(temp) == length:
                possible.append(vctr)
                possible_bonus.append(bonus)

        return tuple(possible), tuple(possible_bonus)

    def __add_to_field(self, probab_field, direction, bonus, point, length):
        """
        Place ship in probability field.

        ARGUMENTS:
        probab_field - probability field to place the ship in
        direction - vector of the orientation to place ship in
        bonus - boolean, if True, place with a bonus
        point - starting point of the ship
        length - length of the ship
        """
        for i in range(length):
            pointer = (point[0]+i*direction[0], point[1]+i*direction[1])

            # should prevent repeated hits for same spot
            # might not work properly - check fix in __generate_target func
            if not self.__enemy_field[pointer[0]][pointer[1]]["hit"]:
                # check for bonus
                if bonus:
                    probab_field[pointer[0]][pointer[1]] += 10
                else:
                    probab_field[pointer[0]][pointer[1]] += 1

    def __generate_possible_points(self):
        """
        Generate all possible starting points for ships at current state.

        Starting points are either never hit spots or already hit spot
        with ship which is not sunken.

        Private method.
        """
        possible = []
        # go through all points
        for x in range(10):
            for y in range(10):
                pointer = self.__enemy_field[x][y]

                # check if suitable state
                if pointer["content"] == "water" and not pointer["hit"]:
                    possible.append((x, y))
                elif pointer["content"] == "ship" and not pointer["sunk"]:
                    possible.append((x, y))

        return possible

    def __sink_ship(self, coords, length):
        """
        Sink the ship in __enemy_field.

        Private method.

        ARGUMENTS:
        coords - start point of ship to sink
        length - length of ship to sink
        """
        # find the orientation of ship to sink
        # if it can't find suitable orientation, defaults to (0, 0) vector
        # this is probably the cause for the fix in __generate_target func
        vectors = ((1, 0), (0, 1), (-1, 0), (0, -1))
        direction = (0, 0)
        for vctr in vectors:

            # if outside the field, skip to next orientation
            if coords[0]+(length-1)*vctr[0] > 9:
                continue
            if coords[1]+(length-1)*vctr[1] > 9:
                continue
            if coords[0]+(length-1)*vctr[0] < 0:
                continue
            if coords[1]+(length-1)*vctr[1] < 0:
                continue

            temp = []

            # step through the length of the ship and check state
            # state must be: is a ship and is not sunken
            # has redudant check, to see if all the points of the ship were hit
            for i in range(length):
                pointer = self.__enemy_field[coords[0]+i*vctr[0]][coords[1]+i*vctr[1]]
                if pointer["content"] == "ship" and not pointer["sunk"]:
                    temp.append(pointer["hit"])

            # do the redudant check, if pass break cycle, orientation was found
            if sum(temp) == length:
                direction = vctr
                break

        # step through the ship and change "sunk" key of every occupied point
        for i in range(length):
            removal = (coords[0]+i*direction[0], coords[1]+i*direction[1])
            self.__enemy_field[removal[0]][removal[1]]["sunk"] = True


def find_highest(probab_field):
    """
    Find the points with highest value in probabilty field.

    Returns list with 1 or more tuples of coordinates.

    ARGUMENTS:
    probab_field - probability field, expects 10x10 field
    """

    # default to (0. 0) and 0 value
    current = [(0, 0)]
    current_value = 0

    # step through the whole field
    for x in range(10):
        for y in range(10):

            # if higher value, rewrite list to contain this point, update value
            if probab_field[x][y] > current_value:
                current = [(x, y)]
                current_value = probab_field[x][y]

            # if same value, append this point to list
            elif probab_field[x][y] == current_value:
                current.append((x, y))

    return current


def display_probability(field):
    for y in range(10):
        for x in range(10):
            print(field[x][y], " ", end="")
        print()
    i = input("Press any key to continue")
