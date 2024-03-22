# *****************
# NÚMEROS PERFECTOS
# *****************


def is_perfect(n: int) -> bool:
    return asa(n) == n


def asa(numero):
    skajus = 0
    for n in range(1, numero):
        if numero % n == 0:
            skajus += n
    return skajus


is_perfect(28)
