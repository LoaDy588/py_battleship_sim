import random
from . import player
from . import field_utils


class Probabilistic_AI(player.Player):

    def __init__(self):
        player.Player.__init__(self)
        self.__enemy_field = field_utils.create_field()
        self.__enemy_shiplist = field_utils.create_shiplist()

        for x in range(10):
            for y in range(10):
                self.__enemy_field[x][y]["sunk"] = False

    def turn(self, oponnent):
        coords = self.__generate_target()
        self.__enemy_field[coords[0]][coords[1]]["hit"] = True
        ship_hit, ship_sunk, length = oponnent.hit(coords)
        if ship_hit:
            self.__enemy_field[coords[0]][coords[1]]["content"] = "ship"
        if ship_sunk:
            self.__sink_ship(coords, length)
            for ship in self.__enemy_shiplist:
                if ship["length"] == length:
                    self.__enemy_shiplist.remove(ship)
                    break

    def __generate_target(self):
        probability = self.__create_probab_field()
        target = find_highest(probability)
        if len(target) == 1:
            return target[0]
        else:
            return target[random.randint(0, len(target)-1)]

    def __create_probab_field(self):
        possible_points = self.__generate_possible_points()
        probab_field = [[0 for y in range(10)] for x in range(10)]
        for ship in self.__enemy_shiplist:
            for point in possible_points:
                orientations, bonus = self.__find_orientations(point, ship["length"])
                for index, orientation in enumerate(orientations):
                    self.__add_to_field(probab_field, orientation, bonus[index],
                                       point, ship["length"])
        return probab_field

    def __find_orientations(self, coords, length):
        possible = []
        possible_bonus = []
        vectors = ((1, 0), (0, 1), (-1, 0), (0, -1))
        for vctr in vectors:
            # if outside the field, skip to next orientation
            if coords[0]+length*vctr[0] > 9 or coords[1]+length*vctr[1] > 9:
                continue
            if coords[0]+length*vctr[0] < 0 or coords[1]+length*vctr[1] < 0:
                continue
            temp = []
            bonus = False
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
        for i in range(length):
            pointer = (point[0]+i*direction[0], point[1]+i*direction[1])
            if not self.__enemy_field[pointer[0]][pointer[1]]["hit"]:
                if bonus:
                    probab_field[pointer[0]][pointer[1]] += 100
                else:
                    probab_field[pointer[0]][pointer[1]] += 1

    def __generate_possible_points(self):
        possible = []
        for x in range(10):
            for y in range(10):
                pointer = self.__enemy_field[x][y]
                if pointer["content"] == "water" and not pointer["hit"]:
                    possible.append((x, y))
                elif pointer["content"] == "ship" and not pointer["sunk"]:
                    possible.append((x, y))
        return possible

    def __sink_ship(self, coords, length):
        vectors = ((1, 0), (0, 1), (-1, 0), (0, -1))
        direction = ()
        for vctr in vectors:
            # if outside the field, skip to next orientation
            if coords[0]+length*vctr[0] > 9 or coords[1]+length*vctr[1] > 9:
                continue
            if coords[0]+length*vctr[0] < 0 or coords[1]+length*vctr[1] < 0:
                continue
            temp = []
            for i in range(length):
                pointer = self.__enemy_field[coords[0]+i*vctr[0]][coords[1]+i*vctr[1]]
                if pointer["content"] == "ship" and not pointer["sunk"]:
                    temp.append(pointer["hit"])
            if sum(temp) == length:
                direction = vctr
                break
        if direction == ():
            return
        for i in range(length):
            removal = (coords[0]+i*direction[0], coords[1]+i*direction[1])
            self.__enemy_field[removal[0]][removal[1]]["sunk"] = True


def find_highest(probab_field):
    current = [(0, 0)]
    current_value = 0
    for x in range(10):
        for y in range(10):
            if probab_field[x][y] > current_value:
                current = [(x, y)]
                current_value = probab_field[x][y]
            elif probab_field[x][y] == current_value:
                current.append((x, y))
    return current
