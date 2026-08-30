from unittest.mock import Mock

import pytest

from grid.cell import Cell, CellIterators


class TestCell:
    @pytest.mark.parametrize(
        ("row", "col", "expected_index"),
        [
            (0, 0, 0),
            (0, 8, 8),
            (1, 0, 9),
            (4, 4, 40),
            (8, 0, 72),
            (8, 8, 80),
        ],
    )
    def test_index(self, row, col, expected_index):
        # ARRANGE
        cell = Cell(row, col)

        # ACT
        index = cell.index

        # ASSERT
        assert index == expected_index

    @pytest.mark.parametrize(
        ("index", "expected_row", "expected_col"),
        [
            (0, 0, 0),
            (8, 0, 8),
            (9, 1, 0),
            (40, 4, 4),
            (72, 8, 0),
            (80, 8, 8),
        ],
    )
    def test_from_index(self, index, expected_row, expected_col):
        # ACT
        cell = Cell.from_index(index)

        # ASSERT
        assert cell.row == expected_row
        assert cell.col == expected_col

    @pytest.mark.parametrize(
        ("row", "col", "expected_box"),
        [
            (0, 0, 0),
            (0, 2, 0),
            (0, 3, 1),
            (2, 8, 2),
            (3, 0, 3),
            (4, 4, 4),
            (5, 8, 5),
            (6, 0, 6),
            (8, 8, 8),
        ],
    )
    def test_box(self, row, col, expected_box):
        # ARRANGE
        cell = Cell(row, col)

        # ACT
        box = cell.box

        # ASSERT
        assert box == expected_box

    @pytest.mark.parametrize(
        ("row", "col"),
        [
            (0, 0),
            (4, 7),
            (8, 8),
        ],
    )
    def test_equal_cells_are_equal(self, row, col):
        # ARRANGE
        first = Cell(row, col)
        second = Cell(row, col)

        # ACT & ASSERT
        assert first == second


class TestCellIterators:
    @pytest.mark.parametrize("row", range(9))
    def test_rows_have_nine_values(self, row):
        # ARRANGE
        iterator = CellIterators(Mock())

        # ACT
        length = len(iterator.row(row))

        # ASSERT
        assert length == 9

    @pytest.mark.parametrize("col", range(9))
    def test_cols_have_with_nine_values(self, col):
        # ARRANGE
        iterator = CellIterators(Mock())

        # ACT
        length = len(iterator.col(col))

        # ASSERT
        assert length == 9

    @pytest.mark.parametrize("box", range(9))
    def test_boxes_have_nine_values(self, box):
        # ARRANGE
        iterator = CellIterators(Mock())

        # ACT
        length = len(iterator.box(box))

        # ASSERT
        assert length == 9

    def test_units_produces_27_units_with_nine_values(self):
        # ARRANGE
        iterator = CellIterators(Mock())

        # ACT
        units = iterator.units()

        # ASSERT
        assert len(units) == 27
        assert all(len(unit) == 9 for unit in units)

    def test_first_row_contains_expected_cells(self):
        # ARRANGE
        iterator = CellIterators(Mock())

        # ACT
        cells = iterator.row(0)

        # ASSERT
        assert [(cell.row, cell.col) for cell in cells] == [
            (0, 0),
            (0, 1),
            (0, 2),
            (0, 3),
            (0, 4),
            (0, 5),
            (0, 6),
            (0, 7),
            (0, 8),
        ]

    def test_first_column_contains_expected_cells(self):
        # ARRANGE
        iterator = CellIterators(Mock())

        # ACT
        cells = iterator.col(0)

        # ASSERT
        assert [(cell.row, cell.col) for cell in cells] == [
            (0, 0),
            (1, 0),
            (2, 0),
            (3, 0),
            (4, 0),
            (5, 0),
            (6, 0),
            (7, 0),
            (8, 0),
        ]

    def test_first_box_contains_expected_cells(self):
        # ARRANGE
        iterator = CellIterators(Mock())

        # ACT
        cells = iterator.box(0)

        # ASSERT
        assert [(cell.row, cell.col) for cell in cells] == [
            (0, 0),
            (0, 1),
            (0, 2),
            (1, 0),
            (1, 1),
            (1, 2),
            (2, 0),
            (2, 1),
            (2, 2),
        ]

    @pytest.mark.parametrize("cell_idx", range(81))
    def test_each_cell_has_20_peers(self, cell_idx):
        # ARRANGE
        iterator = CellIterators(Mock())
        cell = Cell.from_index(cell_idx)

        # ACT
        peers = iterator.peers(cell)
        count = len(peers)

        # ASSERT
        assert count == 20

    @pytest.mark.parametrize(
        ("row", "col"),
        [
            (0, 0),
            (0, 8),
            (4, 4),
            (8, 0),
            (8, 8),
        ],
    )
    def test_cell_is_not_its_own_peer(self, row, col):
        # ARRANGE
        iterator = CellIterators(Mock())
        cell = Cell(row, col)

        # ACT
        peers = iterator.peers(cell)

        # ASSERT
        assert cell not in peers

    def test_cell_peers_share_row_column_or_box(self):
        # ARRANGE
        iterator = CellIterators(Mock())
        cell = Cell(4, 4)

        # ACT
        peers = iterator.peers(cell)

        # ASSERT
        assert all(
            peer.row == cell.row or peer.col == cell.col or peer.box == cell.box
            for peer in peers
        )

    @pytest.mark.parametrize("cell_idx", range(81))
    def test_cell_has_all_20_unique_peers(self, cell_idx):
        # ARRANGE
        iterator = CellIterators(Mock())
        cell = Cell.from_index(cell_idx)

        # ACT
        peers = iterator.peers(cell)
        unique_peers = set(peers)

        # ASSERT
        assert len(unique_peers) == 20

    def test_cells_returns_all_81_cells(self):
        # ARRANGE
        iterator = CellIterators(Mock())

        # ACT
        cells = list(iterator.cells())

        # ASSERT
        assert len(cells) == 81

    def test_empty_cells_returns_all_cells_when_all_empty(self):
        # ARRANGE
        grid = Mock()
        grid.values = [0] * 81
        iterator = CellIterators(grid)

        # ACT
        cells = iterator.empty_cells()

        # ASSERT
        assert len(cells) == 81

    def test_empty_cells_returns_no_cells_when_all_filled(self):
        # ARRANGE
        grid = Mock()
        grid.values = [1] * 81
        iterator = CellIterators(grid)

        # ACT
        cells = iterator.empty_cells()

        # ASSERT
        assert len(cells) == 0

    def test_empty_cells_only_returns_empty_cells(self):
        # ARRANGE
        grid = Mock()
        grid.values = [0] * 81
        grid.values[7] = 1
        iterator = CellIterators(grid)

        # ACT
        cells = iterator.empty_cells()

        # ASSERT
        assert len(cells) == 80
        assert Cell(0, 7) not in cells
