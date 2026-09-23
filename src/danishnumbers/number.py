"""Danish number-name translation utilities.

This module provides functions to translate non-negative integers into
Danish words. The public entry point is ``get_name``, which accepts
values up to the supported maximum and optional formatting settings.

The implementation uses Danish short-scale naming for numbers below one
million and Danish long-scale power names for larger values.
"""
from typing import Any, TypedDict, Unpack
from danishnumbers.positive_integer import check_bounds
from danishnumbers.large_prefix_generator import DegreeTooHigh, prefix_generator


class NumberTooBig(Exception):
    """Exception raised when a number is larger than the supported range."""

    def __init__(self, n: int) -> None:
        super().__init__(f"Cannot handle a make a {n.bit_count()} bit number")


class FormatOptions(TypedDict):
    """Formatting options used throughout Danish number translation."""
    longform: bool
    separator: str
    in_prefix_separator: str
    et_before_hundrede: bool
    et_before_tusinde: bool


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



def danish_number_name(n: int, **__: Any) -> str:
    ...


@check_bounds(max_value=1_000_000)
def danish_names_below_a_million(n: int, **__: Any) -> str:
    ...


@check_bounds(max_value=1_000)
def danish_names_below_1000(
    n: int,
    separator: str = "",
    et_before_hundrede: bool = True,
    **__: Any
) -> str:
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
    parts: list[str] = []
    hundreds, rest = divmod(n, 100)

    # Add hundrets part
    if hundreds == 0:
        pass
    elif hundreds == 1 and et_before_hundrede:
        parts.append('et')
    else:
        parts.append(danish_names_below_10(hundreds))
    parts.append("hundrede")

    # Add tens parts
    if rest > 0:
        parts += ['og', danish_names_below_100(rest, separator)]

    return separator.join(parts)


@check_bounds(max_value=100)
def danish_names_below_100(n: int, separator: str = "", **__: Any) -> str:
    """Return the danish name of a positive integer below 100.

    Args:
        n (int): Number to be translated.
        separator (str, optional): Separator between segments or word.
          Example if separator is '-' the 21 is "en-og-tyve". Defaults to "".

    Returns:
        str: Danish name of a number below 1_000.
    """
    if n < 20:
        return danish_names_below_20(n)
    if (name := DANISH_TENS.get(n, None)):
        return name
    tens, ones = divmod(n, 10)
    return separator.join([danish_names_below_10(ones), "og", DANISH_TENS[10*tens]])


@check_bounds(max_value=20)
def danish_names_below_20(n: int, **__: Any) -> str:
    """Return the danish name of a positive integer below 20."""
    return SMALL_DANISH_NUMBERS[n]


@check_bounds(max_value=10)
def danish_names_below_10(n: int, **__: Any) -> str:
    """Return the danish name of a positive integer below 10."""
    return SMALL_DANISH_NUMBERS[n]

















def with_default_options(func):
    """Wrap a translator so default format options are applied.

    This decorator exposes a normal function signature with explicit defaults
    while internally converting those values into a shared ``FormatOptions``
    typed dict for downstream helper functions.
    """
    def caller(
        n: int,
        /,
        separator="",
        in_prefix_separator="",
        longform=True,
        et_before_hundrede=True,
        et_before_tusinde=True,
    ) -> str:
        options: FormatOptions = {
            "longform": True,
            "separator": separator,
            "in_prefix_separator": in_prefix_separator,
            "et_before_hundrede": et_before_hundrede,
            "et_before_tusinde": et_before_tusinde,
        }
        return func(n, **options)
    return caller


@with_default_options
def get_name(n: int, **options: Unpack[FormatOptions]) -> str:
    """Return the Danish name of a non-negative integer.

    Args:
        n (int): The number to translate. Must be non-negative.
        seperator (str): Separator used to join Danish word parts.
        et_before_hundred (bool): Include ``et`` before ``hundrede`` for 100-199.
        et_before_thousands (bool): Include ``et`` before ``tusind`` for 1000.

    Raises:
        NumberTooBig: If the number cannot be represented with the supported
            power names.

    Returns:
        str: The Danish word representation of ``n``, title-cased.
    """
    assert isinstance(n, int) and n >= 0, "Given number must be a non-negative integer"
    if n == 0:
        return SMALL_DANISH_NUMBERS[n]

    remainding, segment = divmod(n, 1_000_000)
    parts_of_word_reverse_order = [_below_a_million(segment, **options), ]

    try:
        for _, prefix in prefix_generator(options['longform'], options['in_prefix_separator']):
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
    except DegreeTooHigh:
        raise NumberTooBig(n)

    return options['separator'].join(parts_of_word_reverse_order[::-1]).title()


@with_default_options
def _below_a_million(n: int, **options: Unpack[FormatOptions]) -> str:
    """Return the Danish word form of a non-negative integer below a million."""
    assert isinstance(n, int) and 0 <= n < 1_000_000, "Given number must be an integer between 0 and one million."
    thousands, rest = divmod(n, 1_000)

    match thousands:
        case 0:
            thousands_part = ""
        case 1:
            thousands_part = f"et{options['separator']}tusind" if options['et_before_tusinde'] else "tusind"
        case int():
            thousands_part = options['separator'].join([danish_names_below_1000(thousands, **options), "tusinde"])

    if rest == 0:
        return thousands_part
    return options['separator'].join([thousands_part, danish_names_below_1000(rest, **options)])


if __name__ == '__main__':
    for n in range(20):
        value = 2**(2**n)
        print(f"{n}: {value}: {get_name(value, separator="-")}")
    print(f"{get_name(1_000_000_001)=}")
