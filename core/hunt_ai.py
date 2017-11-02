"""Contains Hunt/Target AI with two modes."""
from . import player
import random
from . import field_utils


class Hunt_AI(player.Player):
    """
    Hunt/Target AI class.

    Inherits from Player class.

    Hunts for a ship and then targets it.
    Has two modes for hunting - parity and non-parity

    METHODS:
    turn - plays a one turn against oponnent
    hunt - plays one hunt turn againt oponnent
    target - plays one target turn against oponnent
    create_targets
    cleanup_ship
    """
    def __init__(self, parity=True):
        """
        Initialize the AI.

        ARGUMENTS:
        parity - if the AI should use parity in hunt mode, default True
        """
        player.Player.__init__(self)  # init Player class

        # create variables to store the state of the AI
        self.enemy_field = field_utils.create_field()
        self.hit_list = []
        self.mode = "hunt"
        self.previous_hits = [None]
        self.target_list = []

        # create hit_list
        for x in range(10):
            for y in range(10):
                if (x + y) % 2 == 0 and parity:
                    self.hit_list.append([x, y])
                elif not parity:
                    self.hit_list.append([x, y])

    def turn(self, enemy):
        """
        Play one turn against opponent.

        ARGUMENTS:
        enemy - enemy object to play against, expects Player class or
                class inheriting from it.
        """
        if self.mode == "hunt":
            self.hunt(enemy)
        elif self.mode == "target":
            self.target(enemy)

    def hunt(self, enemy):
        """
        Play one hunt turn against opponent.

        Please don't use unless you 100 percent sure you need to.

        ARGUMENTS:
        enemy - enemy object to play against, expects Player class or
                class inheriting from it.
        """
        # pick a random spot from hit_list, if has 1 element, pick that one.
        if len(self.hit_list) > 1:
            coords = self.hit_list[random.randint(0, len(self.hit_list)-1)]
        elif len(self.hit_list) == 1:
            coords = self.hit_list[0]
        else:  # if hit_list empty, generate new one, pick random one from it.
            self.hit_list = regen_hit_list(self.enemy_field)
            coords = self.hit_list[random.randint(0, len(self.hit_list)-1)]

        # indicate that spot has been hit in enemy_field
        self.enemy_field[coords[0]][coords[1]]["hit"] = True

        # hit an enemy and get status
        ship_hit, ship_sunk, ship_length = enemy.hit(coords)
        self.hit_list.remove(coords)  # remove hit from hit_list

        # if hit is successful, change to target mode
        if ship_hit:
            self.enemy_field[coords[0]][coords[1]]["content"] = "ship"
            self.previous_hits[0] = coords
            self.mode = "target"

    def target(self, enemy):
        """
        Play one target turn against opponent.

        Please don't use unless you 100 percent sure you need to.

        ARGUMENTS:
        enemy - enemy object to play against, expects Player class or
                class inheriting from it.
        """

        # create possible targets and pick one(or the only one)
        self.create_targets()
        if len(self.target_list) > 1:
            coords = self.target_list[random.randint(0, len(self.target_list)-1)]

        # if no possible targets, switch to hunt mode
        elif len(self.target_list) == 0:
            self.mode = "hunt"
            self.target_list = []
            self.previous_hits = [None]
            return
        else:
            coords = self.target_list[0]

        # reflect hit in enemy_field
        self.enemy_field[coords[0]][coords[1]]["hit"] = True

        # hit enemy and get status
        ship_hit, ship_sunk, ship_length = enemy.hit(coords)

        # if target coord was also in hit_list, remove it
        if coords in self.hit_list:
            self.hit_list.remove(coords)

        # if ship hit, add to previous_hits
        if ship_hit:
            self.enemy_field[coords[0]][coords[1]]["content"] = "ship"
            self.previous_hits.append(coords)

        # if ship_sunk and only hits were ship, switch to hunt mode
        if ship_sunk and len(self.previous_hits) == ship_length:
            self.mode = "hunt"
            self.target_list = []
            self.previous_hits = [None]
        # if ship_sunk and more hits than ship, cleanup ship from previous_hits
        # and continue hunting
        elif ship_sunk and len(self.previous_hits) > ship_length:
            self.cleanup_ship(ship_length)

    def create_targets(self):
        """
        Create possible targets based on previous hits.

        Please don't use unless you 100 percent sure you need to.
        """
        # create neighbors for all previous hits
        targets = []
        for hit in self.previous_hits:
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
            if target in self.previous_hits:
                targets_clean1.remove(target)

        # remove already hit spots
        targets_clean2 = []
        for target in targets_clean1:
            if not self.enemy_field[target[0]][target[1]]["hit"]:
                targets_clean2.append(target)

        # write to target_list var
        self.target_list = targets_clean2

    def cleanup_ship(self, length):
        """
        Remove ship from previous_hits.

        Please don't use unless you 100 percent sure you need to.
        """
        # get last hit and find direction of ship
        last = self.previous_hits[-1]
        direction = (0, 0)
        if [last[0]-length+1, last[1]] in self.previous_hits:
            direction = (-1, 0)
        elif [last[0]+length-1, last[1]] in self.previous_hits:
            direction = (1, 0)
        elif [last[0], last[1]-length+1] in self.previous_hits:
            direction = (0, -1)
        elif [last[0], last[1]+length-1] in self.previous_hits:
            direction = (0, 1)

        # remove ship coords from previous hits
        for i in range(length):
            removal = [last[0]+i*direction[0], last[1]+i*direction[1]]
            if removal in self.previous_hits:
                self.previous_hits.remove(removal)


def regen_hit_list(field):
    """
    Generate new hit_list based on field provided.

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
