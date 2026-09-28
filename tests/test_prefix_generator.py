import pytest
import itertools

from danishnumbers.large_prefix_generator import prefix_generator, ExponentDegreeTooHigh


def test_alternative_suffix_long_form():
    prefixes = map(lambda pair: pair[1], prefix_generator(longform=True))
    for value1, value2 in itertools.batched(prefixes, n=2):
        if not (value1.endswith('illion') and value2.endswith('lliard')):
            raise ValueError(f'Suffix was not correct for {(value1, value2)}')
