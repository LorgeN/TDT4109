from sekantmetoden import f, g, differentiate


def secant_method(x0, x1, func, tol):
    x_vals = [x0, x1]

    i = 0
    while abs(func(x_vals[-1])) > tol:
        x = x_vals[i]
        x1 = x_vals[i + 1]
        x_vals.append(x1 - func(x1) * (differentiate(x1, x, func) ** -1))
        i += 1

    return x_vals[-1]


def execute_print(x0, x1, func, tol):
    x_val = secant_method(x0, x1, func, tol)
    print(
        f"Funksjonen nærmer seg et nullpunkt når x = {format(x_val, '.2f')}, da er f(x) = {format(func(x_val), '.2e')}")


if __name__ == '__main__':
    execute_print(11, 13, f, 0.00001)
    execute_print(1, 2, g, 0.00001)
    execute_print(0, 1, g, 0.00001)
