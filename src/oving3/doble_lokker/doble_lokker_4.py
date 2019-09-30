import random
import re
import math

INPUT_VALIDATION = re.compile("[0-9]+")

factor1 = 0
factor2 = 0
attemptIndex = 0
correctStreak = 0


def generator_factors():
    global factor1
    global factor2

    index = math.floor(correctStreak / 5) + 1

    factor1 = random.randint(0, index * 5)
    factor2 = random.randint(0, index * 5)


def validate_product(val):
    return val == (factor1 * factor2)


def attempt_answer(val):
    global attemptIndex
    global correctStreak
    if validate_product(val):
        attemptIndex = 0
        correctStreak += 1
        print("Rett svar! Du har", str(correctStreak), ("rett" if correctStreak == 1 else "rette") + " svar på rad")
        ask_next_question()
    else:
        attemptIndex += 1
        if attemptIndex == 3:
            correctStreak = 0
            failed_answer()
        else:
            print("Feil svar! Du har " + str(3 - attemptIndex) + " forsøk igjen.")
            await_input()


def failed_answer():
    print("Å nei! Du er tom for forsøk.")
    ask_next_question()


def ask_next_question():
    response = input("Vil du ha et nytt spørsmål? (J/N)")
    if response.upper() == "J":
        next_question()


def next_question():
    generator_factors()
    print(factor1, "*", factor2, "= ?")
    await_input()


def await_input():
    input_str = input("Skriv inn et tall: ")
    if not INPUT_VALIDATION.match(input_str):
        print("Ugyldig input!")
        await_input()
        return

    int_val = int(input_str)
    attempt_answer(int_val)


next_question()
