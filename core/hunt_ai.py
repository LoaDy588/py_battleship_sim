"""Contains Hunt/Target AI with two modes."""
from . import player
from . import field_utils
import random


class Hunt_AI(player.Player):
    """
    Hunt/Target AI class.

    Inherits from Player class.

    Hunts for a ship and then targets it.
    Has two modes for hunting - parity and non-parity

    METHODS:
    turn - plays a one turn against oponnent
    __hunt - plays one hunt turn againt oponnent, private
    __target - plays one target turn against oponnent, private
    __create_targets - private method
    __cleanup_ship - private method
    """
    def __init__(self, parity=True):
        """
        Initialize the AI.

        ARGUMENTS:
        parity - if the AI should use parity in hunt mode, default True
        """
        player.Player.__init__(self)  # init Player class

        # create variables to store the state of the AI
        self.__enemy_field = field_utils.create_field()
        self.__hit_list = []
        self.__mode = "hunt"
        self.__previous_hits = [None]
        self.__target_list = []

        # create hit_list
        for x in range(10):
            for y in range(10):
                if (x + y) % 2 == 0 and parity:
                    self.__hit_list.append([x, y])
                elif not parity:
                    self.__hit_list.append([x, y])

    def turn(self, enemy):
        """
        Play one turn against opponent.

        ARGUMENTS:
        enemy - enemy object to play against, expects Player class or
                class inheriting from it.
        """
        if self.__mode == "hunt":
            self.__hunt(enemy)
        elif self.__mode == "target":
            self.__target(enemy)

    def __hunt(self, enemy):
        """
        Play one hunt turn against opponent.

        Private method.

        ARGUMENTS:
        enemy - enemy object to play against, expects Player class or
                class inheriting from it.
        """
        # pick a random spot from hit_list, if has 1 element, pick that one.
        if len(self.__hit_list) > 1:
            coords = self.__hit_list[random.randint(0, len(self.__hit_list)-1)]
        elif len(self.__hit_list) == 1:
            coords = self.__hit_list[0]
        else:  # if hit_list empty, generate new one, pick random one from it.
            self.__hit_list = regen_hit_list(self.__enemy_field)
            coords = self.__hit_list[random.randint(0, len(self.__hit_list)-1)]

        # indicate that spot has been hit in enemy_field
        self.__enemy_field[coords[0]][coords[1]]["hit"] = True

        # hit an enemy and get status
        ship_hit, ship_sunk, ship_length = enemy.hit(coords)
        self.__hit_list.remove(coords)  # remove hit from hit_list

        # if hit is successful, change to target mode
        if ship_hit:
            self.__enemy_field[coords[0]][coords[1]]["content"] = "ship"
            self.__previous_hits[0] = coords
            self.__mode = "target"

    def __target(self, enemy):
        """
        Play one target turn against opponent.

        Private method.

        ARGUMENTS:
        enemy - enemy object to play against, expects Player class or
                class inheriting from it.
        """

        # create possible targets and pick one(or the only one)
        self.__create_targets()
        if len(self.__target_list) > 1:
            coords = self.__target_list[random.randint(0, len(self.__target_list)-1)]

        # if no possible targets, switch to hunt mode
        elif len(self.__target_list) == 0:
            self.__mode = "hunt"
            self.__target_list = []
            self.__previous_hits = [None]
            return
        else:
            coords = self.__target_list[0]

        # reflect hit in enemy_field
        self.__enemy_field[coords[0]][coords[1]]["hit"] = True

        # hit enemy and get status
        ship_hit, ship_sunk, ship_length = enemy.hit(coords)

        # if target coord was also in hit_list, remove it
        if coords in self.__hit_list:
            self.__hit_list.remove(coords)

        # if ship hit, add to previous_hits
        if ship_hit:
            self.__enemy_field[coords[0]][coords[1]]["content"] = "ship"
            self.__previous_hits.append(coords)

        # if ship_sunk and only hits were ship, switch to hunt mode
        if ship_sunk and len(self.__previous_hits) == ship_length:
            self.__mode = "hunt"
            self.__target_list = []
            self.__previous_hits = [None]
        # if ship_sunk and more hits than ship, cleanup ship from previous_hits
        # and continue hunting
        elif ship_sunk and len(self.__previous_hits) > ship_length:
            self.__cleanup_ship(ship_length)

    def __create_targets(self):
        """
        Create possible targets based on previous hits.

        Private method.
        """
        # create neighbors for all previous hits
        targets = []
        for hit in self.__previous_hits:
            neighbors = field_utils.get_neighbors(hit)
            for neighbor in neighbors:
                targets.append(neighbor)

        # remove duplicates
        targets_clean1 = []
        for target in targets:
            if target not in targets_clean1:
                targets_clean1.append(target)

        # remove previous hits
        for target in targets_clean1:
            if target in self.__previous_hits:
                targets_clean1.remove(target)

        # remove already hit spots
        targets_clean2 = []
        for target in targets_clean1:
            if not self.__enemy_field[target[0]][target[1]]["hit"]:
                targets_clean2.append(target)

        # write to target_list var
        self.__target_list = targets_clean2

    def __cleanup_ship(self, length):
        """
        Remove ship from previous_hits.

        Private method.
        """
        # get last hit and find direction of ship
        last = self.__previous_hits[-1]
        direction = (0, 0)
        if [last[0]-length+1, last[1]] in self.__previous_hits:
            direction = (-1, 0)
        elif [last[0]+length-1, last[1]] in self.__previous_hits:
            direction = (1, 0)
        elif [last[0], last[1]-length+1] in self.__previous_hits:
            direction = (0, -1)
        elif [last[0], last[1]+length-1] in self.__previous_hits:
            direction = (0, 1)

        # remove ship coords from previous hits
        for i in range(length):
            removal = [last[0]+i*direction[0], last[1]+i*direction[1]]
            if removal in self.__previous_hits:
                self.__previous_hits.remove(removal)


def regen_hit_list(field):
    """
    Generate new hit_list based on field provided.

    New targets are neighbors of ships in field.

    ARGUMENTS:
    field - field to generate hit_list from
    """
    # create list of ship occupied spots in field
    ships = []
    for x in range(10):
        for y in range(10):
            if field[x][y]["content"] == "ship":
                ships.append([x, y])
    hit_list = []

    # create neighbors for all ships and prevent duplicates
    for ship in ships:
        neighbors = field_utils.get_neighbors(ship)
        for neighbor in neighbors:
            if neighbor not in hit_list:
                hit_list.append(neighbor)

    # remove already hit spots
    for hit in hit_list:
        if field[hit[0]][hit[1]]["hit"]:
            hit_list.remove(hit)
    return hit_list
