import re

INPUT_VALIDATION = re.compile("[0-9]+")


def define_word():
    global secret
    secret = input("Skriv inn det hemmelige ordet:")


def define_life_count():
    global life_count
    life_str = input("Skriv inn antall tillatte feil: ")

    if not INPUT_VALIDATION.match(life_str):
        print("Ugyldig input! Skriv inn et tall")
        define_life_count()
        return

    life_count = int(life_str)


define_word()
define_life_count()
