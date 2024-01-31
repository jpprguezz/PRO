# ******************
# TUPLAS Y CONJUNTOS
# ******************


def run(input: tuple) -> set:
    # TU CÓDIGO AQUÍ
    output = set()
    scnd_part = set()

    for item in input:
        output.add(item[0])
        scnd_part.add(item[1])

    output = set() 

    
    return output


if __name__ == '__main__':
    run(((4, 3), (8, 2), (7, 5), (8, 2), (9, 1)))