import math


def f(x: float) -> float:
    return (x - 12) * math.exp(x / 2) - 8 * ((x + 2) ** 2)


def g(x: float) -> float:
    return -x - 2 * (x ** 2) - 5 * (x ** 3) + 6 * (x ** 4)


if __name__ == '__main__':
    print(f"f(0) = {f(0)}, g(1) = {g(1)}")
