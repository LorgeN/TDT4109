def f(x):
    return 3 + x ** 2


def trapezoid(func, a, b, n):
    h = (b - a) / n

    val = func(a) / 2

    for index in range(1, n):
        val += func(a + index * h)

    val += func(b) / 2

    return h * val


print(f"{trapezoid(f, 0, 3, 4)}")
