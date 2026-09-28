import pytest
from danishnumbers import danish_number_name

@pytest.mark.parametrize('n,name', (
    (19, 'nitten'),
    (21, 'en og tyve'),
    (44, 'fire og fyrre'),
    (500, 'fem hundrede'),
    (517, 'fem hundrede og sytten'),
    (999, 'ni hundrede og ni og halvfems'),
))
def test_below_a_thousand(n: int, name: str) -> None:
    assert name == danish_number_name(n, separator=" "), "Name does not match"


@pytest.mark.parametrize('n,name', (
    (100, 'hundrede'),
    (101, 'hundrede og en'),
    (102, 'hundrede og to'),
    (123, 'hundrede og tre og tyve'),
    (199, 'hundrede og ni og halvfems'),
))
@pytest.mark.parametrize('et_before_hundrede', [False, True])
def test_et_before_hundrede_option(n: int, name: str, et_before_hundrede: bool) -> None:
    if et_before_hundrede:
        name = "et " + name
    assert name == danish_number_name(n, separator=" ", et_before_hundrede=et_before_hundrede), "Name does not match"
