import numpy as np


def are_orthogonal(vector_a: list, vector_b: list) -> bool:
    return np.dot(np.array(vector_a), np.array(vector_b)) == 0
