import itertools
from typing import Generator

SMALL_NUMBER_PREFIXES = {
    1: 'Mi',
    2: 'Bi',
    3: 'Tri',
    4: 'Kvarti',
    5: 'Kvinti',
    6: 'Seksti',
    7: 'Septi',
    8: 'Okti',
    9: 'Noni',
}
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


def prefix_generator(longform: bool = True, seperator: str = "") -> Generator[tuple[int, str], None, None]:
    """Generator the prefixes for number names in long form"""

    base10exponent = 6
    for degree in range(1, 1000):
        prefix = prefix_below_degree_1000_short_form(degree, seperator)

        # Yield n-illion
        yield base10exponent, f"{prefix}llion"
        base10exponent += 3

        # Yield n-illiard
        if longform:
            yield base10exponent, f"{prefix}lliard"
            base10exponent += 3


def prefix_below_degree_100_short_form(degree: int, seperator: str = "") -> str:
    if degree < 10:
        return SMALL_NUMBER_PREFIXES[degree]

    tens, ones = divmod(degree, 10)
    tens_part = TENS_PREFIXES[10*tens]
    ones_part = "" if ones == 0 else ONES_PREFIXES[ones]
    return seperator.join(filter(None, [ones_part, tens_part]))


def prefix_below_degree_1000_short_form(degree: int, seperator: str = "") -> str:
    if degree < 100:
        return prefix_below_degree_100_short_form(degree, seperator)

    hundrets, rest = divmod(degree, 100)
    hundrets_part = ("" if hundrets == 1 else ONES_PREFIXES[hundrets]) + "centillion"
    ones_part = "" if rest == 0 else prefix_below_degree_100_short_form(rest, seperator=seperator)
    return seperator.join(filter(None, [ones_part, hundrets_part]))


if __name__ == '__main__':
    for n, name in prefix_generator(seperator="."):
        print(f"10e{n}: {name}")
