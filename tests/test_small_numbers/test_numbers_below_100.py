import pytest
from danishnumbers import danish_number_name


@pytest.mark.parametrize('n,name', (
    (10, 'ti'), (20, 'tyve'), (30, 'tredive'), (40, 'fyrre'),
    (50, 'halvtreds'), (60, 'tres'), (70, 'halvfjerds'), 
    (80, 'firs'), (90, 'halvfems'),
))
def test_tens(n: int, name: str) -> None:
    assert name == danish_number_name(n), "Name does not match"


@pytest.mark.parametrize('n,name', (
    (21, 'en og tyve'),
    (33, 'tre og tredive'),
    (45, 'fem og fyrre'),
    (55, 'fem og halvtreds'),
    (87, 'syv og firs'),
    (99, 'ni og halvfems'),
))
@pytest.mark.parametrize('separator', [' ', '-', ''])
def test_below_hundred(n: int, name: str, separator: str) -> None:
    name = name.replace(' ', separator)
    assert name == danish_number_name(n, separator), "Name does not match"
