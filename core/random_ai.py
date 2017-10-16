"""Contains basic, randomly firing AI."""
from . import player
import random


class Random_AI(player.Player):
    """
    Simple, randomly firing AI.

    Inherits from Player class, all its methods available.

    METHODS:
    turn - play one turn of game against oponnent
    """

    def __init__(self):
        """Initialize the AI. Doesn't require any arguments."""
        player.Player.__init__(self)  # init the Player class.
        # create the hit_list
        self.hit_list = []
        for x in range(10):
            for y in range(10):
                self.hit_list.append([x, y])

    def turn(self, opponent):
        """
        Play one turn of game against opponent.

        ARGUMENTS:
        opponnent - object of the oponnent, expects Player class
                    or class inheriting hit method from Player class
        """
        # pick random coord from hit_list and remove it from hit_list
        coords = self.hit_list[random.randint(0, len(self.hit_list)-1)]
        self.hit_list.remove(coords)
        # hit opponent at picked coord.
        opponent.hit(coords)
