# *********************************
# SEPARANDO MAYÚSCULAS Y MINÚSCULAS
# *********************************


def split_case(words: list) -> list:
    lower_words = []
    upper_word = []
    for word in words:
        if word.isupper():
            upper_word.append(word)
        if word.islower():
            lower_words.append(word)
    return lower_words, upper_word
