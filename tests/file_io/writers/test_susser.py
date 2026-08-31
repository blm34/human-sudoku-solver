from io import StringIO
from unittest.mock import Mock

from persistance.writers.susser import SusserWriter


def test_writes_values_to_stream():
    # ARRANGE
    values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 9, 8, 7, 6, 5, 4, 3, 2, 1]

    grid = Mock(values=values)
    stream = StringIO()

    writer = SusserWriter()

    # ACT
    writer.write(grid, stream)

    # ASSERT
    assert stream.getvalue() == "123456789987654321"


def test_writes_empty_cells_as_dots():
    # ARRANGE
    grid = Mock(values=[0] * 81)
    stream = StringIO()

    writer = SusserWriter()

    # ACT
    writer.write(grid, stream)

    # ASSERT
    assert stream.getvalue() == "." * 81


def test_writes_zero_and_values_correctly():
    # ARRANGE
    values = [0] * 81
    values[0] = 5
    values[40] = 7
    values[80] = 3

    grid = Mock(values=values)
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


def test_writes_values_in_grid_order():
    # ARRANGE
    values = list(range(1, 10)) * 9

    grid = Mock(values=values)
    stream = StringIO()

    writer = SusserWriter()

    # ACT
    writer.write(grid, stream)

    # ASSERT
    assert stream.getvalue() == "".join(str(value) for value in values)
