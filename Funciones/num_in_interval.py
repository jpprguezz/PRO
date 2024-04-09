# *******************
# NÚMERO EN INTERVALO
# *******************


def in_range(value: int, lower_limit: int, upper_limit: int) -> bool:
    if value in range(lower_limit, upper_limit + 1):
        return True
    else:
        return False
