import enum
import functools
from typing import Any, NotRequired, TypedDict, Unpack


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

    def __init__(self, n: int) -> None:
        super().__init__(f"Cannot handle a make a {n.bit_count()} bit number")


class FormatOptions(TypedDict):
    seperator: NotRequired[str]
    et_before_hundred: NotRequired[bool]
    et_before_thusind: NotRequired[bool]
    og_between_large_powers: NotRequired[bool]
    conjugate_large_power: NotRequired[bool]


SMALL_DANISH_NUMBERS = {
    0: 'Nul',
    1: 'En',
    2: 'To',
    3: 'Tre',
    4: 'Fire',
    5: 'Fem',
    6: 'Seks',
    7: 'Syv',
    8: 'Otte',
    9: 'Ni',
    10: 'Ti',
    11: 'Elleve',
    12: 'Tolv',
    13: 'Tretten',
    14: 'Fjorten',
    15: 'Femten',
    16: 'Seksten',
    17: 'Sytten',
    18: 'Atten',
    19: 'Nitten',
}

DANISH_TENS = {
    1: 'Ti',
    2: 'Tyve',
    3: 'Tredive',
    4: 'Fyre',
    5: 'Halvtreds',
    6: 'Tres',
    7: 'Halvfjerds',
    8: 'Firs',
    9: 'Halvfems',
}


MAXIMUM_INT_VALUE = ...


def set_default_options(func):
    @functools.wraps(func)
    def caller(n: int, **kwargs: Unpack[FormatOptions]) -> str:
        kwargs['seperator'] = kwargs.get('seperator', "")
        kwargs['et_before_hundred'] = kwargs.get('et_before_hundred', True)
        kwargs['et_before_thusind'] = kwargs.get('et_before_thusind', True)
        kwargs['og_between_large_powers'] = kwargs.get('og_between_large_powers', True)
        kwargs['conjugate_large_power'] = kwargs.get('conjugate_large_power', True)
        return func(n, **kwargs)
    return caller


def get_number_name_danish(
    n: int,
    seperator: str = "",
    et_before_hundred: bool = True,
    conjugate_large_power: bool = True,
    **__: Any,
) -> str:
    """Return the Danish word form of a non-negative integer.

    The function supports numbers from 0 up to the maximum allowed value
    defined by ``MAXIMUM_INT_VALUE``. Numbers below one million are formatted
    directly; larger numbers are scaled using the Danish long scale prefixes
    in ``POWERS_OF_THOUSANDS``.

    Args:
        n (int): Non-negative integer to convert. Must be less than
            ``MAXIMUM_INT_VALUE``.
        seperator_below_100 (str): String used to join Danish word parts. For example,
            ``seperator_below_100=" "`` produces ``"Fem og halvfems"`` for 55.
            Default is ``""`` when the wrapper decorator is applied.
        et_before_hundred (bool): Include ``et`` before ``hundrede`` for
            numbers in the 100–199 range. Default is ``True``.
        et_before_thusind (bool): Include ``et`` before ``tusind`` for 1000.
            Default is ``True``.
        og_between_large_powers (bool): If True, insert ``og`` between large
            power groups. Default is ``False``.
        conjugate_large_power (bool): If True, conjugate large power names by
            appending ``er`` when appropriate. Default is ``True``.

    Raises:
        NumberTooBig: If ``n`` is larger than the supported maximum.

    Returns:
        str: The Danish word representation of ``n``.
    """
    assert isinstance(n, int) and n >= 0, "n must be a non-negative integer"

    # Handle the part below one-million.
    remainding, segment = divmod(n, 1_000_000)
    parts_of_word_reverse_order = [below_a_million(segment), ]

    for prefix in POWERS_OF_THOUSANDS:
        if remainding == 0:
            break
        remainding, segment = divmod(remainding, 1_000)
        match segment:
            case 0:
                pass
            case 1:
                parts_of_word_reverse_order.append(f"En{seperator}{prefix}")
            case int():
                if conjugate_large_power:
                    prefix = prefix + "er"
                segment_as_string = below_a_thousand(segment)
                parts_of_word_reverse_order.append(f"{segment_as_string}{seperator}{prefix}")

    if remainding > 0:
        raise NumberTooBig(n)
    return seperator.join(parts_of_word_reverse_order[::-1]).title()


def below_a_million(
    n: int,
    seperator: str = "",
    et_before_thousand: bool = True,
    **__: Any,
) -> str:
    """Return the Danish word form of a non-negative integer below a million.

    Args:
        n (int): Non-negative integer to convert. Must be less than 1_000_000.
        seperator (str): String used to join Danish word parts. For example,
            ``seperator=" "`` produces ``"Fem og halvfems"`` for 55.
            Default is ``" "`` when the wrapper decorator is applied.
        et_before_hundred (bool): Include ``et`` before ``hundrede`` for
            numbers in the 100–199 range. Default is ``True``.
        et_before_thusind (bool): Include ``et`` before ``tusind`` for 1000.
            Default is ``True``.

    Returns:
        str: The Danish word representation of ``n``.
    """
    assert isinstance(n, int) and 0 <= n < 1_000_000, "Given number must be an integer between 0 and one million."

    if n in SMALL_DANISH_NUMBERS:
        return SMALL_DANISH_NUMBERS[n]
    if n < 1_000:
        return below_a_thousand(n)

    # seperator = options.get('seperator', DEFAULT_SEPERATOR) # TODO: Make this a better system
    thousands, modulo = divmod(n, 1_000)

    # Handle the thousands
    match thousands:
        case 0:
            thousands_part = ""
        case 1:
            thousands_part = f"{'et' if et_before_thousand else ''}{seperator}tusind"
        case int():
            thousands_part = f"{below_a_thousand(thousands)}{seperator}tusinde"

    # Handle hundrets part
    if modulo == 0:
        return thousands_part
    if modulo < 10:
        return seperator.join([thousands_part, "og", below_a_hundret(modulo)])
    return f"{thousands_part}{seperator}{below_a_thousand(modulo)}"


def below_a_thousand(
    n: int,
    seperator: str = "",
    et_before_hundred: bool = True,
    og_between_hundrets_and_tens: bool = True,
    **__: Any,
) -> str:
    """Return the Danish word form of a non-negative integer below a thousand.

    Args:
        n (int): Non-negative integer to convert. Must be less than 1_000.
        seperator (str): String used to join Danish word parts. For example,
            ``seperator=" "`` produces ``"Fem og halvfems"`` for 55.
            Default is ``" "`` when the wrapper decorator is applied.
        et_before_hundred (bool): Include ``et`` before ``hundrede`` for
            numbers in the 100–199 range. Default is ``True``.
        og_between_hundrets_and_tens (bool): Include ``og`` between hundrets and tens part.
            Default is ``True``.

    Returns:
        str: The Danish word representation of ``n``.
    """
    assert isinstance(n, int) and 0 <= n < 1000, "Must be integer between 0 and 1000."
    hundrets, rest = divmod(n, 100)

    # Get hundrets part
    match hundrets:
        case 0:
            return below_a_hundret(n, seperator=seperator)
        case 1:
            hundrets_part = f"et{seperator}hundrede" if et_before_hundred else "hundrede"
        case int():
            hundrets_part = seperator.join([SMALL_DANISH_NUMBERS[hundrets], "hundrede"])

    # Get tens part
    if rest == 0:
        return hundrets_part
    tens_part = below_a_hundret(rest, seperator=seperator)

    return seperator.join(
        [hundrets_part, "og", tens_part]
        if og_between_hundrets_and_tens else
        [hundrets_part, tens_part]
    )


def below_a_hundret(n: int, seperator: str = "", **__: Any) -> str:
    """Return the Danish name for a number below 100.
    Args:
        n (int): Non-negative integer to convert. Must be less than 100.
        seperator (str): String used to join Danish word parts. For example,
            ``seperator=" "`` produces ``"Fem og halvfems"`` for 55. Default is "".
    Returns:
        str: The Danish word representation of ``n``.
    """
    assert isinstance(n, int) and 0 <= n < 100, "Number must be non-negativ integer below 100"
    tens, ones = divmod(n, 10)
    match tens:
        case 0 | 1:
            return below_twenty(n)
        case int():
            return seperator.join([below_ten(ones), "og", DANISH_TENS[tens]])


def below_twenty(n: int, **__: Any) -> str:
    """Return the Danish name for a number below 20."""
    assert isinstance(n, int) and 0 <= n < 20, "Number must be non-negativ integer below 20"
    return SMALL_DANISH_NUMBERS[n]


def below_ten(n: int, **__: Any) -> str:
    """Return the Danish name for a number below 10."""
    assert isinstance(n, int) and 0 <= n < 10, "Number must be non-negativ integer below 20"
    return SMALL_DANISH_NUMBERS[n]


if __name__ == '__main__':
    for n in range(5):
        value = 2**(2**n)
        print(f"{n}: {value}: {get_number_name_danish(value, seperator="-")}")

    print(f"{get_number_name_danish(1_000_000_001)=}")
