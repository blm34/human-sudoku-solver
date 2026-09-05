from unittest.mock import Mock

from grid.cell import Cell
from grid.modifier import GridModifier
from grid.state import GridState
from grid.utils import ALL_DIGITS, digit_mask
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
        grid._candidates = [ALL_DIGITS] * 81
        modifier = GridModifier(grid, iterator)

        # ACT
        modifier.write_value(digit, target)

        # ASSERT
        mask = digit_mask(7)
        assert not grid.candidates(peer) & mask
        assert grid.candidates(unrelated) & mask

    def test_write_value_sets_targets_candidates_to_zero(self):
        # ARRANGE
        grid = GridState.create_empty()
        modifier = GridModifier(grid)
        cell = Cell(0, 0)

        # ACT
        modifier.write_value(7, cell)

        # ASSERT
        assert grid.candidates(cell) == 0

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
        assert not grid.candidates(peer) & mask

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
        assert not grid.candidates(peer) & mask

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
        assert not grid.candidates(peer) & mask

    def test_write_value_doesnt_remove_candidate_from_unrelated_cell(self):
        # ARRANGE
        grid = GridState.create_empty()
        grid._candidates = [ALL_DIGITS] * 81
        modifier = GridModifier(grid)

        target = Cell(0, 0)
        unrelated = Cell(3, 3)
        digit = 5

        # ACT
        modifier.write_value(digit, target)

        # ASSERT
        mask = digit_mask(digit)
        assert grid.candidates(unrelated) & mask

    def test_remove_candidate_removes_a_candidate(self):
        # ARRANGE
        cell = Cell(6, 5)

        grid = GridState.create_empty()
        grid._candidates[cell.index] = 0b110011001
        modifier = GridModifier(grid)

        # ACT
        modifier.remove_candidate(4, cell)

        # ASSERT
        assert grid.candidates(cell) == 0b110010001

    def test_add_candidate_adds_a_candidate(self):
        # ARRANGE
        cell = Cell(6, 5)

        grid = GridState.create_empty()
        grid._candidates[cell.index] = 0b110011001
        modifier = GridModifier(grid)

        # ACT
        modifier.add_candidate(7, cell)

        # ASSERT
        assert grid.candidates(cell) == 0b111011001

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
        grid._candidates[cell.index] = ALL_DIGITS
        modifier = GridModifier(grid)

        # ACT
        modifier.apply(deduction)

        # ASSERT
        assert grid.candidates(cell) == 0b111101111

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
        grid._candidates = [ALL_DIGITS] * 81
        modifier = GridModifier(grid)

        # ACT
        modifier.apply(deduction)

        # ASSERT
        assert grid.candidates(cell_1) == 0b111111000
        assert grid.candidates(cell_2) == 0b101111111

    def test_compute_candidates_on_an_empty_grid_gives_all_candidates(self):
        # ARRANGE
        grid = GridState.create_empty()
        modifier = GridModifier(grid)

        # ACT
        modifier.compute_candidates()

        # ASSERT
        assert all(candidates == ALL_DIGITS for candidates in grid._candidates)

    def test_compute_candidates_sets_candidates_to_none_in_cells_with_values(self):
        # ARRANGE
        cell = Cell(5, 5)
        grid = GridState.create_empty()
        grid.write_value(cell, 4)
        modifier = GridModifier(grid)

        # ACT
        modifier.compute_candidates()

        # ASSERT
        assert grid.candidates(cell) == 0

    def test_compute_candidates_removes_candidate_from_peers(self):
        # ARRANGE
        cell = Cell(4, 4)
        grid = GridState.create_empty()
        grid.write_value(cell, 4)
        modifier = GridModifier(grid)

        peers = [Cell(0, 4), Cell(4, 0), Cell(5, 5)]

        # ACT
        modifier.compute_candidates()

        # ASSERT
        assert all(grid.candidates(cell) == 0b111110111 for cell in peers)

    def test_compute_candidates_removes_multiple_candidates_from_cell(self):
        # ARRANGE
        cell = Cell(5, 5)
        grid = GridState.create_empty()
        grid.write_value(Cell(0, 5), 1)
        grid.write_value(Cell(5, 0), 2)
        modifier = GridModifier(grid)

        # ACT
        modifier.compute_candidates()

        # ASSERT
        assert grid.candidates(cell) == 0b111111100
