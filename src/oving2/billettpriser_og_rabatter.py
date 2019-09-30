# Minipris: 199,-
# Vanlig pris: 440,-
#
# Minipris dersom dager igjen er >= 14
# Minipris kan ikke refunderes, tilby vanlig pris også
#
# Vanlig pris, rabatter:
# under 16 = 50%
# 60+, militær i unform = 25%
# Student: * 0.75
#
# Minipris, rabatter:
# Student: 10%
EARLY_BIRD_RATE = 199
NORMAL_RATE = 440


def ask_boolean_question(question):
    return input(question + " (J/N)").upper() == "J"


def calculate_discount_normal():
    multiplier = 1.0

    age = int(input("Alder: "))
    if age < 16:
        multiplier = 0.5
    elif age >= 60:
        multiplier = 0.75
    elif ask_boolean_question("Er du militær i uniform?"):
        multiplier = 0.75

    if ask_boolean_question("Er du student?"):
        multiplier *= 0.75

    return multiplier


def calculate_discount_mini():
    multiplier = 1.0

    if ask_boolean_question("Er du student?"):
        multiplier = 0.9

    return multiplier


days_left = int(input("Hvor mange dager er det til du skal reise? "))
if days_left >= 14:
    print("Du kvalifiserer for MINIPRIS! Denne er på " + str(EARLY_BIRD_RATE) + ",- (Før rabatter)")
    print("Minipris kan ikke refunderes/endres")
    if ask_boolean_question("Ønskes dette?"):
        discount_rate = calculate_discount_mini()
        print("Prisen på din billett blir: " + str(EARLY_BIRD_RATE * discount_rate) + ",-")
        exit(0)

print("Normal pris er på " + str(NORMAL_RATE) + ",- (Før rabatter)")
discount_rate = calculate_discount_normal()
print("Prisen på din billett blir: " + str(NORMAL_RATE * discount_rate) + ",-")
