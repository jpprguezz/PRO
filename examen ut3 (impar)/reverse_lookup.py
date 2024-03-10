# ********************
# CLAVES DESDE VALORES
# ********************


def run(items: dict, target_value: int) -> tuple:
    # TU CÓDIGO AQUÍ
    source_keys = []
    for item in items.keys():
        if items.get(item) == target_value:
            source_keys.append(item)
    source_keys = tuple(source_keys)


    return source_keys


if __name__ == '__main__':
    run({'A': 1, 'B': 2, 'C': 3, 'D': 3, 'E': 4}, 3)
