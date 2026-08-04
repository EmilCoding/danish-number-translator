import pytest
from danishnumbers.number import below_twenty


@pytest.mark.parametrize('n,name', (
    (0, 'nul'), (1, 'en'), (2, 'to'), (3, 'tre'), (4, 'fire'), (5, 'fem'),
    (6, 'seks'), (7, 'syv'), (8, 'otte'), (9, 'ni'), (10, 'ti'), (11, 'elleve'),
    (12, 'tolv'), (13, 'tretten'), (14, 'fjorten'), (15, 'femten'), (16, 'seksten'),
    (17, 'sytten'), (18, 'atten'), (19, 'nitten'),
))
def test_input_output(n: int, name: str) -> None:
    assert below_twenty(n).lower() == name.lower(), "Name does not match"
