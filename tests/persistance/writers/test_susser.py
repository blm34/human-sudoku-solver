from io import StringIO
from unittest.mock import Mock

from sudoku_strategy.persistance.writers.susser import SusserWriter


def test_writes_digits_to_stream():
    # ARRANGE
    digits = [1, 2, 3, 4, 5, 6, 7, 8, 9, 9, 8, 7, 6, 5, 4, 3, 2, 1]

    grid = Mock(_digits=digits)
    stream = StringIO()

    writer = SusserWriter()

    # ACT
    writer.write(grid, stream)

    # ASSERT
    assert stream.getvalue() == "123456789987654321"


def test_writes_empty_cells_as_dots():
    # ARRANGE
    grid = Mock(_digits=[0] * 81)
    stream = StringIO()

    writer = SusserWriter()

    # ACT
    writer.write(grid, stream)

    # ASSERT
    assert stream.getvalue() == "." * 81


def test_writes_zero_and_digits_correctly():
    # ARRANGE
    digits = [0] * 81
    digits[0] = 5
    digits[40] = 7
    digits[80] = 3

    grid = Mock(_digits=digits)
    stream = StringIO()

    writer = SusserWriter()

    # ACT
    writer.write(grid, stream)

    # ASSERT
    output = stream.getvalue()

    assert len(output) == 81
    assert output[0] == "5"
    assert output[40] == "7"
    assert output[80] == "3"


def test_writes_digits_in_grid_order():
    # ARRANGE
    digits = list(range(1, 10)) * 9

    grid = Mock(_digits=digits)
    stream = StringIO()

    writer = SusserWriter()

    # ACT
    writer.write(grid, stream)

    # ASSERT
    assert stream.getvalue() == "".join(str(digit) for digit in digits)
