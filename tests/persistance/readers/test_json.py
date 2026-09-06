import json
from io import StringIO

from sudoku_lib.grid import Cell
from sudoku_lib.persistance.readers.json import JsonReader


def test_reads_puzzle_values():
    # ARRANGE
    puzzle_values = [1, 2, 3] + [0] * 78
    text = json.dumps(
        {
            "puzzle_values": puzzle_values,
            "values": [0] * 81,
            "candidate_values": [[] for _ in range(81)],
        }
    )
    stream = StringIO(text)

    reader = JsonReader()

    # ACT
    grid = reader.read(stream)

    # ASSERT
    assert grid._puzzle_values[0] == 1
    assert grid._puzzle_values[1] == 2
    assert grid._puzzle_values[2] == 3
    assert all(value == 0 for value in grid._puzzle_values[3:])


def test_leaves_empty_puzzle_cells_unset():
    # ARRANGE
    text = json.dumps(
        {
            "puzzle_values": [0] * 81,
            "values": [0] * 81,
            "candidate_values": [[] for _ in range(81)],
        }
    )
    stream = StringIO(text)

    reader = JsonReader()

    # ACT
    grid = reader.read(stream)

    # ASSERT
    assert all(value == 0 for value in grid._puzzle_values)


def test_reads_values_into_correct_cells():
    # ARRANGE
    values = [0] * 81
    values[0] = 1
    values[Cell(4, 4).index] = 5
    values[Cell(8, 8).index] = 9

    text = json.dumps(
        {
            "puzzle_values": [0] * 81,
            "values": values,
            "candidate_values": [[] for _ in range(81)],
        }
    )
    stream = StringIO(text)

    reader = JsonReader()

    # ACT
    grid = reader.read(stream)

    # ASSERT
    assert grid._values[Cell(0, 0).index] == 1
    assert grid._values[Cell(4, 4).index] == 5
    assert grid._values[Cell(8, 8).index] == 9


def test_reads_candidate_values_into_correct_cells():
    # ARRANGE
    candidate_values = [[] for _ in range(81)]
    candidate_values[Cell(0, 0).index] = [1, 2, 3]
    candidate_values[Cell(4, 4).index] = [4, 5, 6]
    candidate_values[Cell(8, 8).index] = [7, 8, 9]

    text = json.dumps(
        {
            "puzzle_values": [0] * 81,
            "values": [0] * 81,
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
