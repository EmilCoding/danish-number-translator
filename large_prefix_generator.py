import itertools
from typing import Generator


ONES_PREFIXES = {
    1: 'un',
    2: 'duo',
    3: 'tre',
    4: 'quattuor',
    5: 'quin',
    6: 'se',
    7: 'septen',
    8: 'octo',
    9: 'noven',
}
TENS_PREFIXES = {
    10: 'deci',
    20: 'viginti',
    30: 'triginti',
    40: 'quadraginti',
    50: 'quinquaginti',
    60: 'sexaginti',
    70: 'septuaginti',
    80: 'octoginti',
    90: 'nonaginti',
}
SMALL_NUMBER_PREFIXES = (
    'Mi', 'Bi', 'Tri', 'Kvarti', 'Kvinti', 'Seksti', 'Septi', 'Okti', 'Noni',
)


def prefix_generator(longform: bool = True) -> Generator[tuple[int, str], None, None]:
    """Generator the prefixes for number names in long form"""
    
    base10exponent = 6
    for degree in range(1, 1000):
        prefix = prefix_below_degree_1000_short_form(degree)

        # Yield n-illion
        yield base10exponent, f"{prefix}llion"
        base10exponent += 3

        # Yield n-illiard
        if longform:
            yield base10exponent, f"{prefix}lliard"
            base10exponent += 3


def prefix_below_degree_10_short_form(degree: int) -> str:
    return SMALL_NUMBER_PREFIXES[degree - 1]


def prefix_below_degree_100_short_form(degree: int) -> str:
    if degree < 10:
        return SMALL_NUMBER_PREFIXES[degree - 1]

    tens, ones = divmod(degree, 10)
    return ("" if ones == 0 else ONES_PREFIXES[ones]) + TENS_PREFIXES[10*tens]


def prefix_below_degree_1000_short_form(degree: int) -> str:
    if degree < 100:
        return prefix_below_degree_100_short_form(degree)

    hundrets, rest = divmod(degree, 100)
    hundrets_part = ("" if hundrets == 1 else ONES_PREFIXES[hundrets]) + "centillion"
    ones_part = "" if rest == 0 else prefix_below_degree_100_short_form(rest)
    return ones_part + hundrets_part


if __name__ == '__main__':
    for n, name in prefix_generator():
        print(f"10e{n}: {name}")
