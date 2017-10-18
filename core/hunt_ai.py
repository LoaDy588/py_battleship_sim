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
            self.hunt(enemy)
        elif self.mode == "target":
            self.target(enemy)

    def hunt(self, enemy):
        if len(self.hit_list) > 1:
            coords = self.hit_list[random.randint(0, len(self.hit_list)-1)]
        elif len(self.hit_list) == 1:
            coords = self.hit_list[0]
        else:
            self.hit_list = regen_hit_list(self.enemy_field)
            coords = self.hit_list[random.randint(0, len(self.hit_list)-1)]
        self.enemy_field[coords[0]][coords[1]]["hit"] = True
        ship_hit, ship_sunk, ship_length = enemy.hit(coords)
        self.hit_list.remove(coords)
        if ship_hit:
            self.enemy_field[coords[0]][coords[1]]["content"] = "ship"
            self.previous_hits[0] = coords
            self.mode = "target"

    def target(self, enemy):
        self.create_targets()
        if len(self.target_list) > 1:
            coords = self.target_list[random.randint(0, len(self.target_list)-1)]
        elif len(self.target_list) == 0:
            self.mode = "hunt"
            self.target_list = []
            self.previous_hits = [None]
            return
        else:
            coords = self.target_list[0]
        self.enemy_field[coords[0]][coords[1]]["hit"] = True
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

    def create_targets(self):
        targets = []
        for hit in self.previous_hits:
            neighbors = field_utils.get_neighbors(hit)
            for neighbor in neighbors:
                targets.append(neighbor)
        targets_clean1 = []
        for target in targets:
            if target not in targets_clean1:
                targets_clean1.append(target)
        for target in targets_clean1:
            if target in self.previous_hits:
                targets_clean1.remove(target)
        targets_clean2 = []
        for target in targets_clean1:
            if not self.enemy_field[target[0]][target[1]]["hit"]:
                targets_clean2.append(target)
        self.target_list = targets_clean2

    def cleanup_ship(self, length):
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
        for i in range(length):
            removal = [last[0]+i*direction[0], last[1]+i*direction[1]]
            if removal in self.previous_hits:
                self.previous_hits.remove(removal)


def regen_hit_list(field):
    ships = []
    for x in range(10):
        for y in range(10):
            if field[x][y]["content"] == "ship":
                ships.append([x, y])
    hit_list = []
    for ship in ships:
        neighbors = field_utils.get_neighbors(ship)
        for neighbor in neighbors:
            if neighbor not in hit_list:
                hit_list.append(neighbor)
    for hit in hit_list:
        if field[hit[0]][hit[1]]["hit"]:
            hit_list.remove(hit)
    return hit_list
