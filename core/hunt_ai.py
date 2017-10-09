from . import player
import random
from . import field_utils


class Hunt_AI(player.Player):
    def __init__(self, parity=True):
        player.Player.__init__(self)
        self.enemy_field = field_utils.create_field()
        self.hit_list = []
        self.mode = "hunt"
        self.previous_hits = []
        self.target_list = []
        for x in range(10):
            for y in range(10):
                if (x + y % 2) == 0 and parity:
                    self.hit_list.append([x, y])
                elif not parity:
                    self.hit_list.append([x, y])

    def turn(self, enemy):
        if self.mode == "hunt":
            coords = self.hit_list[random.randint(0, len(self.hit_list)-1)]
            ship_hit, ship_sunk = enemy.hit(coords)
            if coords in hit_list:
                self.hit_list.remove(coords)
            if ship_hit:
                self.enemy_field[coords[0]][coords[1]]["content"] = "ship"
                self.previous_hits[0] = coords
                self.mode = "target"
            else:
                self.enemy_field[coords[0]][coords[1]]["content"] = "water"

        elif self.mode == "target":
            create_targets()
            coords = self.target_list[random.randint(0, len(self.target_list)-1)]
            ship_hit, ship_sunk = enemy.hit(coords)
            if coords in self.hit_list:
                self.hit_list.remove(coords)
            if ship_hit:
                self.enemy_field[coords[0]][coords[1]]["content"] = "ship"
                self.previous_hits.append(coords)
            elif ship_sunk:
                self.enemy_field[coords[0]][coords[1]]["content"] = "ship"
                self.mode = "hunt"
                self.target_list = []
                self.previous_hits = []
            else:
                self.enemy_field[coords[0]][coords[1]]["content"] = "water"
            return

    def create_targets(self):
        
