from random import randint


def random_matrix(width: int, height: int) -> list:
    return [[randint(0, 10) for x in range(width)] for y in range(height)]


def print_matrix(matrix: list, name: str):
    if matrix is None:
        return

    lines = '\n  '.join(map(str, matrix))
    print(f"{name}=[\n  {lines}\n]")


def add_matrices(matrix_a: list, matrix_b: list):
    if not len(matrix_a) == len(matrix_b):
        print("Matrisene er ikke av samme dimensjon")
        return None

    if len(matrix_a) == 0:
        return []

    # We assume that the 2nd dimension is uniform
    if not len(matrix_a[0]) == len(matrix_b[0]):
        print("Matrisene er ikke av samme dimensjon")
        return None

    height = len(matrix_a)
    width = len(matrix_a[0])

    return [[(matrix_a[x][y] + matrix_b[x][y]) for y in range(width)] for x in range(height)]


def main():
    A = random_matrix(4, 3)
    print_matrix(A, 'A')

    B = random_matrix(3, 4)
    print_matrix(B, 'B')

    C = random_matrix(3, 4)
    print_matrix(C, 'C')

    D = add_matrices(A, B)
    print_matrix(D, 'A+B')

    E = add_matrices(B, C)
    print_matrix(E, 'B+C')


if __name__ == '__main__':
    main()
