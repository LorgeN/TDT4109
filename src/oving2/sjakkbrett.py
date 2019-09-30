import re

INPUT_VALIDATION = re.compile("[A-Ha-h][0-8]")


def parse_slot_color(position):
    x_pos = ord(list(position)[0]) % 2
    y_pos = int(position[1]) % 2

    if x_pos == 0:
        if y_pos == 0:
            return "Svart"
        else:
            return "Hvit"

    if y_pos == 0:
        return "Hvit"
    else:
        return "Svart"


pos = input("Posisjon: ")
if not INPUT_VALIDATION.match(pos):
    print("Ugyldig input!")
    exit(0)

color = parse_slot_color(pos)
print("Farge: ", color)
