# *****************
# ALFABETO CIRCULAR
# *****************

def get_alphabet(num_letters: int):
    for n in range(num_letters):
        yield n


def run(max_letters: int) -> str:
    ALPHABET = 'abcdefghijklmnñopqrstuvwxyz'  
    text = ''
    for num in get_alphabet(max_letters):
        text += ALPHABET[num % len(ALPHABET)]
    return text


if __name__ == '__main__':
    run(0)