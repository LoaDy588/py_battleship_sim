import random


def create_field():
    field = []
    for y in range(10):
        line = []
        for x in range(10):
            line.append({"content": "water", "hit": False, "ship": None})
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


def create_center():
    return "test"


def create_shiplist():
    shiplist = []
    shiplist.append({
        "name": "carrier",
        "length": 5
    })
    shiplist.append({
            "name": "battleship",
            "length": 4
    })
    shiplist.append({
        "name": "cruiser",
        "length": 3
    })
    shiplist.append({
        "name": "submarine",
        "length": 3
    })
    shiplist.append({
        "name": "destroyer",
        "length": 2
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
    orientations = []
    for i in range(4):
        for j in range(length):
            if i == 0:
                if coords[0]-j > 9 or coords[0]-j < 0:
                    break
                else:
                    pass
                if field[coords[0]-j][coords[1]]["content"] == "water":
                    pass
                else:
                    break
            elif i == 1:
                if coords[1]-j > 9 or coords[1]-j < 0:
                    break
                else:
                    pass
                if field[coords[0]][coords[1]-j]["content"] == "water":
                    pass
                else:
                    break
            elif i == 2:
                if coords[0]+j > 9 or coords[0]+j < 0:
                    break
                else:
                    pass
                if field[coords[0]+j][coords[1]]["content"] == "water":
                    pass
                else:
                    break
            elif i == 3:
                if coords[1]+j > 9 or coords[1]+j < 0:
                    break
                else:
                    pass
                if field[coords[0]][coords[1]+j]["content"] == "water":
                    pass
                else:
                    break
            if j == length-1:
                orientations.append(i)
    return orientations


def place_ship(field, ship):
    length = ship["length"]
    coords = ship["coords"]
    for i in range(length):
        if ship["orientation"] == 0:
            field[coords[0]-i][coords[1]]["content"] = "ship"
            field[coords[0]-i][coords[1]]["ship"] = ship["name"]
        elif ship["orientation"] == 1:
            field[coords[0]][coords[1]-i]["content"] = "ship"
            field[coords[0]][coords[1]-i]["ship"] = ship["name"]
        if ship["orientation"] == 2:
            field[coords[0]+i][coords[1]]["content"] = "ship"
            field[coords[0]+i][coords[1]]["ship"] = ship["name"]
        elif ship["orientation"] == 3:
            field[coords[0]][coords[1]+i]["content"] = "ship"
            field[coords[0]][coords[1]+i]["ship"] = ship["name"]
    return field
