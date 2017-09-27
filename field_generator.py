import random


class field_generator:
    def create_field(self):
        field = []
        for x in range(10):
            line = []
            for y in range(10):
                line.append({"content": None})
            field.append(line)
        return field

    def create_random(self):
        field = self.create_field()
        for i in range(10):
            x = random.randint(0, 9)
            y = random.randint(0, 9)
            print(x, y)
            field[x][y] = {"content": "ship"}
        return field

    def create_outside(self):
        return "test"

    def create_center(self):
        return "test"

    def create_shiplist(self):
        return "test"


test = field_generator()
display.display_field(test.create_random())
