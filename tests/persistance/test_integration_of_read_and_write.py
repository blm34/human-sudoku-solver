from io import StringIO

from sudoku_strategy.grid import GridState
from sudoku_strategy.persistance.readers import JsonReader, SusserReader
from sudoku_strategy.persistance.writers import JsonWriter, SusserWriter


def test_susser_round_trip():
    # ARRANGE
    original = GridState.create_empty()
    original._values = list(range(1, 10)) * 9

    stream = StringIO()

    # ACT
    SusserWriter().write(original, stream)

    stream.seek(0)

    result = SusserReader().read(stream)

    # ASSERT
    assert result._values == original._values


def test_json_round_trip():
    # ARRANGE
    puzzle_values = [0] * 81
    for val, idx in enumerate(range(0, 81, 10), start=1):
        puzzle_values[idx] = val

    original = GridState.new_puzzle(tuple(puzzle_values))

    original._values[1] = 4
    original._values[2] = 5
    original._values[9] = 6

    original._candidates[3] = 0b111100110
    original._candidates[4] = 0b111100110
    original._candidates[5] = 0b111100110

    stream = StringIO()

    # ACT
    JsonWriter().write(original, stream)
    stream.seek(0)

    result = JsonReader().read(stream)

    # ASSERT
    assert result._values == original._values
