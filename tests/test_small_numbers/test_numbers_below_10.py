import pytest
from danishnumbers import danish_number_name


@pytest.mark.parametrize('n,name', (
    (1, 'en'), (2, 'to'), (3, 'tre'), (4, 'fire'), (5, 'fem'),
    (6, 'seks'), (7, 'syv'), (8, 'otte'), (9, 'ni'),
))
def test_below_10(n: int, name: str) -> None:
    assert name == danish_number_name(n), "Name does not match"
