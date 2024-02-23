# *****************************
# SUMA DE LA DIAGONAL PRINCIPAL
# *****************************


def run(matrix: list) -> int:
    # TU CÓDIGO AQUÍ
    sum_diagonal = 0
    for line in matrix:
        if len(line) != sum_diagonal:
            None
    for i in range(sum_diagonal):
        sum_diagonal += matrix[i][i]

    return sum_diagonal


if __name__ == '__main__':
    run([[4, 6, 1], [2, 9, 3], [1, 7, 7]])