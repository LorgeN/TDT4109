from sekantmetoden import f


def differentiate(x_k: float, x_k1: float, func) -> float:
    return (func(x_k) - func(x_k1)) / (x_k - x_k1)


if __name__ == '__main__':
    print(f"{differentiate(9, 10, f)}")
