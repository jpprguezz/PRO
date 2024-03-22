# ************************************
# CALCULANDO EL FACTORIAL DE UN NÚMERO
# ************************************


def factorial(n):
    if n < 0:
        return None
    fact = 1
    for n in range(1, n + 1):
        fact *= n
    return fact
