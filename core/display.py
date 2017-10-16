"""
Display utilites for battleship fields.

METHODS:
display_field - displays field
print_point - internal method, should not be used outside

Oldřich Pecák(LoaDy588), 2017
"""
import os


def display_field(field):
    """
    Display field in console.

    ARGUMENTS:
    field - field to display, expects standard format
    """
    os.system('cls' if os.name == 'nt' else 'clear')     # clear console
    print("/|0|1|2|3|4|5|6|7|8|9|")     # print top row
    # step through the field and display every point
    for y in range(10):
        print(str(y)+"|", end="")   # print begging of line/row
        for x in range(10):
            print_point(field[x][y])
        print()


def print_point(data):
    """INTERNAL FUNCTION."""
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
