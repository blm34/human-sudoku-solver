from unittest.mock import Mock

from grid.cell import Cell
from grid.modifier import GridModifier
from grid.state import GridState
from grid.utils import digit_mask
from strategy.deduction import DigitDeduction, EliminationDeduction


class TestGridModifier:
    def test_write_value_stores_value(self):
        # ARRANGE
        grid = GridState.create_empty()
        modifier = GridModifier(grid)
        cell = Cell(3, 4)

        # ACT
        modifier.write_value(7, cell)

        # ASSERT
        assert grid._values[cell.index] == 7

    def test_write_value_removes_candidate_from_peers(self):
        # ARRANGE
        target = Cell(4, 4)
        peer = Cell(4, 5)
        unrelated = Cell(0, 0)
        digit = 7

        iterator = Mock()
        iterator.peers.return_value = (peer,)

        grid = GridState.create_empty()
        modifier = GridModifier(grid, iterator)

        # ACT
        modifier.write_value(digit, target)

        # ASSERT
        mask = digit_mask(7)
        assert not grid._candidates[peer.index] & mask
        assert grid._candidates[unrelated.index] & mask

    def test_write_value_sets_targets_candidates_to_zero(self):
        # ARRANGE
        grid = GridState.create_empty()
        modifier = GridModifier(grid)
        cell = Cell(0, 0)

        # ACT
        modifier.write_value(7, cell)

        # ASSERT
        assert grid._candidates[cell.index] == 0

    def test_write_value_removes_candidate_from_row_peer(self):
        # ARRANGE
        grid = GridState.create_empty()
        modifier = GridModifier(grid)

        target = Cell(0, 0)
        peer = Cell(0, 8)
        digit = 5

        # ACT
        modifier.write_value(digit, target)

        # ASSERT
        mask = digit_mask(digit)
        assert not grid._candidates[peer.index] & mask

    def test_write_value_removes_candidate_from_column_peer(self):
        # ARRANGE
        grid = GridState.create_empty()
        modifier = GridModifier(grid)

        target = Cell(0, 0)
        peer = Cell(8, 0)
        digit = 5

        # ACT
        modifier.write_value(digit, target)

        # ASSERT
        mask = digit_mask(digit)
        assert not grid._candidates[peer.index] & mask

    def test_write_value_removes_candidate_from_box_peer(self):
        # ARRANGE
        grid = GridState.create_empty()
        modifier = GridModifier(grid)

        target = Cell(0, 0)
        peer = Cell(2, 2)
        digit = 5

        # ACT
        modifier.write_value(digit, target)

        # ASSERT
        mask = digit_mask(digit)
        assert not grid._candidates[peer.index] & mask

    def test_write_value_doesnt_remove_candidate_from_unrelated_cell(self):
        # ARRANGE
        grid = GridState.create_empty()
        modifier = GridModifier(grid)

        target = Cell(0, 0)
        unrelated = Cell(3, 3)
        digit = 5

        # ACT
        modifier.write_value(digit, target)

        # ASSERT
        mask = digit_mask(digit)
        assert grid._candidates[unrelated.index] & mask

    def test_remove_candidate_removes_a_candidate(self):
        # ARRANGE
        cell = Cell(6, 5)

        grid = GridState.create_empty()
        grid._candidates[cell.index] = 0b110011001
        modifier = GridModifier(grid)

        # ACT
        modifier.remove_candidate(4, cell)

        # ASSERT
        assert grid._candidates[cell.index] == 0b110010001

    def test_add_candidate_adds_a_candidate(self):
        # ARRANGE
        cell = Cell(6, 5)

        grid = GridState.create_empty()
        grid._candidates[cell.index] = 0b110011001
        modifier = GridModifier(grid)

        # ACT
        modifier.add_candidate(7, cell)

        # ASSERT
        assert grid._candidates[cell.index] == 0b111011001

    def test_apply_with_a_digit_deduction_adds_the_value(self):
        # ARRANGE
        cell = Cell(7, 1)
        value = 3
        deduction = DigitDeduction("strategy", "explanation", cell, value)

        grid = GridState.create_empty()
        modifier = GridModifier(grid)

        # ACT
        modifier.apply(deduction)

        # Assert
        assert grid._values[cell.index] == value

    def test_apply_elimination_deduction_with_one_elimination(self):
        # ARRANGE
        cell = Cell(2, 7)
        deduction = EliminationDeduction("", "", [(cell, 5)])

        grid = GridState.create_empty()
        modifier = GridModifier(grid)

        # ACT
        modifier.apply(deduction)

        # ASSERT
        assert grid._candidates[cell.index] == 0b111101111

    def test_apply_elimination_deduction_with_multiple_eliminations(self):
        # ARRANGE
        cell_1 = Cell(2, 7)
        cell_2 = Cell(1, 8)
        eliminations = [
            (cell_1, 1),
            (cell_1, 2),
            (cell_1, 3),
            (cell_2, 8),
        ]
        deduction = EliminationDeduction("", "", eliminations)

        grid = GridState.create_empty()
        modifier = GridModifier(grid)

        # ACT
        modifier.apply(deduction)

        # ASSERT
        assert grid._candidates[cell_1.index] == 0b111111000
        assert grid._candidates[cell_2.index] == 0b101111111
