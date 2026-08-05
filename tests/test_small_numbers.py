import pytest
from danishnumbers.number import FormatOptions, _below_twenty, _below_a_hundret, _below_a_thousand, _below_a_million

OPTIONS: FormatOptions = {
    'seperator': " ",
    'et_before_hundred': True,
    'et_before_thousands': True,
}


@pytest.mark.parametrize('n,name', (
    (0, 'nul'), (1, 'en'), (2, 'to'), (3, 'tre'), (4, 'fire'), (5, 'fem'),
    (6, 'seks'), (7, 'syv'), (8, 'otte'), (9, 'ni'), (10, 'ti'), (11, 'elleve'),
    (12, 'tolv'), (13, 'tretten'), (14, 'fjorten'), (15, 'femten'), (16, 'seksten'),
    (17, 'sytten'), (18, 'atten'), (19, 'nitten'),
))
def test_below_20(n: int, name: str) -> None:
    assert name == _below_twenty(n, **OPTIONS).lower(), "Name does not match"


@pytest.mark.parametrize('n,name', (
    (10, 'ti'), (20, 'tyve'), (30, 'tredive'), (40, 'fyre'),
    (50, 'halvtreds'), (60, 'tres'), (70, 'halvfjerds'), 
    (80, 'firs'), (90, 'halvfems'),
))
def test_tens(n: int, name: str) -> None:
    assert name == _below_a_hundret(n, **OPTIONS).lower(), "Name does not match"


@pytest.mark.parametrize('n,name', (
    (21, 'en og tyve'),
    (33, 'tre og tredive'),
    (45, 'fem og fyre'),
    (55, 'fem og halvtreds'),
    (87, 'syv og firs'),
    (99, 'ni og halvfems'),
))
def test_below_hundred(n: int, name: str) -> None:
    output = _below_a_hundret(n, **OPTIONS).lower()
    assert name == output, f"Error {n}: Got {output}, expected {name}"


@pytest.mark.parametrize('n,name', (
    (100, 'et hundrede'),
    (101, 'et hundrede og en'),
    (123, 'et hundrede og tre og tyve'),
    (500, 'fem hundrede'),
    (517, 'fem hundrede og sytten'),
    (999, 'ni hundrede og ni og halvfems'),
))
def test_below_a_thousand(n: int, name: str) -> None:
    output = _below_a_thousand(n, **OPTIONS).lower()
    assert name == output, f"Error {n}: Got {output}, expected {name}"


@pytest.mark.parametrize('n,name', (
    (900000, "ni hundrede tusinde"),
    (967044, "ni hundrede og syv og tres tusinde fire og fyre"),
    (198411, "et hundrede og otte og halvfems tusinde fire hundrede og elleve"),
    (565929, "fem hundrede og fem og tres tusinde ni hundrede og ni og tyve"),
    (450962, "fire hundrede og halvtreds tusinde ni hundrede og to og tres"),
    (457194, "fire hundrede og syv og halvtreds tusinde et hundrede og fire og halvfems"),
    (425087, "fire hundrede og fem og tyve tusinde syv og firs"),
    (922995, "ni hundrede og to og tyve tusinde ni hundrede og fem og halvfems"),
    (751214, "syv hundrede og en og halvtreds tusinde to hundrede og fjorten"),
    (559665, "fem hundrede og ni og halvtreds tusinde seks hundrede og fem og tres"),
    (315660, "tre hundrede og femten tusinde seks hundrede og tres"),
))
def test_below_a_million(n: int, name: str) -> None:
    output = _below_a_million(n, **OPTIONS).lower()
    assert name == output, f"Error {n}: Got {output}, expected {name}"
