# *************************
# PRIMER ELEMENTO DUPLICADO
# *************************


def run(numbers: list) -> int:
    # TU CÓDIGO AQUÍ
    fdup = 0
    for number in numbers:
        if number in numbers:
            fdup.remove()
        else:
            -1
    return fdup


if __name__ == '__main__':
    run([2, 3, 5, 3, 2])
