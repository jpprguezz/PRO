from __future__ import annotations


class Date:
    def __init__(self, day: int, month: int, year: int):
        """Validar día, mes y año. Se comprobará si la fecha es correcta
        (entre el 1-1-1900 y el 31-12-2050); si el día no es correcto, lo pondrá a 1;
        si el mes no es correcto, lo pondrá a 1; y si el año no es correcto, lo pondrá a 1900.
        Ojo con los años bisiestos.
        El 1-1-1900 fue lunes.
        """
        self.day = day
        self.month = month
        self.year = year

        if self.day > 31:
            self.day = 1
        else:
            self.day
        if self.month > 12:
            self.month = 1
        else:
            self.month
        if self.year > 2500:
            self.year = 1900
        else:
            self.year

    @staticmethod
    def is_leap_year(year: int) -> bool:
        """Indica si un año es bisiesto"""
        return year % 4 == 0

    @staticmethod
    def get_days_in_month(month: int, year: int) -> int:
        """Número de días en un determinado mes de un determinado año"""
        ...

    def get_delta_days(self) -> int:
        """Número de días transcurridos desde el 1-1-1900 hasta la fecha"""
        ...

    @property
    def weekday(self) -> int:
        """Día de la semana de la fecha (0 para domingo, ..., 6 para sábado)."""
        ...

    @property
    def is_weekend(self) -> bool:
        """Indica si la fecha del objeto actual cae en fin de semana"""
        ...

    @property
    def short_date(self) -> str:
        """02/09/2003"""
        ...

    def __str__(self):
        """Formato: MARTES 2 DE SEPTIEMBRE DE 2003"""
        ...

    def __add__(self, days: int) -> Date:
        """Sumar un número de días a la fecha"""
        ...

    def __sub__(self, other: Date | int) -> int | Date:
        """Dos opciones:
        1) Restar una fecha a otra fecha -> Número de días
        2) Restar un número de días la fecha -> Nueva fecha"""
        ...

    def __lt__(self, other) -> bool:
        """Indica si la fecha del objeto actual es menor que la fecha de other"""
        ...

    def __gt__(self, other) -> bool:
        """Indica si la fecha del objeto actual es mayor que la fecha de other"""
        ...

    def __eq__(self, other) -> bool:
        """Indica si la fecha del objeto actual es igual que la fecha de other"""
        ...
