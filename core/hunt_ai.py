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
            self.enemy_field[coords[0]][coords[1]]["hit"] = True
            print(coords)
            ship_hit, ship_sunk, ship_length = enemy.hit(coords)
            self.hit_list.remove(coords)
            if ship_hit:
                self.enemy_field[coords[0]][coords[1]]["content"] = "ship"
                self.previous_hits[0] = coords
                self.mode = "target"

        elif self.mode == "target":
            self.create_targets()
            if not len(self.target_list) == 1:
                coords = self.target_list[random.randint(0, len(self.target_list)-1)]
            else:
                coords = self.target_list[0]
            self.enemy_field[coords[0]][coords[1]]["hit"] = True
            print(coords)
            ship_hit, ship_sunk, ship_length = enemy.hit(coords)
            if coords in self.hit_list:
                self.hit_list.remove(coords)
            if ship_hit:
                self.enemy_field[coords[0]][coords[1]]["content"] = "ship"
                self.previous_hits.append(coords)
            if ship_sunk and len(self.previous_hits) == ship_length:
                self.mode = "hunt"
                self.target_list = []
                self.previous_hits = [None]
            elif ship_sunk and len(self.previous_hits) > ship_length:
                self.cleanup_ship(ship_length)
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

    def cleanup_ship(self, length):
        last = self.previous_hits[-1]
        direction = 0
        if [last[0]-length+1, last[1]] in self.previous_hits:
            direction = 0
        elif [last[0]+length-1, last[1]] in self.previous_hits:
            direction = 2
        elif [last[0], last[1]-length+1] in self.previous_hits:
            direction = 1
        elif [last[0], last[1]+length-1] in self.previous_hits:
            direction = 3
        for i in range(length):
            if direction == 0:
                removal = [last[0]-i, last[1]]
                if removal in self.previous_hits:
                    self.previous_hits.remove(removal)
            elif direction == 1:
                removal = [last[0], last[1]-i]
                if removal in self.previous_hits:
                    self.previous_hits.remove(removal)
            elif direction == 2:
                removal = [last[0]+i, last[1]]
                if removal in self.previous_hits:
                    self.previous_hits.remove(removal)
            elif direction == 3:
                removal = [last[0], last[1]+i]
                if removal in self.previous_hits:
                    self.previous_hits.remove(removal)


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
