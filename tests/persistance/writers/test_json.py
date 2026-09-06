import json
from io import StringIO

from sudoku_strategy.grid import Cell, GridModifier, GridState
from sudoku_strategy.persistance.writers.json import JsonWriter


def test_writes_puzzle_values():
    # ARRANGE
    puzzle_values = [1, 2, 3] + [0] * 78
    grid = GridState.new_puzzle(tuple(puzzle_values))
    stream = StringIO()

    writer = JsonWriter()

    # ACT
    writer.write(grid, stream)

    # ASSERT
    grid_dict = json.loads(stream.getvalue())

    assert grid_dict["puzzle_values"] == puzzle_values


def test_writes_values_into_correct_cells():
    # ARRANGE
    grid = GridState.create_empty()
    modifier = GridModifier(grid)

    modifier.write_value(1, Cell(0, 0))
    modifier.write_value(5, Cell(4, 4))
    modifier.write_value(9, Cell(8, 8))

    stream = StringIO()

    writer = JsonWriter()

    # ACT
    writer.write(grid, stream)

    # ASSERT
    grid_dict = json.loads(stream.getvalue())

    assert grid_dict["values"][Cell(0, 0).index] == 1
    assert grid_dict["values"][Cell(4, 4).index] == 5
    assert grid_dict["values"][Cell(8, 8).index] == 9


def test_writes_empty_values_as_zero():
    # ARRANGE
    grid = GridState.create_empty()
    stream = StringIO()

    writer = JsonWriter()

    # ACT
    writer.write(grid, stream)

    # ASSERT
    grid_dict = json.loads(stream.getvalue())

    assert all(value == 0 for value in grid_dict["values"])


def test_writes_candidate_values_into_correct_cells():
    # ARRANGE
    grid = GridState.create_empty()
    grid._candidates[Cell(0, 0).index] = 0b000000111
    grid._candidates[Cell(4, 4).index] = 0b000111000
    grid._candidates[Cell(8, 8).index] = 0b111000000

    stream = StringIO()

    writer = JsonWriter()

    # ACT
    writer.write(grid, stream)

    # ASSERT
    grid_dict = json.loads(stream.getvalue())

    assert grid_dict["candidate_values"][Cell(0, 0).index] == [1, 2, 3]
    assert grid_dict["candidate_values"][Cell(4, 4).index] == [4, 5, 6]
    assert grid_dict["candidate_values"][Cell(8, 8).index] == [7, 8, 9]


def test_writes_empty_candidate_values_as_empty_lists():
    # ARRANGE
    grid = GridState.create_empty()
    stream = StringIO()

    writer = JsonWriter()

    # ACT
    writer.write(grid, stream)

    # ASSERT
    grid_dict = json.loads(stream.getvalue())

    assert all(candidate_list == [] for candidate_list in grid_dict["candidate_values"])


def test_writes_all_grid_data():
    # ARRANGE
    puzzle_values = [0] * 81
    puzzle_values[0] = 1
    puzzle_values[40] = 5

    grid = GridState.new_puzzle(tuple(puzzle_values))
    modifier = GridModifier(grid)

    modifier.write_value(2, Cell(0, 1))
    modifier.write_value(9, Cell(8, 8))

    modifier.add_candidates([3, 4, 5], Cell(1, 1))
    modifier.add_candidates([6, 7, 8], Cell(7, 7))

    stream = StringIO()

    writer = JsonWriter()

    # ACT
    writer.write(grid, stream)

    # ASSERT
    grid_dict = json.loads(stream.getvalue())

    assert grid_dict["puzzle_values"] == puzzle_values

    assert grid_dict["values"][Cell(0, 0).index] == 1
    assert grid_dict["values"][Cell(0, 1).index] == 2
    assert grid_dict["values"][Cell(4, 4).index] == 5
    assert grid_dict["values"][Cell(8, 8).index] == 9

    assert grid_dict["candidate_values"][Cell(1, 1).index] == [3, 4, 5]
    assert grid_dict["candidate_values"][Cell(7, 7).index] == [6, 7, 8]
