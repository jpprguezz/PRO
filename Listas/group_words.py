# ******************
# AGRUPANDO PALABRAS
# ******************


def run(words: list) -> dict:
    group_words = {}
    for word in words:
        initial_letter = word[0]
        if initial_letter not in group_words:
            group_words[initial_letter] = []
        group_words[initial_letter].append(word)

    return group_words


if __name__ == '__main__':
    run(['mesa', 'móvil', 'barco', 'coche', 'avión', 'bandeja', 'casa', 'monitor', 'carretera', 'arco'])