
class field_generator:
    def get_field(self):
        field = []
        for x in range(10):
            line = []
            for y in range(10):
                line.append([x, y])
            field.append(line)
        return field


test = field_generator()
print(test.get_field())
