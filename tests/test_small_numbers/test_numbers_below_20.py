import pytest
from danishnumbers import danish_number_name


@pytest.mark.parametrize('n,name', (
    (1, 'en'), (2, 'to'), (3, 'tre'), (4, 'fire'), (5, 'fem'),
    (6, 'seks'), (7, 'syv'), (8, 'otte'), (9, 'ni'), (10, 'ti'), (11, 'elleve'),
    (12, 'tolv'), (13, 'tretten'), (14, 'fjorten'), (15, 'femten'), (16, 'seksten'),
    (17, 'sytten'), (18, 'atten'), (19, 'nitten'),
))
def test_below_20(n: int, name: str) -> None:
    assert name == danish_number_name(n).lower(), "Name does not match"
