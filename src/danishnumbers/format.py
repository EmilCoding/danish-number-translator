"""
Define formatting options.
"""
from typing import Protocol, TypedDict, Unpack


class Translator(Protocol):

    def __call__(self, n: int, **options: Unpack[FormatOptions]) -> str:
        ...


class FormatOptions(TypedDict):
    """Format options for the `danish_number_name` functions.

    Args:
        separator (str, optional): Separator used to separate parts of the name for
          more readability. Eg. is separator='-', then 1001 becomes "tusinde-og-en".

        et_before_hundrede (bool, optional): If flag is set, then single-digit hundreds have an
          "et" as a prefix. So 100 becomes "ethundrede" (one hundred)

        et_before_tusinde (bool, optional): If flag is set, then single-digit thousands have an
          "et" as a prefix. So 1000 is "ettusinde" (one thousand).

        group_hundreds_and_thousands_digit (bool, optional): If flag is set, hundreds and thousands
          digit are grouped together when naming. The results in 1100 becomes "ellevehundrede"
          (eleven hundred) instead of "ettusindeethundede" (one thousand one hundreds).
    """
    separator: str
    in_prefix_separator: str
    et_before_hundrede: bool
    et_before_tusinde: bool
    group_hundreds_and_thousands_digit: bool


def set_default_values_option(func: Translator):
    """Add default values to the options."""
    def wrapper(
        n: int,
        /,
        separator: str = "",
        in_prefix_separator: str = "",
        et_before_hundrede: bool = True,
        et_before_tusinde: bool = True,
        group_hundreds_and_thousands_digit: bool = False,
    ) -> str:
        options: FormatOptions = {
            'separator': separator,
            'et_before_hundrede': et_before_hundrede,
            'et_before_tusinde': et_before_tusinde,
            'group_hundreds_and_thousands_digit': group_hundreds_and_thousands_digit,
            'in_prefix_separator': in_prefix_separator,
        }
        return func(n, **options)
    return wrapper
