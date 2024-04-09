# *****************
# NÚMEROS PERFECTOS
# *****************


def is_perfect(n: int) -> bool:
    if n % 2 == 0:
        return True
    else:
        return False


def own_number(n: int) -> bool:
    if n % n == 0:
        return True
    else:
        return False
