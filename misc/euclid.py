class EuclidPart:
    def __init__(self, count: int, quotient: int, remainder: int):
        self.value = count * quotient + remainder
        self.count = count
        self.quotient = quotient
        self.remainder = remainder


def find_gcd(a: int, m: int) -> list:
    parts = []

    remainder = m
    quotient = a

    while remainder > 0:
        count = remainder // quotient
        remainder %= quotient
        part = EuclidPart(count, quotient, remainder);
        parts.append(part)
        if remainder == 0:
            break

        remainder = part.quotient
        quotient = part.remainder

    return parts


def format_part(part: EuclidPart) -> str:
    return f"{part.value} = {part.count} * {part.quotient} + {part.remainder}"


def compute_print(a: int, m: int):
    parts_found = find_gcd(a, m)

    for current_part in parts_found:
        print(format_part(current_part))

    print(f"gcd({a_in}, {m_in}) = {parts_found[len(parts_found) - 1].quotient}")


a_in = int(input("a = "))
m_in = int(input("m = "))

compute_print(a_in, m_in)
