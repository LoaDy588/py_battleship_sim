from . import player
import random


class Random_AI(player.Player):
    def __init__(self):
        player.Player.__init__(self)
        self.hit_list = []
        for x in range(10):
            for y in range(10):
                self.hit_list.append([x, y])

    def turn(self, opponent):
        coords = self.hit_list[random.randint(0, len(self.hit_list)-1)]
        self.hit_list.remove(coords)
        opponent.hit(coords)
