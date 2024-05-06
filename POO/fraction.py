from __future__ import annotations


class Fraction:
    def __init__(self, num: int, den: int):
        self.num = num
        self.den = den

    def __add__(self, other: Fraction):
        new_num = (self.num * self.den) + (self.den * self.num)
        new_den = (self.den * self.den)
        return f'{new_num} / {new_den}'

    def __sub__(self, other: Fraction):
        new_num = (self.num * self.den) - (self.den * self.num)
        new_den = (self.den * self.den)
        return f'{new_num} / {new_den}'

    def __mul__(self, other: Fraction):
        new_num = (self.num * self.num)
        new_den = (self.den * self.den)
        return f'{new_num} / {new_den}'

    def __truediv__(self, other: Fraction):
        new_num = (self.num * self.den)
        new_den = (self.den * self.num)
        return f'{new_num} / {new_den}'
    def __str__(self):
        

    @staticmethod
    def gcd(a: int, b: int) -> int:
        '''Euclid's Algorithm'''
        while b > 0:
            a, b = b, a % b
        return a
