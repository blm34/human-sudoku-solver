from unittest.mock import Mock

import pytest

from sudoku_lib.grid.cell import Cell
from sudoku_lib.grid.modifier import GridModifier
from sudoku_lib.grid.state import GridState
from sudoku_lib.grid.utils import ALL_DIGITS, digit_mask
from sudoku_lib.strategy.deduction import DigitDeduction, EliminationDeduction


class TestGridModifier:
    def test_add_value_writes_the_value_to_the_cell(self):
        # ARRANGE
        grid = GridState.create_empty()
        modifier = GridModifier(grid)
        modifier.write_value = Mock()

        value = 5
        cell = Cell(4, 6)

        # ACT
        modifier.add_value(value, cell)

        # ASSERT
        modifier.write_value.assert_called_once_with(value, cell)

    def test_add_value_eliminates_the_relevant_candidates(self):
        # ARRANGE
        grid = GridState.create_empty()
        modifier = GridModifier(grid)
        modifier.update_candidates = Mock()

        value = 5
        cell = Cell(4, 6)

        # ACT
        modifier.add_value(value, cell)

        # ASSERT
        modifier.update_candidates.assert_called_once_with(value, cell)

    def test_write_value_stores_value(self):
        # ARRANGE
        grid = GridState.create_empty()
        modifier = GridModifier(grid)
        cell = Cell(3, 4)

        # ACT
        modifier.write_value(7, cell)

        # ASSERT
        assert grid._values[cell.index] == 7

    def test_update_candidates_removes_candidate_from_peers(self):
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
        modifier.update_candidates(digit, target)

        # ASSERT
        mask = digit_mask(7)
        assert not grid.candidates(peer) & mask
        assert grid.candidates(unrelated) & mask

    def test_update_candidates_sets_targets_candidates_to_zero(self):
        # ARRANGE
        grid = GridState.create_empty()
        modifier = GridModifier(grid)
        cell = Cell(0, 0)

        # ACT
        modifier.update_candidates(7, cell)

        # ASSERT
        assert grid.candidates(cell) == 0

    def test_update_candidates_removes_candidate_from_row_peer(self):
        # ARRANGE
        grid = GridState.create_empty()
        modifier = GridModifier(grid)

        target = Cell(0, 0)
        peer = Cell(0, 8)
        digit = 5

        # ACT
        modifier.update_candidates(digit, target)

        # ASSERT
        mask = digit_mask(digit)
        assert not grid.candidates(peer) & mask

    def test_update_candidates_removes_candidate_from_column_peer(self):
        # ARRANGE
        grid = GridState.create_empty()
        modifier = GridModifier(grid)

        target = Cell(0, 0)
        peer = Cell(8, 0)
        digit = 5

        # ACT
        modifier.update_candidates(digit, target)

        # ASSERT
        mask = digit_mask(digit)
        assert not grid.candidates(peer) & mask

    def test_update_candidates_removes_candidate_from_box_peer(self):
        # ARRANGE
        grid = GridState.create_empty()
        modifier = GridModifier(grid)

        target = Cell(0, 0)
        peer = Cell(2, 2)
        digit = 5

        # ACT
        modifier.update_candidates(digit, target)

        # ASSERT
        mask = digit_mask(digit)
        assert not grid.candidates(peer) & mask

    def test_update_candidates_doesnt_remove_candidate_from_unrelated_cell(self):
        # ARRANGE
        grid = GridState.create_empty()
        grid._candidates = [ALL_DIGITS] * 81
        modifier = GridModifier(grid)

        target = Cell(0, 0)
        unrelated = Cell(3, 3)
        digit = 5

        # ACT
        modifier.update_candidates(digit, target)

        # ASSERT
        mask = digit_mask(digit)
        assert grid.candidates(unrelated) & mask

    @pytest.mark.parametrize(
        "values, expected_mask",
        (
            ((1, 2, 3), 0b000000111),
            ((4, 5, 6), 0b000111000),
            ((7, 8, 9), 0b111000000),
            ((1,), 0b000000001),
            ((1, 3, 5, 7, 9), 0b101010101),
            ((1, 2, 3, 4, 5, 6, 7, 8, 9), 0b111111111),
            ((), 0b000000000),
        ),
    )
    def test_get_candidate_mask(self, values, expected_mask):
        # ARRANGE
        grid = Mock()
        modifier = GridModifier(grid)

        # ACT
        mask = modifier._get_candidate_mask(values)

        # ASSERT
        assert mask == expected_mask

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

    def test_remove_candidates_removes_multiple_candidates(self):
        # ARRANGE
        cell = Cell(4, 4)

        grid = GridState.create_empty()
        grid._candidates[cell.index] = ALL_DIGITS
        modifier = GridModifier(grid)

        # ACT
        modifier.remove_candidates((5, 6, 7), cell)

        # ASSERT
        assert grid._candidates[cell.index] == 0b110001111

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

    def test_add_candidates_adds_multiple_candidates(self):
        # ARRANGE
        cell = Cell(4, 4)

        grid = GridState.create_empty()
        modifier = GridModifier(grid)

        # ACT
        modifier.add_candidates((5, 6, 7), cell)

        # ASSERT
        assert grid._candidates[cell.index] == 0b001110000

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
