"""Generate prefix names for large number magnitudes.

This module supports Danish-style long-form prefixes for large numbers,
producing names such as ``million``, ``milliard``, ``billion``,
``billiard``, and beyond. The public generator yields exponent/prefix
pairs for powers of ten in the long form.
"""
from typing import Generator
from danishnumbers.positive_integer import check_bounds


SMALL_EXPONENT_PREFIXES: dict[int, str] = {
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
"""Prefixed for short form exponents of degree 1 to 9."""


TENS_DIGIT_EXPONENT_PREFIXES: dict[int, str] = {
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
"""Prefixed for short form exponents of degrees that are multiples of ten."""


SINGLE_DIGIT_EXPONENT_PREFIXES: dict[int, str] = {
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
"""Prefixes for ones digit in short form exponents of degree larger than 10."""


class ExponentDegreeTooHigh(StopIteration):
    """Degree of exponent is too big to be named under current rules."""
    base10exponent: int

    def __init__(self, base10exponent: int) -> None:
        self.base10exponent = base10exponent
        super().__init__(f"Number 10**({base10exponent}) is too large to handle")


def prefix_generator(
    longform: bool = True,
    in_prefix_seperator: str = "",
    conjugate_large_powers: bool = True,
    strict: bool = False,
) -> Generator[tuple[int, str], None, None]:
    """Yield long-form number prefixes for increasingly large powers of ten.

    The generator returns tuples of ``(exponent, suffix)`` where the exponent
    is a power of ten (for example, 6 for million, 9 for milliard, 12 for
    billion, etc.) and the prefix is the corresponding name.

    Args:
        longform (bool, optional): If True, include the ``-illiard`` variant after each
            ``-illion`` name. If False, generate only ``-illion`` names. Default is True.
        in_prefix_seperator (str, optional): String inserted between prefix components when
            composing compound names. Default is "".
        strict (bool, optional): If True, and expection is raised when limits has been reached.
          Default is False.

    Raises:
        ExponentDegreeTooHigh: When limit of prefix has been reached.

    Yields:
        tuple[int, str]: Exponent and full suffix name for the power of ten.
    """
    base10exponent = 6
    for degree in range(1, 1_000):
        prefix = exponent_prefix_shortform_below_1000(degree, in_prefix_seperator)

        # Yield n-illion
        yield base10exponent, f"{prefix}llion"
        base10exponent += 3

        # Yield n-illiard
        if longform:
            yield base10exponent, f"{prefix}lliard"
            base10exponent += 3


@check_bounds(max_value=1_000)
def exponent_prefix_shortform_below_1000(degree: int, in_prefix_seperator: str = "") -> str:
    """Build a short-form prefix for numbers 10^{3n + 3} with n from 1 to 999.

    For degrees 100 and above, this helper includes the ``centillion`` base
    portion and any additional tens/ones prefix for the remainder.

    Args:
        degree (int): The numeric degree to convert, between 1 and 999.
        in_prefix_seperator (str): Separator inserted between prefix fragments.

    Returns:
        str: The composed short-form prefix for the degree.
    """
    if degree < 100:
        return exponent_prefix_shortform_below_100(degree, in_prefix_seperator)

    parts: list[str] = []
    hundrets, rest = divmod(degree, 100)

    # Add hundreds part
    if 1 == hundrets:
        parts.append("centi")
    else:
        parts += [SINGLE_DIGIT_EXPONENT_PREFIXES[hundrets], "centi"]

    # Add rest parts
    if rest > 0:
        parts.append(exponent_prefix_shortform_below_100(rest, in_prefix_seperator))

    return in_prefix_seperator.join(parts)


@check_bounds(max_value=100)
def exponent_prefix_shortform_below_100(degree: int, in_prefix_seperator: str = "") -> str:
    """Build a short-form prefix for numbers 10^{3n + 3} with n from 1 to 99.

    Examples include ``Mi`` for 1, ``Duodeci`` for 12, and ``Septuaginti`` for
    70. This helper produces the prefix portion used before ``-illion``.

    Args:
        degree (int): The numeric degree to convert, between 1 and 99.
        in_prefix_seperator (str): Separator inserted between prefix fragments.

    Returns:
        str: The composed short-form prefix.
    """
    if degree < 10:
        return SMALL_EXPONENT_PREFIXES[degree]

    parts: list[str] = []
    tens, ones = divmod(degree, 10)

    # Add ones part
    if ones > 0:
        parts.append(SINGLE_DIGIT_EXPONENT_PREFIXES[ones])
    parts.append(TENS_DIGIT_EXPONENT_PREFIXES[10*tens])  # Add tens part

    return in_prefix_seperator.join(parts)


if __name__ == '__main__':
    import time
    for n, name in prefix_generator(in_prefix_seperator="."):
        print(f"10e{n}: {name}")
        time.sleep(0.01)
