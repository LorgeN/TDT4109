import re

INPUT_VALIDATION = re.compile("[0-9]+")


class SumData:
    def __init__(self, alternating_sum: int, iteration: int):
        self.alternating_sum = alternating_sum
        self.iteration = iteration


def alternating_sum_with_max(max_val: int) -> SumData:
    value = SumData(0, 0)

    multiplier = -1
    next_value = 1
    while next_value <= max_val:
        value.iteration += 1
        value.alternating_sum = next_value

        next_value = next_value + (multiplier * ((value.iteration + 1) ** 2))
        multiplier *= -1

    return value


str_in = input("k = ")
if not INPUT_VALIDATION.match(str_in):
    print("Ugyldig input! Skriv inn et tall")
else:
    sum_info = alternating_sum_with_max(int(str_in))
    print(f"Summen av tallene før summen blir større enn k er {sum_info.alternating_sum}."
          f" Antall iterasjoner: {sum_info.iteration}")
