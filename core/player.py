from . import field_utils


class Player:
    def __init__(self):
        self.field, self.shiplist = field_utils.create_random()

    def hit(self, coords):
        x = coords[0]
        y = coords[1]
        self.field[x][y]["hit"] = True
        if self.field[x][y]["content"] == "ship":
            ship_id = self.field[x][y]["shipID"]
            ship_sunk = check_ship(self.field, self.shiplist[ship_id])
            return True, ship_sunk
        else:
            return False, False

    def has_lost(self):
        ship_status = []
        for ship in self.shiplist:
            ship_status.append(check_ship(self.field, ship))
        if sum(ship_status) == 5:
            return True
        else:
            return False

    def get_field(self):
        return self.field

    def get_shiplist(self):
        return self.shiplist


def check_ship(field, ship):
    x = ship["coords"][0]
    y = ship["coords"][1]
    orientation = ship["orientation"]
    hit_list = []
    for i in range(ship["length"]):
        if orientation == 0:
            hit_list.append(field[x-i][y]["hit"])
        elif orientation == 1:
            hit_list.append(field[x][y-i]["hit"])
        elif orientation == 2:
            hit_list.append(field[x+i][y]["hit"])
        elif orientation == 3:
            hit_list.append(field[x][y+i]["hit"])
    if sum(hit_list) == ship["length"]:
        return True
    else:
        return False
