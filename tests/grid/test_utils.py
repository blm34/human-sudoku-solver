import pytest

from grid.utils import digit_mask


@pytest.mark.parametrize(
    ("digit", "expected_mask"),
    [
        (1, 0b000000001),
        (2, 0b000000010),
        (3, 0b000000100),
        (4, 0b000001000),
        (5, 0b000010000),
        (6, 0b000100000),
        (7, 0b001000000),
        (8, 0b010000000),
        (9, 0b100000000),
    ],
)
def test_digit_mask(digit, expected_mask):
    # ACT
    mask = digit_mask(digit)

    # ASSERT
    assert mask == expected_mask
