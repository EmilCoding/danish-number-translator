import enum
import functools
from typing import TypedDict, Unpack


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
    pass


class FormatOptions(TypedDict):
    seperator: str
    et_before_hundred: bool
    et_before_thusind: bool
    og_between_large_powers: bool
    conjugate_large_power: bool


class SmallDanishNumbers(enum.IntEnum):
    NUL = 0
    EN = 1
    TO = 2
    TRE = 3
    FIRE = 4
    FEM = 5
    SEKS = 6
    SYV = 7
    OTTE = 8
    NI = 9
    TI = 10
    ELLEVE = 11
    TOLV = 12
    TRETTEN = 13
    FJORTEN = 14
    FEMTEN = 15
    SEKSTEN = 16
    SYTTEN = 17
    ATTEN = 18
    NITTEN = 19


class DanishTens(enum.IntEnum):
    TI = 10
    TYVE = 20
    TREDIVE = 30
    FYRE = 40
    HALVTREDS = 50
    TRES = 60
    HALVFJERDS = 70
    FIRS = 80
    HALVFEMS = 90


def format_name(func):
    @functools.wraps(func)
    def wrapper(n: int, **options: Unpack[FormatOptions]) -> str:
        return func(n, **options).title()
    return wrapper


def set_default_values_options(func):
    def wrapped(
        n: int,
        /,
        seperator: str = " ",
        et_before_hundred: bool = True,
        et_before_thusind: bool = True,
        og_between_large_powers: bool = False,
        conjugate_large_power: bool = True,
    ) -> str:
        return func(
            n,
            seperator=seperator,
            et_before_hundred=et_before_hundred,
            et_before_thusind=et_before_thusind,
            og_between_large_powers=og_between_large_powers,
            conjugate_large_power=conjugate_large_power,
        )
    return wrapped


@set_default_values_options
@format_name
def get_number_name_danish(n: int, **options: Unpack[FormatOptions]) -> str:
    if n < 1_000_000:
        return below_a_million(n, **options)

    current, rest = divmod(n, 1_000_000)
    parts: list[str] = [below_a_million(rest, **options)]
    for prefix in POWERS_OF_THOUSANDS:
        current, rest = divmod(current, 1_000)
        if rest == 0:
            pass
        elif rest == 1:
            parts.append(options['seperator'].join(['En', prefix]))
        else:
            parts.append(options['seperator'].join([
                below_a_thousand(rest, **options),
                prefix + ("er" if options['conjugate_large_power'] else "")
            ]))

    if current == 0:
        return options['seperator'].join(parts[::-1])
    raise NumberTooBig("Number is too big to handle")


@format_name
@set_default_values_options
def below_a_million(n: int, **options: Unpack[FormatOptions]) -> str:
    if n < 1_000:
        return below_a_thousand(n, **options)
    assert n < 1_000_000, "Number must be below a million"

    parts: list[str] = []
    thousands, rest = divmod(n, 1_000)

    # Define parts related to the thousands
    if thousands == 1:
        parts += (['Et',] if options['et_before_thusind'] else []) + ['tusind']
    else:
        parts += [below_a_thousand(thousands, **options), 'tusind']

    # Define parts related to the rest
    if 0 == (rest // 100):
        parts.append('og')
    parts.append(below_a_thousand(rest, **options))

    # Make the word from the parts
    return options['seperator'].join(parts)


@format_name
@set_default_values_options
def below_a_thousand(n: int, **options: Unpack[FormatOptions]) -> str:
    if n < 100:
        return below_a_hundret(n, **options)

    # Defined list of parts of the word
    parts: list[str] = []
    hundrets, rest = divmod(n, 100)

    # Define parts related to hundrets
    if hundrets == 1:
        parts += (['Et'] if options['et_before_hundred'] else []) + ['hundrede']
    else:
        parts += [below_ten(hundrets, **options), 'hundrede']

    # Defined the part related to ones
    parts += (['og', below_a_hundret(rest, **options)] if rest > 0 else [])
    return options['seperator'].join(parts)


@format_name
@set_default_values_options
def below_a_hundret(n: int, **options: Unpack[FormatOptions]) -> str:
    assert n < 100
    if n < 20:
        return below_twenty(n)
    tens, ones = divmod(n, 10)
    if ones == 0:
        return DanishTens(n).name
    return options['seperator'].join([below_ten(ones), "og", DanishTens(10 * tens).name])


@format_name
def below_twenty(n: int, **__) -> str:
    assert n < 20, "Number must be below 20"
    return SmallDanishNumbers(n).name


@format_name
def below_ten(n: int, **__) -> str:
    return SmallDanishNumbers(n).name


if __name__ == '__main__':
    for n in range(11):
        value = 2**(2**n)
        print(f"{n}: {value}: {get_number_name_danish(value, seperator="-").lower()}")