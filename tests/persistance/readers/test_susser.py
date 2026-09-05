from io import StringIO

import pytest

from grid import Cell
from persistance.readers.susser import SusserReader


def test_reads_complete_grid():
    # ARRANGE
    text = (
        "123456789"
        "456789123"
        "789123456"
        "234567891"
        "567891234"
        "891234567"
        "345678912"
        "678912345"
        "912345678"
    )
    stream = StringIO(text)

    reader = SusserReader()

    # ACT
    grid = reader.read(stream)

    # ASSERT
    assert all(grid._values[idx] == int(char) for idx, char in enumerate(text))


def test_reads_values_into_correct_cells():
    # ARRANGE
    text = "1" + "." * 80
    stream = StringIO(text)

    reader = SusserReader()

    # ACT
    grid = reader.read(stream)

    # ASSERT
    assert grid._values[0] == 1
    assert all(value == 0 for value in grid._values[1:])


def test_leaves_empty_cells_unset():
    # ARRANGE
    text = "." * 81
    stream = StringIO(text)

    reader = SusserReader()

    # ACT
    grid = reader.read(stream)

    # ASSERT
    assert all(val == 0 for val in grid._values)


@pytest.mark.parametrize("empty", ["0", ".", "X", "*", "_"])
def test_supports_preferred_empty_characters(empty):
    # ARRANGE
    text = "5" + empty * 80
    stream = StringIO(text)

    reader = SusserReader()

    # ACT
    grid = reader.read(stream)

    # ASSERT
    assert grid._values[0] == 5
    assert all(value == 0 for value in grid._values[1:])


def test_raises_error_when_input_is_too_short():
    # ARRANGE
    text = "." * 80
    stream = StringIO(text)

    reader = SusserReader()

    # ACT / ASSERT
    with pytest.raises(ValueError, match="Expected 81 characters but got 80"):
        reader.read(stream)


def test_raises_error_when_input_is_too_long():
    # ARRANGE
    text = "." * 82
    stream = StringIO(text)

    reader = SusserReader()

    # ACT / ASSERT
    with pytest.raises(ValueError, match="Expected 81 characters but got 82"):
        reader.read(stream)


def test_raises_error_when_empty_character_cannot_be_determined():
    # ARRANGE
    text = "1" * 80 + "A"
    stream = StringIO(text)

    reader = SusserReader()

    # ACT / ASSERT
    with pytest.raises(
        ValueError,
        match="Could not determine the 'empty' character",
    ):
        reader.read(stream)


@pytest.mark.xfail(
    strict=True,
    reason="This functionality has not yet been implemented",
)
def test_can_determine_a_non_standard_empty_character():
    # ARRANGE
    text = "1" * 80 + "A"
    stream = StringIO(text)

    reader = SusserReader()

    # ACT
    grid = reader.read(stream)

    # ASSERT
    assert grid._values[0] == 1
    assert all(value == 0 for value in grid._values[1:])


def test_values_are_written_to_correct_cells():
    # ARRANGE
    text = (
        "1........"
        "........."
        "........."
        "........."
        "....5...."
        "........."
        "........."
        "........."
        "........9"
    )
    stream = StringIO(text)

    reader = SusserReader()

    # ACT
    grid = reader.read(stream)

    # ASSERT
    assert grid._values[Cell(0, 0).index] == 1
    assert grid._values[Cell(4, 4).index] == 5
    assert grid._values[Cell(8, 8).index] == 9


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("1" + "0" * 80, "0"),
        ("1" + "." * 80, "."),
        ("1" + "X" * 80, "X"),
        ("1" + "*" * 80, "*"),
        ("1" + "_" * 80, "_"),
    ],
)
def test_get_empty_character(text, expected):
    # ARRANGE
    reader = SusserReader()

    # ACT
    char = reader._get_empty_character(text)

    assert char == expected
