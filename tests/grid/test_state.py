from unittest.mock import Mock

from grid.state import GridState
from grid.cell import Cell, CellIterators
from grid.utils import ALL_DIGITS, digit_mask


class TestGridStateState:
    def test_initialises_empty_grid_of_values(self):
        # ARRANGE
        grid = GridState()

        # ASSERT
        assert len(grid.values) == 81
        assert all(value == 0 for value in grid.values)

    def test_initialises_empty_grid_of_candidates(self):
        # ARRANGE
        grid = GridState()

        # ASSERT
        assert len(grid.candidates) == 81
        assert all(candidates == ALL_DIGITS for candidates in grid.candidates)

    def test_uses_supplied_cell_relations(self):
        # ARRANGE
        relations = Mock(spec=CellIterators)

        # ACT
        grid = GridState(relations)

        # ASSERT
        assert grid._cell_iterators is relations

    def test_creates_cell_relations_when_none_supplied(self):
        # ACT
        grid = GridState()

        # ASSERT
        assert isinstance(grid._cell_iterators, CellIterators)

    def test_write_value_stores_value(self):
        # ARRANGE
        grid = GridState()
        cell = Cell(3, 4)

        # ACT
        grid.write_value(7, cell)

        # ASSERT
        assert grid.values[cell.index] == 7

    def test_write_value_removes_candidate_from_peers(self):
        # ARRANGE
        target = Cell(4, 4)
        peer = Cell(4, 5)
        unrelated = Cell(0, 0)
        digit = 7

        iterator = Mock(spec=CellIterators)
        iterator.peers.return_value = (peer,)

        grid = GridState(iterator)

        # ACT
        grid.write_value(digit, target)

        # ASSERT
        mask = digit_mask(7)
        assert not grid.candidates[peer.index] & mask
        assert grid.candidates[unrelated.index] & mask

    def test_write_value_sets_targets_candidates_to_zero(self):
        # ARRANGE
        grid = GridState()
        cell = Cell(0, 0)

        # ACT
        grid.write_value(7, cell)

        # ASSERT
        assert grid.candidates[cell.index] == 0

    def test_candidate_removed_from_row_peer(self):
        # ARRANGE
        grid = GridState()

        target = Cell(0, 0)
        peer = Cell(0, 8)
        digit = 5

        # ACT
        grid.write_value(digit, target)

        # ASSERT
        mask = digit_mask(digit)
        assert not grid.candidates[peer.index] & mask

    def test_candidate_removed_from_column_peer(self):
        # ARRANGE
        grid = GridState()

        target = Cell(0, 0)
        peer = Cell(8, 0)
        digit = 5

        # ACT
        grid.write_value(digit, target)

        # ASSERT
        mask = digit_mask(digit)
        assert not grid.candidates[peer.index] & mask

    def test_candidate_removed_from_box_peer(self):
        # ARRANGE
        grid = GridState()

        target = Cell(0, 0)
        peer = Cell(2, 2)
        digit = 5

        # ACT
        grid.write_value(digit, target)

        # ASSERT
        mask = digit_mask(digit)
        assert not grid.candidates[peer.index] & mask

    def test_candidate_remains_in_unrelated_cell(self):
        # ARRANGE
        grid = GridState()

        target = Cell(0, 0)
        unrelated = Cell(3, 3)
        digit = 5

        # ACT
        grid.write_value(digit, target)

        # ASSERT
        mask = digit_mask(digit)
        assert grid.candidates[unrelated.index] & mask
