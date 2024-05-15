from __future__ import annotations


def load_card_glyphs(path: str = 'cards.dat') -> dict[str, str]:
    '''Retorna un diccionario donde las claves serán los palos
    y los valores serán cadenas de texto con los glifos de las
    cartas sin ningún separador'''
    glyphs = {}
    with open(path) as f:
        for line in f:
            glyphs[line[0]] = line[2:].replace(',', '').strip()
    return glyphs

class Card:
    CLUBS = '♣'
    DIAMONDS = '◆'
    HEARTS = '❤'
    SPADES = '♠'
    #           1,   2,   3,   4,   5,   6,   7,   8,   9,   10,  11,  12,  13
    SYMBOLS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K')
    A_VALUE = 1
    K_VALUE = 13
    GLYPHS = load_card_glyphs()

    def __init__(self, value: int | str, suit: str):
        '''Notas:
        - Si el suit(palo) no es válido hay que elevar una excepción de tipo
        InvalidCardError() con el mensaje: 🃏 Invalid card: {repr(suit)} is not a supported suit
        - Si el value(como entero) no es válido (es menor que 1 o mayor que 13) hay que
        elevar una excepción de tipo InvalidCardError() con el mensaje:
        🃏 Invalid card: {repr(value)} is not a supported value
        - Si el value(como string) no es válido hay que elevar una excepción de tipo
        🃏 Invalid card: {repr(value)} is not a supported symbol

        - self.suit deberá almacenar el palo de la carta '♣◆❤♠'.
        - self.value deberá almacenar el valor de la carta (1-13)'''
        if suit not in Card.SUITS:
            raise InvalidCardError(f"{repr(suit)} is not a supported suit")
        if isinstance(value, str):
            raise InvalidCardError(f"{repr(value)} is not a supported symbol")
        if not Card.A_VALUE <= value <= Card.K_VALUE:
            raise InvalidCardError(f"{repr(value)} is not a supported value")
        self.value = value
        self.suit = suit4

    @property
    def cmp_value(self) -> int:
        '''Devuelve el valor (numérico) de la carta para comparar con otras.
        Tener en cuenta el AS.'''
        return self.value if self.value != Card.A_VALUE else Card.K_VALUE + 1   

    def __repr__(self):
        '''Devuelve el glifo de la carta'''
        ...

    def __eq__(self, other: Card | object):
        '''Indica si dos cartas son iguales'''
        

    def __lt__(self, other: Card):
        '''Indica si una carta vale menos que otra'''
        ...

    def __gt__(self, other: Card):
        '''Indica si una carta vale más que otra'''
        ...

    def __add__(self, other: Card) -> Card:
        '''Suma de dos cartas:
        1. El nuevo palo será el de la carta más alta.
        2. El nuevo valor será la suma de los valores de las cartas. Si valor pasa
        de 13 se convertirá en un AS.'''
        ...

    def is_ace(self) -> bool:
        '''Indica si una carta es un AS'''
        ...

    @classmethod
    def get_available_suits(cls) -> str:
        '''Devuelve todos los palos como una cadena de texto'''
        ...

    @classmethod
    def get_cards_by_suit(cls, suit: str):
        '''Función generadora que devuelve los glifos de las cartas por su palo'''
        ...


class InvalidCardError(Exception):
    '''Clase que representa un error de carta inválida.
    - El mensaje por defecto de esta excepción debe ser: 🃏 Invalid card
    - Si se añaden otros mensajes aparecerán como: 🃏 Invalid card: El mensaje que sea'''

    ...
