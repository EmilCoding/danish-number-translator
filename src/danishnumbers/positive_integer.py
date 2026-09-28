"""
Defines the ´check_bounds´ decorator that wraps functions in a bounds checker.
"""
import functools
from typing import Any, TypeIs


def check_bounds(max_value: int, min_value: None | int = None):
    """Create a decorator that wraps the function in a type- and bounds checker.

    The decorator wraps a function ´func´: (int, ...) -> str. The first argument is
    check for its type and value which must be or type ´int´ and have a value in the
    interval [1, max_value]. If not, expections are raised.

    If ´max_value´ is None, then upper limit is not checked.
    """
    def decorator(func):
        """Wraps a function ´func´ in a type- and bounds checker.

        The function is expected to have signature ´func´: (int, ...) -> str.
        The first arguments is check if its an integer and have bounds [1, max_value].
        If type- or bounds are not satisfied, expections are raised.
        """
        if max_value is not None:
            func = enforce_maximum(func, max_value)
        if min_value is not None:
            func = enforce_minimum(func, min_value)
        return enforce_type_checker(func)
    return decorator


def is_positive_integer(n: Any) -> TypeIs[int]:
    """Check if a python object is an integer and its value is positive."""
    return isinstance(n, int) and n > 0


def enforce_type_checker(func):
    """Enforce checking first argument for its type."""
    @functools.wraps(func)
    def wrapper(n: int, *args: Any, **kwargs: Any) -> str:
        """Check if the first argument of `func` is a positive integer."""
        if not is_positive_integer(n):
            raise TypeError('Input argument must be a positve integer')
        return func(n, *args, **kwargs)
    return wrapper


def enforce_maximum(func, max_value: int):
    @functools.wraps(func)
    def wrapper(n: int, *args: Any, **kwargs: Any) -> str:
        """Check if the first argument is less than given max-value."""
        if n >= max_value:
            raise ValueError(f"Number 'n' must be below {max_value} - Was {n}")
        return func(n, *args, **kwargs)
    return wrapper


def enforce_minimum(func, min_value: int):
    @functools.wraps(func)
    def wrapper(n: int, *args: Any, **kwargs: Any) -> str:
        """Check if the first argument is greater than or equal to than given min-value."""
        if n < min_value:
            raise ValueError(f"Number 'n' must be greater than {min_value} - Was {n}")
        return func(n, *args, **kwargs)
    return wrapper
