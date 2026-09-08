from unittest.mock import Mock

import pytest

from sudoku_strategy.grid.cell import Cell, CellIterators, Cells


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


class TestCells:
    def test_empty_cells_contains_no_cells(self):
        # ARRANGE
        cells = Cells(0)

        # ACT
        result = list(cells)

        # ASSERT
        assert result == []

    def test_cells_contains_single_cell(self):
        # ARRANGE
        cell = Cell(4, 4)
        cells = Cells(1 << cell.index)

        # ACT
        result = list(cells)

        # ASSERT
        assert result == [cell]

    def test_cells_contains_expected_cells(self):
        # ARRANGE
        expected_cells = [
            Cell(0, 0),
            Cell(1, 4),
            Cell(4, 8),
            Cell(8, 3),
        ]
        mask = sum(1 << cell.index for cell in expected_cells)
        cells = Cells(mask)

        # ACT
        result = list(cells)

        # ASSERT
        assert result == expected_cells

    def test_cells_iteration_is_reusable(self):
        # ARRANGE
        cells = Cells(
            (1 << Cell(0, 0).index) | (1 << Cell(4, 4).index) | (1 << Cell(8, 8).index)
        )

        # ACT
        first_iteration = list(cells)
        second_iteration = list(cells)

        # ASSERT
        assert first_iteration == second_iteration

    def test_add_adds_cell(self):
        # ARRANGE
        cells = Cells(0)
        cell = Cell(4, 4)

        # ACT
        cells.add(cell)

        # ASSERT
        assert list(cells) == [cell]

    def test_add_does_not_remove_existing_cells(self):
        # ARRANGE
        existing_cell = Cell(0, 0)
        new_cell = Cell(8, 8)
        cells = Cells(1 << existing_cell.index)

        # ACT
        cells.add(new_cell)

        # ASSERT
        assert set(cells) == {existing_cell, new_cell}

    def test_remove_removes_cell(self):
        # ARRANGE
        cell = Cell(4, 4)
        cells = Cells(1 << cell.index)

        # ACT
        cells.remove(cell)

        # ASSERT
        assert list(cells) == []

    def test_remove_does_not_remove_other_cells(self):
        # ARRANGE
        remaining_cell = Cell(0, 0)
        removed_cell = Cell(8, 8)
        mask = (1 << remaining_cell.index) | (1 << removed_cell.index)
        cells = Cells(mask)

        # ACT
        cells.remove(removed_cell)

        # ASSERT
        assert list(cells) == [remaining_cell]

    def test_and_returns_intersection(self):
        # ARRANGE
        first = Cells(
            (1 << Cell(0, 0).index) | (1 << Cell(4, 4).index) | (1 << Cell(8, 8).index)
        )
        second = Cells(
            (1 << Cell(0, 0).index) | (1 << Cell(1, 1).index) | (1 << Cell(8, 8).index)
        )

        # ACT
        result = first & second

        # ASSERT
        assert list(result) == [
            Cell(0, 0),
            Cell(8, 8),
        ]

    def test_or_returns_union(self):
        # ARRANGE
        first = Cells((1 << Cell(0, 0).index) | (1 << Cell(4, 4).index))
        second = Cells((1 << Cell(4, 4).index) | (1 << Cell(8, 8).index))

        # ACT
        result = first | second

        # ASSERT
        assert list(result) == [
            Cell(0, 0),
            Cell(4, 4),
            Cell(8, 8),
        ]

    def test_invert_returns_complement(self):
        # ARRANGE
        cell = Cell(4, 4)
        cells = Cells(1 << cell.index)

        # ACT
        result = ~cells

        # ASSERT
        assert len(list(result)) == 80
        assert cell not in result

    def test_invert_of_empty_cells_contains_all_81_cells(self):
        # ARRANGE
        cells = Cells(0)

        # ACT
        result = ~cells

        # ASSERT
        assert len(list(result)) == 81
        assert set(result) == {Cell.from_index(index) for index in range(81)}

    def test_invert_of_all_cells_contains_no_cells(self):
        # ARRANGE
        cells = Cells(Cells._MASK)

        # ACT
        result = ~cells

        # ASSERT
        assert list(result) == []

    def test_len_gives_number_of_cells(self):
        # ARRANGE
        mask = (
            (1 << Cell(0, 0).index) | (1 << Cell(4, 4).index) | (1 << Cell(8, 8).index)
        )
        cells = Cells(mask)

        # ACT
        length = len(cells)

        # ASSERT
        assert length == 3

    def test_contians_checks_cell_is_in_cells(self):
        # ARRANGE
        cell = Cell(5, 3)
        mask = 1 << cell.index
        cells = Cells(mask)

        # ACT
        contains = cell in cells

        # ASSERT
        assert contains

    def test_contians_checks_cell_is_not_in_cells(self):
        # ARRANGE
        cell = Cell(5, 3)
        other_cell = Cell(4, 2)
        mask = 1 << cell.index
        cells = Cells(mask)

        # ACT
        contains = other_cell in cells

        # ASSERT
        assert not contains


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
        grid.cell_empty.return_value = True
        iterator = CellIterators(grid)

        # ACT
        cells = iterator.empty_cells()

        # ASSERT
        assert len(cells) == 81

    def test_empty_cells_returns_no_cells_when_all_filled(self):
        # ARRANGE
        grid = Mock()
        grid.cell_empty.return_value = False

        iterator = CellIterators(grid)

        # ACT
        cells = iterator.empty_cells()

        # ASSERT
        assert len(cells) == 0

    def test_empty_cells_only_returns_empty_cells(self):
        # ARRANGE
        grid = Mock()
        filled_cell = Cell(5, 5)
        grid.cell_empty = lambda cell: cell != filled_cell
        iterator = CellIterators(grid)

        # ACT
        cells = iterator.empty_cells()

        # ASSERT
        assert len(cells) == 80
        assert filled_cell not in cells

    def test_filled_cells_returns_filled_cells(self):
        # ARRANGE
        grid = Mock()
        filled_cells = [
            Cell(0, 6),
            Cell(2, 1),
            Cell(5, 5),
            Cell(7, 6),
            Cell(8, 4),
        ]
        grid.cell_empty = lambda cell: cell not in filled_cells
        iterator = CellIterators(grid)

        # ACT
        cells = iterator.filled_cells()

        # ASSERT
        assert len(cells) == len(filled_cells)
        assert all(cell in filled_cells for cell in cells)

    @pytest.mark.parametrize(
        "row, col, string",
        (
            (0, 0, "R1C1"),
            (8, 8, "R9C9"),
            (0, 5, "R1C6"),
            (7, 2, "R8C3"),
        ),
    )
    def test_string_gives_expected_representation(self, row, col, string):
        # ARRANGE
        cell = Cell(row, col)

        # ACT
        cell_str = str(cell)

        # ASSERT
        assert cell_str == string
