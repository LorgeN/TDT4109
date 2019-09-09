import math


def calculate_discriminator(a_val, b_val, c_val):
    return (b_val ** 2) - (4 * a_val * c_val)


def find_solution_area(discriminator_val):
    if discriminator_val < 0:
        return "to imaginære løsninger"

    if discriminator_val > 0:
        return "to reelle løsninger"

    return "én reell dobbeltrot"


a = int(input("A-verdi: "))
b = int(input("B-verdi: "))
c = int(input("C-verdi: "))

print("Ligning: " + str(a) + "x^2 + " + str(b) + "x + " + str(c))

discrim = calculate_discriminator(a, b, c)

print("Det eksisterer " + find_solution_area(discrim))

if discrim < 0:
    exit(0)

if discrim == 0:
    solution = -b / (2 * a)
    print("Løsning: x = " + str(solution))
    exit(0)

sqrt_discrim = math.sqrt(discrim)
solution_1 = (-b + sqrt_discrim) / (2 * a)
solution_2 = (-b - sqrt_discrim) / (2 * a)

print("Løsninger: x = " + str(solution_1) + " V x = " + str(solution_2))