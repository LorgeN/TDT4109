class FibonacciSequence:
    def __init__(self) -> None:
        self.values = []


def compute_fibonacci_sequence(size: int) -> FibonacciSequence:
    if size < 0:
        raise ValueError(f"Size must be >= 0! Was {size}!")

    sequence = FibonacciSequence()

    for i in range(size + 1):
        if i <= 1:
            sequence.values.append(i)
            continue

        sequence.values.append(sequence.values[i - 1] + sequence.values[i - 2])

    return sequence


def compute_sum(sequence: FibonacciSequence) -> int:
    total = 0

    for val in sequence.values:
        total += val

    return total


input_str = input("k = ")
if not input_str.isdigit():
    print(f"Ugyldig input {input_str}! Vennligst skriv inn et tall")
else:
    k_value = int(input_str)
    fib_seq = compute_fibonacci_sequence(k_value)
    fib_sum = compute_sum(fib_seq)
    print(f"Summen av fibonaccitallene opp til {k_value} er {fib_sum}. Sekvensen er {fib_seq.values}")
