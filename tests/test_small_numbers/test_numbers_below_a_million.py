"""
Test if the translator can generate numbers below a million.

"""

import pytest
from danishnumbers import danish_number_name


@pytest.mark.parametrize('n,name', (
    (5, 'fem'),
    (55, 'fem og halvtreds'),
    (1099, 'et tusinde og ni og halvfems'),
    (2000, 'to tusinde'),
    (1200, 'et tusinde to hundrede'),
    (5400, 'fem tusinde fire hundrede'),
    (11500, 'elleve tusinde fem hundrede'),
    (900000, "ni hundrede tusinde"),
    (967044, "ni hundrede og syv og tres tusinde og fire og fyrre"),
    (198411, "et hundrede og otte og halvfems tusinde fire hundrede og elleve"),
    (565929, "fem hundrede og fem og tres tusinde ni hundrede og ni og tyve"),
    (450962, "fire hundrede og halvtreds tusinde ni hundrede og to og tres"),
    (457194, "fire hundrede og syv og halvtreds tusinde et hundrede og fire og halvfems"),
    (425087, "fire hundrede og fem og tyve tusinde og syv og firs"),
    (922995, "ni hundrede og to og tyve tusinde ni hundrede og fem og halvfems"),
    (751214, "syv hundrede og en og halvtreds tusinde to hundrede og fjorten"),
    (559665, "fem hundrede og ni og halvtreds tusinde seks hundrede og fem og tres"),
    (315660, "tre hundrede og femten tusinde seks hundrede og tres"),
))
def test_below_a_million(n: int, name: str):
    assert name == danish_number_name(n, separator=" "), "Name did not match"


@pytest.mark.parametrize('n,name', (
    (1100, 'elleve hundrede'),
    (1150, 'elleve hundrede halvtreds'),
    (1200, 'tolv hundrede'),
    (5400, 'fire og halvtreds hundrede'),
    (2000, 'to tusinde'),
    (3000, 'tre tusinde'),
    (9900, 'ni og halvfems hundrede'),
    (9999, 'ni og halvfems hundrede ni og halvfems'),
))
def test_grouping_digits(n: int, name: str):
    assert name == danish_number_name(n, separator=" ", group_hundreds_and_thousands_digit=True), "Name did not match."
