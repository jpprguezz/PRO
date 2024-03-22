# *******************************
# DECORANDO CON VALORES ABSOLUTOS
# *******************************


def fabs(func):
    def wrapper(a: int, b: int) -> int:
        a = abs(a)
        b = abs(b)
        result = func(a, b)

    return wrapper


@fabs
def fprd(num1, num2):
    return num1 * num2
