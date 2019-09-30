import re

INPUT_VALIDATION = re.compile("[0-9]+")


def alternating_sum(n):
    multiplier = 1
    total = 0
    for i in range(1, n + 1):
        total += multiplier * (i ** 2)
        multiplier *= -1
    return total


str_in = input("n = ")
if not INPUT_VALIDATION.match(str_in):
    print("Ugyldig input! Skriv inn et tall")
else:
    value = alternating_sum(int(str_in))
    print(f"Summen av tallserien er {value}!")
