# ********************
# MÁXIMO COMÚN DIVISOR
# ********************


def gcd(a: int, b: int) -> int:
    if b == 0:
        (a, b) = a
    else:
        r = (a / b) % 2
    return int((a, b) * (b, r))
