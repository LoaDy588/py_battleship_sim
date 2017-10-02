def display_field(field):
    print("/|0|1|2|3|4|5|6|7|8|9|")
    for y in range(10):
        print(str(y)+"|", end="")
        for x in range(10):
            print_point(field[x][y])
        print()


def print_point(data):
    if data["content"] == "ship":
        if not data["hit"]:
            print("\u25a0", end=" ")
        if data["hit"]:
            print("\u2613", end=" ")
    elif data["content"] == "water":
        if not data["hit"]:
            print(" ", end=" ")
        if data["hit"]:
            print("\u00b7", end=" ")
