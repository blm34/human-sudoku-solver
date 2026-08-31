from unittest.mock import Mock, patch

import pytest

from persistance.read import SudokuFileReader


def test_loads_grid_using_reader_for_file_type(tmp_path):
    # ARRANGE
    path = tmp_path / "puzzle.ext"
    path.write_text("puzzle")

    expected_grid = Mock()

    reader = Mock()
    reader.read.return_value = expected_grid

    reader_map = {".ext": Mock(return_value=reader)}

    with patch("persistance.read.READERS", reader_map):
        file_reader = SudokuFileReader()

        # ACT
        result = file_reader.load(path)

    # ASSERT
    assert result is expected_grid
    reader.read.assert_called_once()


def test_raises_error_when_no_reader_exists(tmp_path):
    # ARRANGE
    path = tmp_path / "puzzle.unknown"
    path.write_text("puzzle")

    file_reader = SudokuFileReader()

    # ACT / ASSERT
    with pytest.raises(
        ValueError,
        match="No reader found for .unknown file types.",
    ):
        file_reader.load(path)


def test_reader_receives_file_stream(tmp_path):
    # ARRANGE
    path = tmp_path / "puzzle.ext"
    path.write_text("puzzle")

    reader = Mock()

    def mock_read(stream):
        assert stream.read() == "puzzle"
        return Mock()

    reader.read.side_effect = mock_read

    reader_map = {".ext": Mock(return_value=reader)}

    with patch(
        "persistance.read.READERS",
        reader_map,
    ):
        file_reader = SudokuFileReader()

        # ACT
        file_reader.load(path)

    # ASSERT
    reader.read.assert_called_once
