import math


def f(x):
    return 8 + 1 / 3 * math.sin(x)


prev_val = f(0.33)
for i in range(2):
    prev_val = f(prev_val)

print(f"{prev_val}")
