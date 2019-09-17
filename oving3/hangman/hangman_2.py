# Copy from hangman_1
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

# End of copy

given_guesses = []


def print_word():
    output = ""
    for i in range(len(secret)):
        output += secret[i] if state_list[i] else "*"
    print(output)


def attempt_guess(char: str) -> bool:
    global state_list
    if char in given_guesses:
        print("Du har allerede gjettet denne bokstaven før!")
        if not fail_guess():
            return False
        print_word()
        return True

    given_guesses.append(char)

    correct = False
    for i in range(len(secret)):
        if not secret[i] == char:
            continue
        state_list[i] = True
        correct = True

    if correct:
        for val in state_list:
            if not val:
                print("Korrekt! Bokstaven", char, " er i ordet!")
                print_word()
                return True
        print("Gratulerer! Du har greid å gjette hele ordet!")
        return False

    print("Feil! Bokstaven", char, "er ikke i ordet!")
    return fail_guess()


def fail_guess() -> bool:
    global life_count
    life_count -= 1
    if life_count == 0:
        print("Du har brukt opp livene dine!")
        print("Riktig ord var", secret)
        return False

    print("Du har", life_count, "liv igjen")
    return True


state_list = [False] * len(secret)

while True:
    char_input = input("Gjett på en bokstav i ordet: ")
    if not len(char_input) == 1:
        print("Ugyldig input! Vennligst skriv inn en bokstav.")
        continue
    if not attempt_guess(char_input):
        break
