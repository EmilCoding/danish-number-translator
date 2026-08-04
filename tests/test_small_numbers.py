import pytest
from danishnumbers.number import get_number_name_danish


@pytest.mark.parametrize('n,name', (
    (0, 'nul'), (1, 'en'), (2, 'to'), (3, 'tre'), (4, 'fire'), (5, 'fem'),
    (6, 'seks'), (7, 'syv'), (8, 'otte'), (9, 'ni'), (10, 'ti'), (11, 'elleve'),
    (12, 'tolv'), (13, 'tretten'), (14, 'fjorten'), (15, 'femten'), (16, 'seksten'),
    (17, 'sytten'), (18, 'atten'), (19, 'nitten'),
))
def test_below_20(n: int, name: str) -> None:
    assert get_number_name_danish(n).lower() == name.lower(), "Name does not match"


@pytest.mark.skip
@pytest.mark.parametrize('n,name', (
    (21, 'en og tyve'),
    (33, 'tre og tredive'),
    (45, 'fem og fyre'),
    (55, 'fem og halvtreds'),
    (87, 'syv og firs'),
    (99, 'ni og halvfems'),
))
def test_below_hundred(n: int, name: str) -> None:
    output = get_number_name_danish(n, seperator_below_1000=" ").lower()
    assert name == output, f"Error {n}: Got {output}, expected {name}"


@pytest.mark.skip
@pytest.mark.parametrize('n,name', (
    (100, 'et hundrede'),
    (101, 'et hundrede og en'),
    (123, 'et hundrede og tre og tyve'),
    (500, 'fem hundrede'),
    (517, 'fem hundrede og sytten'),
    (999, 'ni hundrede og ni og halvfems'),
))
def test_below_a_thousand(n: int, name: str) -> None:
    output = get_number_name_danish(n, seperator_below_1000=" ").lower()
    assert name == output, f"Error {n}: Got {output}, expected {name}"


@pytest.mark.skip
@pytest.mark.parametrize('n,name', (
    (967044, "ni hundrede syv og treds tusinde og fire og fyre"),
    (198411, "et hundrede ni og halvfems tusinde fire hundrede og elleve"),
    (565929, "fem hundrede fem og treds tusinde ni hundrede og ni og tyve"),
    (450962, "fire hundrede og halvtreds tusinde ni hundrede og to og treds"),
    (457194, "fire hundrede syv og halvtreds tusinde et hundrede fire og halvfems"),
    (425087, "fire hundrede fem og tyve tusinde og syv og firs"),
    (922995, "ni hundrede to og tyve tuside ni hundrede fem og halv fems"),
    (751214, "syv hundrede en og halvtreds tusinde to hundrede og fjorten"),
    (559665, "fem hundrede og ni og halvtreds tusinde seks hundrede og fem og treds"),
    (315660, "tre hundrede femten tusinde seks hundrede og treds"),
))
def test_below_a_million(n: int, name: str) -> None:
    output = get_number_name_danish(n).lower()
    assert name == output, f"Error {n}: Got {output}, expected {name}"
