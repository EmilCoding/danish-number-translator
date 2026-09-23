"""
Defines the ´check_bounds´ decorator that wraps functions in a bounds checker.
"""
import functools
from typing import Any, TypeIs


def check_bounds(max_value: int):
    """Create a decorator that wraps the function in a type- and bounds checker.

    The decorator wraps a function ´func´: (int, ...) -> str. The first argument is
    check for its type and value which must be or type ´int´ and have a value in the
    interval [1, max_value]. If not, expections are raised.
    """
    def decorator(func):
        """Wraps a function ´func´ in a type- and bounds checker.

        The function is expected to have signature ´func´: (int, ...) -> str.
        The first arguments is check if its an integer and have bounds [1, max_value].
        If type- or bounds are not satisfied, expections are raised.
        """
        @functools.wraps(func)
        def wrappper(n: int, *args: Any, **kwargs: Any) -> str:
            """Check if the input argument is an interger in the interval [1, max_value].

            Args:
                n (int): Number to be checked.

            Raises:
                TypeError: If number is not an integer or integer is non-positive.
                ValueError: If number is larger than the maximum value.

            Returns:
                str: Name of the number determined by function ´func´.
            """
            if not is_positive_integer(n):
                raise TypeError('Input argument must be a positve integer')
            if not n < max_value:
                raise ValueError(f"Number 'n' must be below {max_value} - Was {n}")
            return func(n, *args, **kwargs)
        return wrappper
    return decorator


def is_positive_integer(n: Any) -> TypeIs[int]:
    """Check if a python object is an integer and its value is positive."""
    return isinstance(n, int) and n > 0
