import math


def is_prime(number: int) -> bool:
    # Speedup
    if number == 2:
        return True

    # Check if even number
    if number % 2 == 0 or number <= 1:
        return False

    i = 3
    # No prime will be found beyond the sqrt of the number so no need to check
    while (i * i) <= number:
        if number % i == 0:
            return False
        # Skip even numbers
        i += 2

    return True


def find_primes(max_val: int) -> list:
    primes = []

    if max_val >= 2:
        primes.append(2)

    min_val = 3
    for i in range(min_val, max_val + 1):
        if not is_prime(i):
            continue
        primes.append(i)

    return primes


def find_factors(number: int) -> list:
    factors = []

    remaining = number

    while remaining != 1:
        if is_prime(remaining):
            factors.append(remaining)
            break

        for prime in find_primes(int(math.sqrt(remaining))):
            div = remaining / prime
            if not div.is_integer():
                continue
            factors.append(prime)
            remaining = int(div)
            break

    return factors


value = int(input("Skriv inn et positivt heltall: "))
if is_prime(value):
    print(str(value) + " er et primtall")
else:
    valueFactors = find_factors(value)
    factorized = str(value) + " = " + str(valueFactors[0])

    for factor in valueFactors[1:len(valueFactors)]:
        factorized += "*" + str(factor)

    print(factorized)
