from . import player, field_utils


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
        ship_hit, ship_sunk, length = oponnent.hit(coords)
        if ship_hit and not ship_sunk:
            self.__enemy_field[coords[0]][coords[1]]["hit"] = True
        elif ship_hit and ship_sunk:
            self.__enemy_field[coords[0]][coords[1]]["hit"] = True
            self.__enemy_field = sink_ship(self.__enemy_field, coords, length)
            for ship in self.__enemy_shiplist:
                if ship["length"] == length:
                    self.__enemy_shiplist.remove(ship)
                    break

    def __generate_target(self):
        probability = self.__create_probab_field()
        target = find_highest(probability)
        return target


    def __create_probab_field(self):
        possible_points = generate_possible_points(self.__enemy_field)
        probab_field = [[0 for x in range(10)] for x in range(10)]
        for ship in self.__enemy_shiplist:
            for point in possible_points:
                orientations = find_orientations(point, ship["length"])
                for orientation in orientations:
                    add_to_field(probab_field, orientation, point, ship["length"])


def __add_to_field(self, field, direction, point, length):
    for i in range(length):
        pointer = (point[0]+i*direction[0], point[1]+i*direction[1])



def generate_possible_points(field):
    possible = []
    for x in range(10):
        for y in range(10):
            if field[x][y]["content"] == "water" and not field[x][y]["hit"]:
                possible.append((x, y))
            elif field[x][y]["content"] == "ship" and not field[x][y]["sunk"]:
                possible.append((x, y))
    return possible


def sink_ship(field, coords, length):
    directions = ((0, 0), (0, 1), (-1, 0), (0, -1))
    direction = ()
    for direc in directions:
        temp = []
        for i in range(length):
            pointer = field[coords[0]+i*direc[0]][coords[1]+i*[direc[1]]]
            if not pointer["sunk"]:
                temp.append(pointer["hit"])
        if sum(temp) == length:
            direction = direc
            break

    for i in range(length):
        removal = (coords[0]+i*direction[0], coords[1]+i*direction[1])
        field[removal[0]][removal[1]]["sunk"] = True
