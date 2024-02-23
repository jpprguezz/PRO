# ******************
# AGRUPANDO PALABRAS
# ******************


def run(words: list) -> dict:
    # TU CÓDIGO AQUÍ
    group_words = {}
    for word in words:
        initial_word = word[0]
        if initial_word not in group_words:
            group_words[initial_word] = [word]
        else:
            group_words[initial_word].append(word)

    return group_words


if __name__ == '__main__':
    run(['mesa', 'móvil', 'barco', 'coche', 'avión', 'bandeja', 'casa', 'monitor', 'carretera', 'arco'])