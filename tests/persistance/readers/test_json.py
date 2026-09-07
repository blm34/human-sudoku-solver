import json
from io import StringIO

from sudoku_strategy.grid import Cell
from sudoku_strategy.persistance.readers.json import JsonReader


def test_reads_puzzle_digits():
    # ARRANGE
    puzzle_digits = [1, 2, 3] + [0] * 78
    text = json.dumps(
        {
            "puzzle_digits": puzzle_digits,
            "digits": [0] * 81,
            "candidate_values": [[] for _ in range(81)],
        }
    )
    stream = StringIO(text)

    reader = JsonReader()

    # ACT
    grid = reader.read(stream)

    # ASSERT
    assert grid._puzzle_digits[0] == 1
    assert grid._puzzle_digits[1] == 2
    assert grid._puzzle_digits[2] == 3
    assert all(digit == 0 for digit in grid._puzzle_digits[3:])


def test_leaves_empty_puzzle_cells_unset():
    # ARRANGE
    text = json.dumps(
        {
            "puzzle_digits": [0] * 81,
            "digits": [0] * 81,
            "candidate_values": [[] for _ in range(81)],
        }
    )
    stream = StringIO(text)

    reader = JsonReader()

    # ACT
    grid = reader.read(stream)

    # ASSERT
    assert all(digit == 0 for digit in grid._puzzle_digits)


def test_reads_digits_into_correct_cells():
    # ARRANGE
    digits = [0] * 81
    digits[0] = 1
    digits[Cell(4, 4).index] = 5
    digits[Cell(8, 8).index] = 9

    text = json.dumps(
        {
            "puzzle_digits": [0] * 81,
            "digits": digits,
            "candidate_values": [[] for _ in range(81)],
        }
    )
    stream = StringIO(text)

    reader = JsonReader()

    # ACT
    grid = reader.read(stream)

    # ASSERT
    assert grid._digits[Cell(0, 0).index] == 1
    assert grid._digits[Cell(4, 4).index] == 5
    assert grid._digits[Cell(8, 8).index] == 9


def test_reads_candidate_values_into_correct_cells():
    # ARRANGE
    candidate_values = [[] for _ in range(81)]
    candidate_values[Cell(0, 0).index] = [1, 2, 3]
    candidate_values[Cell(4, 4).index] = [4, 5, 6]
    candidate_values[Cell(8, 8).index] = [7, 8, 9]

    text = json.dumps(
        {
            "puzzle_digits": [0] * 81,
            "digits": [0] * 81,
            "candidate_values": candidate_values,
        }
    )
    stream = StringIO(text)

    reader = JsonReader()

    # ACT
    grid = reader.read(stream)

    # ASSERT
    assert grid._candidates[Cell(0, 0).index] == 0b000000111
    assert grid._candidates[Cell(4, 4).index] == 0b000111000
    assert grid._candidates[Cell(8, 8).index] == 0b111000000
