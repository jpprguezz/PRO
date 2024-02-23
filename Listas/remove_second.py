# *************************
# NO ME INTERESAN LOS PARES
# *************************


def run(items: list) -> list:
    # TU CÓDIGO AQUÍ
    filter = [elemento for i, elemento in enumerate(items) if i % 2 == 0]

    return filter


if __name__ == '__main__':
    run([1, 2, 1, 2, 1, 2])