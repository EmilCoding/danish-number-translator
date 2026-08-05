"""Danish number-name translation utilities.

This module provides functions to translate non-negative integers into
Danish words. The public entry point is ``get_name``, which accepts
values up to the supported maximum and optional formatting settings.

The implementation uses Danish short-scale naming for numbers below one
million and Danish long-scale power names for larger values.
"""
from typing import TypedDict, Unpack
from danishnumbers.large_prefix_generator import prefix_generator


POWERS_OF_THOUSANDS = (
    'Million', 'Milliard',
    'Billion', 'Billiard',
    'Trillion', 'Trilliard',
    'Kvadrillion', 'Kvadrilliard',
    'Kvintillion', 'Kvintilliard',
    'Sekstillion', 'Sekstilliard',
    'Septillion', 'Septilliard',
    'Oktillion', 'Oktilliard',
    'Nonillion', 'Nonilliard',
    'Decillion', 'Decilliard',
    'hendekallion', 'hendekalliard',
    'dodekallion', 'dodekalliard',
    'triskaidekallion', 'triskaidekalliard',
    'tettareskaidekallion', 'tettareskaidekalliard',
    'pentekaidekallion', 'pentekaidekalliard',
    'hekkaidekallion', 'hekkaidekalliard',
    'heptakaidekallion', 'heptakaidekalliard',
    'oktokaidekallion', 'oktokaidekalliard',
    'enneakaidekallion', 'enneakaidekalliard',
    'eikosillion', 'eikosilliard',
    'heiskaieikosillion', 'heiskaieikosillard',
    'duokaieikosillion', 'duokaieikosillard',
    'triskaieikosillion', 'triskaieikosillard',
    'tetterakaieikosillion', 'tetterakaieikosillard',
    'pentekaieikosillion', 'pentekaieikosillard',
    'hekkaieikosillion', 'hekkaieikosillard',
    'heptakaieikosillion', 'heptakaieikosillard',
    'oktokaieikosillion', 'oktokaieikosillard',
    'enneakaieikosillion', 'enneakaieikosillard',
    'heiskaitriakontallion', 'heiskaitriakontallard',
)


class NumberTooBig(Exception):
    """Exception raised when a number is larger than the supported range."""

    def __init__(self, n: int) -> None:
        super().__init__(f"Cannot handle a make a {n.bit_count()} bit number")


class FormatOptions(TypedDict):
    """Formatting options used throughout Danish number translation."""

    seperator: str
    et_before_hundred: bool
    et_before_thousands: bool


SMALL_DANISH_NUMBERS = {
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

DANISH_TENS = {
    1: 'ti',
    2: 'tyve',
    3: 'tredive',
    4: 'fyre',
    5: 'halvtreds',
    6: 'tres',
    7: 'halvfjerds',
    8: 'firs',
    9: 'halvfems',
}


DEFAULT_FORMAT_OPTIONS: FormatOptions = {
    'seperator': "",
    'et_before_hundred': True,
    'et_before_thousands': True,
}


def with_default_options(func):
    """Wrap a translator so default format options are applied.

    This decorator exposes a normal function signature with explicit defaults
    while internally converting those values into a shared ``FormatOptions``
    typed dict for downstream helper functions.
    """
    def caller(
        n: int,
        /,
        seperator="",
        et_before_hundred=True,
        et_before_thousands=True,
    ) -> str:
        options: FormatOptions = {
            "seperator": seperator,
            "et_before_hundred": et_before_hundred,
            "et_before_thousands": et_before_thousands,
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

    for prefix in POWERS_OF_THOUSANDS:
        if remainding == 0:
            break
        remainding, segment = divmod(remainding, 1_000)
        match segment:
            case 0:
                pass
            case 1:
                parts_of_word_reverse_order.append(options['seperator'].join(["En", prefix]))
            case int():
                parts_of_word_reverse_order.append(
                    options['seperator'].join([_below_a_thousand(segment, **options), prefix])
                )

    if remainding > 0:
        raise NumberTooBig(n)
    return options['seperator'].join(parts_of_word_reverse_order[::-1]).title()


@with_default_options
def _below_a_million(n: int, **options: Unpack[FormatOptions]) -> str:
    """Return the Danish word form of a non-negative integer below a million."""
    assert isinstance(n, int) and 0 <= n < 1_000_000, "Given number must be an integer between 0 and one million."
    thousands, rest = divmod(n, 1_000)

    match thousands:
        case 0:
            thousands_part = ""
        case 1:
            thousands_part = f"et{options['seperator']}tusind" if options['et_before_thousands'] else "tusind"
        case int():
            thousands_part = options['seperator'].join([_below_a_thousand(thousands, **options), "tusinde"])

    if rest == 0:
        return thousands_part
    return options['seperator'].join([thousands_part, _below_a_thousand(rest, **options)])


@with_default_options
def _below_a_thousand(n: int, **options: Unpack[FormatOptions]) -> str:
    """Return the Danish word form of a non-negative integer below a thousand."""
    assert isinstance(n, int) and 0 <= n < 1000, "Must be integer between 0 and 1000."
    hundrets, rest = divmod(n, 100)

    word_parts: list[str] = []

    # Define thousands part
    match hundrets:
        case 0:
            return _below_a_hundret(n, **options)
        case 1:
            word_parts.append("Et") if options['et_before_hundred'] else None
        case int():
            word_parts.append(_below_ten(hundrets, **options))
    word_parts.append("hundrede")

    # Define ones part
    word_parts += ["og", _below_a_hundret(rest, **options)] if rest > 0 else []

    return options['seperator'].join(word_parts)


@with_default_options
def _below_a_hundret(n: int, **options: Unpack[FormatOptions]) -> str:
    """Return the Danish name for a number below 100."""
    assert isinstance(n, int) and 0 <= n < 100, "Number must be a non-negative integer below 100"
    match divmod(n, 10):
        case (0, int()) | (1, int()):
            return _below_twenty(n, **options)
        case (tens, 0):
            return DANISH_TENS[tens]
        case (tens, ones):
            return options['seperator'].join([_below_ten(ones, **options), "og", DANISH_TENS[tens]])


@with_default_options
def _below_twenty(n: int, **options: Unpack[FormatOptions]) -> str:
    """Return the Danish name for a number below 20."""
    assert isinstance(n, int) and 0 <= n < 20, "Number must be a non-negative integer below 20"
    return SMALL_DANISH_NUMBERS[n]


@with_default_options
def _below_ten(n: int, **options: Unpack[FormatOptions]) -> str:
    """Return the Danish name for a number below 10."""
    assert isinstance(n, int) and 0 <= n < 10, "Number must be a non-negative integer below 10"
    return SMALL_DANISH_NUMBERS[n]


if __name__ == '__main__':
    for n in range(20):
        value = 2**(2**n)
        print(f"{n}: {value}: {get_name(value, seperator="-")}")

    print(f"{get_name(1_000_000_001)=}")