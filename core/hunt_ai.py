from . import player
import random
from . import field_utils


class Hunt_AI(player.Player):
    def __init__(self, parity=True):
        player.Player.__init__(self)
        self.enemy_field = field_utils.create_field()
        self.hit_list = []
        self.mode = "hunt"
        self.previous_hits = [None]
        self.target_list = []
        for x in range(10):
            for y in range(10):
                if (x + y) % 2 == 0 and parity:
                    self.hit_list.append([x, y])
                elif not parity:
                    self.hit_list.append([x, y])

    def turn(self, enemy):
        if self.mode == "hunt":
            coords = self.hit_list[random.randint(0, len(self.hit_list)-1)]
            ship_hit, ship_sunk = enemy.hit(coords)
            self.hit_list.remove(coords)
            if ship_hit:
                self.enemy_field[coords[0]][coords[1]]["content"] = "ship"
                self.enemy_field[coords[0]][coords[1]]["hit"] = True
                self.previous_hits[0] = coords
                self.mode = "target"
            else:
                self.enemy_field[coords[0]][coords[1]]["hit"] = True

        elif self.mode == "target":
            self.create_targets()
            if not len(self.target_list) == 0:
                coords = self.target_list[random.randint(0, len(self.target_list)-1)]
            else:
                coords = self.target_list[0]
            ship_hit, ship_sunk = enemy.hit(coords)
            if coords in self.hit_list:
                self.hit_list.remove(coords)
            if ship_hit and not ship_sunk:
                self.enemy_field[coords[0]][coords[1]]["content"] = "ship"
                self.enemy_field[coords[0]][coords[1]]["hit"] = True
                self.previous_hits.append(coords)
            elif ship_hit and ship_sunk:
                self.enemy_field[coords[0]][coords[1]]["content"] = "ship"
                self.enemy_field[coords[0]][coords[1]]["hit"] = True
                self.mode = "hunt"
                self.target_list = []
                self.previous_hits = [None]
            else:
                self.enemy_field[coords[0]][coords[1]]["hit"] = True
            return

    def create_targets(self):
        targets = []
        for hit in self.previous_hits:
            neighbors = get_neighbors(hit)
            for neighbor in neighbors:
                targets.append(neighbor)
        for target in targets:
            if target in self.previous_hits:
                targets.remove(target)
        for target in targets:
            if self.enemy_field[target[0]][target[1]]["hit"]:
                targets.remove(target)
        targets_clean = []
        for target in targets:
            if target not in targets_clean:
                targets_clean.append(target)
        self.target_list = targets_clean


def get_neighbors(coords):
    neighbors = []
    directions = [0, 1, 2, 3]
    if coords[0]+1 > 9:
        directions.remove(2)
    if coords[0]-1 < 0:
        directions.remove(0)
    if coords[1]+1 > 9:
        directions.remove(3)
    if coords[1]-1 < 0:
        directions.remove(1)
    for i in directions:
        neighbor = []
        if i == 0:
            x = coords[0] - 1
            y = coords[1]
        elif i == 1:
            x = coords[0]
            y = coords[1] - 1
        elif i == 2:
            x = coords[0] + 1
            y = coords[1]
        elif i == 3:
            x = coords[0]
            y = coords[1] + 1
        neighbor.append(x)
        neighbor.append(y)
        neighbors.append(neighbor)
    return neighbors
