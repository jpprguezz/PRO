# ******************************
# VALORES IGUALES EN DICCIONARIO
# ******************************


def run(items: dict) -> bool:
    # TU CÓDIGO AQUÍ
    all_same = bool()
    for item in items:
        if item == items.values():
            True
        if item != items.values():
            False

    return all_same


if __name__ == '__main__':
    run({'a': 1, 'b': 1, 'c': 1, 'd': 1})