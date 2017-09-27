def display_field(field):
    print("_|O|1|2|3|4|5|6|7|8|9|")
    for x in field:
        print(str(field.index(x))+"|", end="")
        for y in x:
            if y["content"] == "ship":
                print("x", end=" ")
            else:
                print("o", end=" ")
        print()
