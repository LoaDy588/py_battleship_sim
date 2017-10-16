import random


def create_field():
    field = []
    for y in range(10):
        line = []
        for x in range(10):
            line.append({"content": "water", "hit": False, "shipID": None})
        field.append(line)
    return field


def create_random():
    field = create_field()
    shiplist = create_shiplist()
    for ship in shiplist:
        coords, orientations = find_empty_space(field, ship["length"])
        orientation = orientations[random.randint(0, len(orientations)-1)]
        ship["coords"] = coords
        ship["orientation"] = orientation
        field = place_ship(field, ship)
    return field, shiplist


def create_outside():
    return "test"


def create_cluster():
    return "test"


def create_human_like():
    return "foobar"


def create_shiplist():
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


def find_empty_space(field, length):
    while True:
        x = random.randint(0, 9)
        y = random.randint(0, 9)
        if field[x][y]["content"] == "ship":
            continue
        else:
            coords = [x, y]
            orientations = find_possible_orientations(field, coords, length)
            if len(orientations) == 0:
                continue
            else:
                return coords, orientations


def find_possible_orientations(field, coords, length):
    orientations = [(-1, 0), (0, -1), (1, 0), (0, 1)]
    possible = []
    for vctr in orientations:
        for i in range(length):
            position = []
            position.append(coords[0]+i*vctr[0])
            position.append(coords[1]+i*vctr[1])
            if position[0] > 9 or position[1] > 9:
                break
            if position[0] < 0 or position[1] < 0:
                break
            if not field[position[0]][position[1]]["content"] == "water":
                break
            if i == length-1:
                possible.append(vctr)
    return possible


def place_ship(field, ship):
    length = ship["length"]
    coords = ship["coords"]
    orientation = ship["orientation"]
    for i in range(length):
        position = []
        position.append(coords[0]+i*orientation[0])
        position.append(coords[1]+i*orientation[1])
        field[position[0]][position[1]]["content"] = "ship"
        field[position[0]][position[1]]["shipID"] = ship["id"]
    return field


def get_neighbors(coords):
    neighbors = []
    directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]
    for vector in directions:
        if coords[0]+vector[0] > 9 or coords[1]+vector[1] > 9:
            directions.remove(vector)
        elif coords[0]+vector[0] < 0 or coords[1]+vector[1] < 0:
            directions.remove(vector)
    for vector in directions:
        neighbor = []
        x = coords[0] + vector[0]
        y = coords[1] + vector[1]
        neighbor.append(x)
        neighbor.append(y)
        neighbors.append(neighbor)
    return neighbors
