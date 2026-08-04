import pytest
from danishnumbers import get_number_name_danish


GIANT_NUMBER = int('0x' + 1023*'F', base=16)


@pytest.mark.parametrize('n', [
    0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
    24, 25, 28, 32, 33, 47, 63, 67, 93, 100,
    132, 241, 378, 574, 646, 724, 819, 864, 898, 916,
    161225, 180470, 305918, 339672, 383213, 436572, 456475, 602028, 618237, 714031, 717475, 811782, 
    855200, 917688, 982434,
    95613015, 448299922, 731116721, 920142532, 957241897, 1062108163, 1123928350, 1269469302, 1558538977, 
    4019464748,
])
def test_runs_at_all(n: int) -> None:
    number = get_number_name_danish(n)
    assert isinstance(number, str), f"Error for {hex(n)}"


def test_giant_number() -> None:
    _ = get_number_name_danish(GIANT_NUMBER)
