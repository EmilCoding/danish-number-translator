"""Generate prefix names for large number magnitudes.

This module supports Danish-style long-form prefixes for large numbers,
producing names such as ``million``, ``milliard``, ``billion``,
``billiard``, and beyond. The public generator yields exponent/prefix
pairs for powers of ten in the long form.
"""

import itertools
from typing import Generator


class DegreeTooHigh(Exception):
    base10exponent: int

    def __init__(self, base10exponent: int) -> None:
        self.base10exponent = base10exponent
        super().__init__(f"Number 10**({base10exponent}) is too large to handle")


SMALL_NUMBER_PREFIXES = {
    1: 'mi',
    2: 'bi',
    3: 'tri',
    4: 'kvarti',
    5: 'kvinti',
    6: 'seksti',
    7: 'septi',
    8: 'okti',
    9: 'noni',
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


def prefix_generator(longform: bool = True, in_prefix_seperator: str = "") -> Generator[tuple[int, str], None, None]:
    """Yield long-form number suffixes for increasingly large powers of ten.

    The generator returns tuples of ``(exponent, suffix)`` where the exponent
    is a power of ten (for example, 6 for million, 9 for milliard, 12 for
    billion, etc.) and the suffix is the corresponding name.

    Args:
        longform (bool): If True, include the ``-illiard`` variant after each
            ``-illion`` name. If False, generate only ``-illion`` names.
        in_prefix_seperator (str): String inserted between prefix components when
            composing compound names.

    Raises:
        DegreeTooHigh: When limit of prefix has been reached.

    Yields:
        tuple[int, str]: Exponent and full suffix name for the power of ten.
    """
    base10exponent = 6
    try:
        for degree in itertools.count(1):
            prefix = _prefix_below_degree_1000_short_form(degree, in_prefix_seperator)

            # Yield n-illion
            yield base10exponent, f"{prefix}llion"
            base10exponent += 3

            # Yield n-illiard
            if longform:
                yield base10exponent, f"{prefix}lliard"
                base10exponent += 3
    except AssertionError:
        raise DegreeTooHigh(base10exponent)


def _prefix_below_degree_1000_short_form(degree: int, in_prefix_seperator: str = "") -> str:
    """Build a short-form prefix for numbers 10^{3n + 3} with n from 1 to 999.

    For degrees 100 and above, this helper includes the ``centillion`` base
    portion and any additional tens/ones prefix for the remainder.

    Args:
        degree (int): The numeric degree to convert, between 1 and 999.
        in_prefix_seperator (str): Separator inserted between prefix fragments.

    Returns:
        str: The composed short-form prefix for the degree.
    """
    assert isinstance(degree, int) and 0 < degree < 1000, "Degree must be a positive integer under 1000."
    if degree < 100:
        return _prefix_below_degree_100_short_form(degree, in_prefix_seperator)

    hundrets, rest = divmod(degree, 100)
    hundrets_part = ("" if hundrets == 1 else ONES_PREFIXES[hundrets]) + "centillion"
    ones_part = "" if rest == 0 else _prefix_below_degree_100_short_form(rest, in_prefix_seperator)
    return in_prefix_seperator.join(filter(None, [ones_part, hundrets_part]))


def _prefix_below_degree_100_short_form(degree: int, in_prefix_seperator: str = "") -> str:
    """Build a short-form prefix for numbers 10^{3n + 3} with n from 1 to 99.

    Examples include ``Mi`` for 1, ``Duodeci`` for 12, and ``Septuaginti`` for
    70. This helper produces the prefix portion used before ``-illion``.

    Args:
        degree (int): The numeric degree to convert, between 1 and 99.
        in_prefix_seperator (str): Separator inserted between prefix fragments.

    Returns:
        str: The composed short-form prefix.
    """
    assert isinstance(degree, int) and 0 < degree < 100, "Degree must be a positive integer under 100."
    if degree < 10:
        return SMALL_NUMBER_PREFIXES[degree]

    tens, ones = divmod(degree, 10)
    tens_part = TENS_PREFIXES[10*tens]
    ones_part = "" if ones == 0 else ONES_PREFIXES[ones]
    return in_prefix_seperator.join(filter(None, [ones_part, tens_part]))


if __name__ == '__main__':
    try:
        for n, name in prefix_generator(in_prefix_seperator="."):
            print(f"10e{n}: {name}")
    except DegreeTooHigh as error:
        assert error.base10exponent == 6000, f"{error.base10exponent}"
