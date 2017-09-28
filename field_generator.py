import random
import display


class field_generator:
    def create_field(self):
        field = []
        for y in range(10):
            line = []
            for x in range(10):
                line.append({"content": "water", "hit": False})
            field.append(line)
        return field

    def create_random(self):
        field = self.create_field()
        shiplist = self.create_shiplist()
        
        return field, shiplist

    def create_outside(self):
        return "test"

    def create_center(self):
        return "test"

    def create_shiplist(self):
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


test = field_generator()
field, shiplist = test.create_random()
display.display_field(field)
print(shiplist)
