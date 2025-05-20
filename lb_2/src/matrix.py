import math
import random


def generate_weight_matrix(size: int, symmetric: bool = False, max_weight: int = 100):
    matrix = [[0] * size for _ in range(size)]

    for i in range(size):
        for j in range(size):
            if i == j:
                matrix[i][j] = math.inf
            elif symmetric and j > i:
                weight = random.randint(1, max_weight)
                matrix[i][j] = weight
                matrix[j][i] = weight
            elif not symmetric and j != i:
                matrix[i][j] = random.randint(1, max_weight)
    return matrix

def print_matrix(matrix):
    for row in matrix:
        print(" ".join(str(x).ljust(5) if x != math.inf else "∞    " for x in row))


def write_matrix_to_file(matrix, filename):
    copy_matrix = [row.copy() for row in matrix]
    for i in range(len(copy_matrix)):
        copy_matrix[i][i] = -1
    with open(filename, 'w') as f:
        for row in copy_matrix:
            f.write(' '.join(map(str, row)) + '\n')


def read_matrix_from_file(filename):
    matrix = []
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
        if not lines:
            raise ValueError("Файл пустой")
        for line in lines:
            if line.strip():
                matrix.append(list(map(float, line.strip().split())))
    for i in range(len(matrix)):
        matrix[i][i] = math.inf
    return matrix

