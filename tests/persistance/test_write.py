from unittest.mock import Mock, patch

import pytest

from persistance.write import SudokuFileWriter


def test_saves_grid_using_writer_for_file_type(tmp_path):
    # ARRANGE
    path = tmp_path / "puzzle.ext"
    grid = Mock()

    writer = Mock()

    writers = {".ext": Mock(return_value=writer)}

    with patch(
        "persistance.write.WRITERS",
        writers,
    ):
        file_writer = SudokuFileWriter()

        # ACT
        file_writer.save(grid, path)

    # ASSERT
    writer.write.assert_called_once()


def test_writer_receives_grid_and_file_stream(tmp_path):
    # ARRANGE
    path = tmp_path / "puzzle.ext"
    grid = Mock()

    writer = Mock()

    def write(received_grid, stream):
        assert received_grid is grid
        assert not stream.closed
        assert stream.writable()

    writer.write.side_effect = write

    writers = {".ext": Mock(return_value=writer)}

    with patch(
        "persistance.write.WRITERS",
        writers,
    ):
        file_writer = SudokuFileWriter()

        # ACT
        file_writer.save(grid, path)

    # ASSERT
    writer.write.assert_called_once()


def test_raises_error_when_no_writer_exists(tmp_path):
    # ARRANGE
    path = tmp_path / "puzzle.unknown"
    grid = Mock()

    file_writer = SudokuFileWriter()

    # ACT / ASSERT
    with pytest.raises(ValueError, match="No writer found for files of type .unknown"):
        file_writer.save(grid, path)
