"""Danish number-name translation utilities.

This module provides functions to translate non-negative integers into
Danish words. The public entry point is ``get_name``, which accepts
values up to the supported maximum and optional formatting settings.

The implementation uses Danish short-scale naming for numbers below one
million and Danish long-scale power names for larger values.
"""
from typing import Unpack
from danishnumbers.positive_integer import check_bounds, is_positive_integer
from danishnumbers.format import FormatOptions, set_default_values_option
from danishnumbers.large_prefix_generator import ExponentDegreeTooHigh, prefix_generator


class NumberTooBig(Exception):
    """Exception raised when a number is larger than the supported range."""

    def __init__(self, n: int) -> None:
        super().__init__(f"Cannot handle a make a {n.bit_count()} bit number")


SMALL_DANISH_NUMBERS: dict[int, str] = {
    0: 'nul',
    1: 'en',
    2: 'to',
    3: 'tre',
    4: 'fire',
    5: 'fem',
    6: 'seks',
    7: 'syv',
    8: 'otte',
    9: 'ni',
    10: 'ti',
    11: 'elleve',
    12: 'tolv',
    13: 'tretten',
    14: 'fjorten',
    15: 'femten',
    16: 'seksten',
    17: 'sytten',
    18: 'atten',
    19: 'nitten',
}
"""Dictionary containing the danish names of non-negative integers below 20."""

DANISH_TENS: dict[int, str] = {
    10: 'ti',
    20: 'tyve',
    30: 'tredive',
    40: 'fyrre',
    50: 'halvtreds',
    60: 'tres',
    70: 'halvfjerds',
    80: 'firs',
    90: 'halvfems',
}
"""Dictionary containing the danish names of the small multiples of 10."""


@set_default_values_option
def danish_number_name(n: int, **options: Unpack[FormatOptions]) -> str:
    if not (0 == n or is_positive_integer(n)):
        raise ValueError('`n` must be a non-negative integer.')
    if n == 0:
        return SMALL_DANISH_NUMBERS[0]

    remainding, segment = divmod(n, 1_000_000)
    parts_of_word_reverse_order = [danish_names_below_a_million(segment, **options), ]
    try:
        for _, prefix in prefix_generator(True, in_prefix_seperator=options['in_prefix_separator']):
            if remainding == 0:
                break
            remainding, segment = divmod(remainding, 1_000)
            match segment:
                case 0:
                    pass
                case 1:
                    parts_of_word_reverse_order.append(options['separator'].join(["En", prefix]))
                case int():
                    parts_of_word_reverse_order.append(
                        options['separator'].join([danish_names_below_1000(segment, **options), prefix])
                    )
    except ExponentDegreeTooHigh:
        raise NumberTooBig(n)

    return options['separator'].join(parts_of_word_reverse_order[::-1])


@set_default_values_option
@check_bounds(max_value=1_000_000)
def danish_names_below_a_million(n: int, **options: Unpack[FormatOptions]) -> str:
    if n < 1_000:
        return danish_names_below_1000(n, **options)
    if options['group_hundreds_and_thousands_digit'] and n < 10_000:
        return danish_names_below_10_000_grouped(n, **options)

    parts: list[str] = []
    thousands, rest = divmod(n, 1_000)
    # Get name of thousands
    if thousands == 1 and options['et_before_tusinde']:
        parts.append('et')
    else:
        parts.append(danish_names_below_1000(thousands, **options))
    parts.append('tusinde')

    # Get name of hundreds
    if rest == 0:
        pass
    elif rest < 100:
        parts += ['og', danish_names_below_1000(rest, **options)]
    else:
        parts.append(danish_names_below_1000(rest, **options))

    return options['separator'].join(parts)


@check_bounds(max_value=10_000, min_value=1_000)
def danish_names_below_10_000_grouped(n: int, **options: Unpack[FormatOptions]) -> str:
    """Get danish name of number in interval [1000, 10000) with hundrets and thousands digits grouped together."""
    hundrets, rest = divmod(n, 100)

    parts: list[str] = []
    if 0 == hundrets % 10:  # Clean thousands
        parts += [danish_names_below_10(hundrets // 10, **options), "tusinde"]
    else:
        parts += [danish_names_below_100(hundrets, **options), "hundrede"]

    if rest > 0:
        parts += [danish_names_below_100(rest, **options)]

    return options['separator'].join(parts)


@set_default_values_option
@check_bounds(max_value=1_000)
def danish_names_below_1000(n: int, **options: Unpack[FormatOptions]) -> str:
    """Return the danish name for a number below 1000.

    Args:
        n (int): Number to be translated.

    Kwargs:
        separator (str, optional): Separator between segments or word.
          Eg. if separator is '-' the 21 is "en-og-tyve". Defaults to "".
        et_before_hundrede (bool, optional): If True, "et" if put in front of single digit hundreds
          Eg. 117 becomes "et-hundrede-og-sytten" insted of "hundrede-og-sytten". Defaults to True.

    Returns:
        str: Name of the number ´n´ in danish.
    """
    if n < 100:
        return danish_names_below_100(n, **options)
    parts: list[str] = []
    hundreds, rest = divmod(n, 100)

    # Add hundrets part
    if hundreds == 1 and options['et_before_hundrede']:
        parts.append('et')
    elif hundreds > 1:
        parts.append(danish_names_below_10(hundreds, **options))
    parts.append("hundrede")

    # Add tens parts
    if rest > 0:
        parts += ['og', danish_names_below_100(rest, **options)]

    return options['separator'].join(parts)


@set_default_values_option
@check_bounds(max_value=100)
def danish_names_below_100(n: int, **options: Unpack[FormatOptions]) -> str:
    """Return the danish name of a positive integer below 100.

    Args:
        n (int): Number to be translated.
        separator (str, optional): Separator between segments or word.
          Example if separator is '-' the 21 is "en-og-tyve". Defaults to "".

    Returns:
        str: Danish name of a number below 1_000.
    """
    if n < 20:
        return danish_names_below_20(n, **options)
    if (name := DANISH_TENS.get(n, None)):
        return name
    tens, ones = divmod(n, 10)
    return options['separator'].join([danish_names_below_10(ones, **options), "og", DANISH_TENS[10*tens]])


@set_default_values_option
@check_bounds(max_value=20)
def danish_names_below_20(n: int, **options: Unpack[FormatOptions]) -> str:
    """Return the danish name of a positive integer below 20."""
    return SMALL_DANISH_NUMBERS[n]


@set_default_values_option
@check_bounds(max_value=10)
def danish_names_below_10(n: int, **options: Unpack[FormatOptions]) -> str:
    """Return the danish name of a positive integer below 10."""
    return SMALL_DANISH_NUMBERS[n]


if __name__ == '__main__':
    for n in range(20):
        value = 2**(2**n)
        print(f"{n}: {value}: {danish_number_name(value, separator="")}")
    print(f"{danish_number_name(1_000_000_001)=}")
