"""
Contains utilites for creating and working with battleship game fields.

field, ship, shiplist returns/arguments are always standard format.
For standard formats, check wiki.


GENERATION METHODS:
create_field - creates empty field
create_random - creates field randomly filled with ships
create_shiplist - creates shiplist
generate_cheat_list - generates cheat list

UTILITY METHODS:
find_empty_space_random - finds random empty space in specified field
find_possible_orientations - finds possible orientation
                             for a ship of specified length and origin
find_highest - finds points with highest values in probability field
place_ship - places specified ship in the specified field
get_neighbors - returns list of neighbors of specified fied coord

Oldřich Pecák(LoaDy588), 2017
"""
import random


def create_field():
    """Return empty field."""
    field = []
    for y in range(10):
        line = []
        for x in range(10):
            # add dictionary with default values
            line.append({"content": "water",
                         "hit": False,
                         "shipID": None})
        field.append(line)
    return field


def create_random():
    """Return randomly filled field and shiplist."""
    # create empty field and basic shiplist
    field = create_field()
    shiplist = create_shiplist()
    # place every ship from shiplist in the field
    for ship in shiplist:
        coords, orientations = find_empty_space_random(field, ship["length"])
        # pick random from possible orientations of ship
        orientation = orientations[random.randint(0, len(orientations)-1)]
        # write position values to the ship dictionary
        ship["coords"] = coords
        ship["orientation"] = orientation

        field = place_ship(field, ship)
    return field, shiplist


def create_shiplist():
    """Return shiplist."""
    shiplist = []
    shiplist.append({
        "name": "carrier",
        "length": 5,
        "id": 0
    })
    shiplist.append({
        "name": "battleship",
        "length": 4,
        "id": 1
    })
    shiplist.append({
        "name": "cruiser",
        "length": 3,
        "id": 2
    })
    shiplist.append({
        "name": "submarine",
        "length": 3,
        "id": 3
    })
    shiplist.append({
        "name": "destroyer",
        "length": 2,
        "id": 4
    })
    return shiplist


def find_empty_space_random(field, length):
    """
    Find random empty space for a ship.

    ARGUMENTS:
    field - field in which to find space
    length - length of the ship we want to find space for in format int(length)

    RETURNS(tuple):
    coords - coords of the empty space(origin point of ship) in format [x, y]
    orientations - list of possible orientation vectors
    """
    while True:
        # create random coords
        x = random.randint(0, 9)
        y = random.randint(0, 9)
        # if space occupied, skip cycle and start again
        if field[x][y]["content"] == "ship":
            continue
        else:
            coords = [x, y]
            orientations = find_possible_orientations(field, coords, length)
            # if no possible orientations, skip cycle and star again
            if len(orientations) == 0:
                continue
            else:
                return coords, orientations


def find_possible_orientations(field, coords, length):
    """
    Find possible orientations for a ship.

    ARGUMENTS:
    field - field in which to find orientations
    coords - origin coords of ship in format  [x, y]
    length - length of ship in format int(length)

    RETURNS:
    list of possible orientations(each orientation characterized by vector)
    """
    orientations = [(-1, 0), (0, -1), (1, 0), (0, 1)]
    possible = []
    # for every possible orientation
    for vctr in orientations:
        # if outside the field, skip to next orientation
        if coords[0]+(length-1)*vctr[0] > 9 or coords[1]+(length-1)*vctr[1] > 9:
            continue
        if coords[0]+(length-1)*vctr[0] < 0 or coords[1]+(length-1)*vctr[1] < 0:
            continue
        # for length of the ship
        for i in range(length):
            position = []
            position.append(coords[0]+i*vctr[0])
            position.append(coords[1]+i*vctr[1])
            # if current position occupied, skip to next orientation
            if not field[position[0]][position[1]]["content"] == "water":
                break

            # if length unnoccupied, add vector to possible orientations list
            if i == length-1:
                possible.append(vctr)
    return possible


def place_ship(field, ship):
    """
    Place ship in a field.

    ARGUMENTS:
    field - a field in which to place the ship
    ship - the ship to place

    RETURNS:
    field with the ship placed
    """
    length = ship["length"]
    coords = ship["coords"]
    orientation = ship["orientation"]
    # for every spot occupied by ship, edit field to reflect this
    for i in range(length):
        position = []
        position.append(coords[0]+i*orientation[0])
        position.append(coords[1]+i*orientation[1])
        field[position[0]][position[1]]["content"] = "ship"
        field[position[0]][position[1]]["shipID"] = ship["id"]
    return field


def get_neighbors(coords):
    """
    Find neighbors of coord in a field.

    ARGUMENTS:
    coords - in format [x, y]

    RETURNS:
    list of neighbors, where each neighbor has format [x, y]
    """
    neighbors = []
    directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]

    # for every direction, get neighbor coords, append to list
    for vector in directions:
        neighbor = []
        x = coords[0] + vector[0]
        y = coords[1] + vector[1]
        neighbor.append(x)
        neighbor.append(y)
        if neighbor[0] > 9 or neighbor[1] > 9:
            continue
        if neighbor[0] < 0 or neighbor[1] < 0:
            continue
        neighbors.append(neighbor)
    return neighbors


def check_ship(field, ship):
    """
    Check if ship has been sunk.

    ARGUMENTS:
    field - the field with ship to check
    ship - ship to check

    RETURNS:
    True/False boolean, True if ship has been sunk.
    """
    x = ship["coords"][0]
    y = ship["coords"][1]
    orientation = ship["orientation"]
    hit_list = []
    for i in range(ship["length"]):
        hit_list.append(field[x+i*orientation[0]][y+i*orientation[1]]["hit"])
    if sum(hit_list) == ship["length"]:
        return True
    else:
        return False


def find_highest(probab_field):
    """
    Find the points with highest value in probabilty field.

    Returns list with 1 or more tuples of coordinates.

    ARGUMENTS:
    probab_field - probability field, expects 10x10 array of int values
    """
    # default to (0. 0) and 0 value
    current = [(0, 0)]
    current_value = 0

    # step through the whole field
    for x in range(10):
        for y in range(10):

            # if higher value, rewrite list to contain this point, update value
            if probab_field[x][y] > current_value:
                current = [(x, y)]
                current_value = probab_field[x][y]

            # if same value, append this point to list
            elif probab_field[x][y] == current_value:
                current.append((x, y))

    return current


def generate_cheat_list(field, n):
    """
    Create cheat list.

    Returns list with specified number of tuples of coordinates, which
    contain ship based on specified field.

    ARGUMENTS:
    field - field from which to create cheat_list
    n - number of points to return, min 1, max - number of ships in field
    """
    cheat_list = []
    ship_dict = {}
    for x in range(10):
        for y in range(10):
            if field[x][y]["content"] == "ship":
                if field[x][y]["shipID"] in ship_dict.keys():
                    ship_dict[field[x][y]["shipID"]].append((x, y))
                else:
                    ship_dict[field[x][y]["shipID"]] = [(x, y)]
    for i in range(n):
        temp = ship_dict.pop(random.choice(list(ship_dict.keys())))
        if len(temp) == 1:
            cheat_list.append(temp[0])
        else:
            cheat_list.append(temp[random.randint(0, len(temp)-1)])
    return cheat_list
