import pytest

from grid.cell import Cell
from grid.state import GridState
from grid.utils import ALL_DIGITS, digit_mask


class TestGridState:
    def test_create_empty_initialises_empty_grid_of_values(self):
        # ACT
        grid = GridState.create_empty()

        # ASSERT
        assert len(grid._values) == 81
        assert all(value == 0 for value in grid._values)

    def test_create_empty_initialises_empty_grid_of_candidates(self):
        # ACT
        grid = GridState.create_empty()

        # ASSERT
        assert len(grid._candidates) == 81
        assert all(candidates == 0 for candidates in grid._candidates)

    def test_create_empty_initialises_empty_grid_of_puzzle_values(self):
        # ACT
        grid = GridState.create_empty()

        # ASSERT
        assert len(grid._puzzle_values) == 81
        assert all(value == 0 for value in grid._puzzle_values)

    def test_new_puzzle_adds_values_to_values(self):
        # ARRANGE
        values = [0] * 81
        values[8] = 1
        values = tuple(values)

        # ACT
        grid = GridState.new_puzzle(values)

        # ASSERT
        assert grid._values.count(0) == 80
        assert grid._values[8] == 1

    def test_new_puzzle_sets_all_candidates_to_zero(self):
        # ARRANGE
        values = (0,) * 81

        # ACT
        grid = GridState.new_puzzle(values)

        # ASSERT
        assert len(grid._candidates) == 81
        assert all(candidates == 0 for candidates in grid._candidates)

    def test_new_puzzle_sets_puzzle_values_correctly(self):
        # ARRANGE
        values = [0] * 81
        values[8] = 1
        values = tuple(values)

        # ACT
        grid = GridState.new_puzzle(values)

        # ASSERT
        assert grid._puzzle_values.count(0) == 80
        assert grid._puzzle_values[8] == 1

    @pytest.mark.parametrize("length", (10, 80, 82, 100))
    def test_new_puzzle_raises_error_when_given_wrong_number_of_values(self, length):
        # ARRANGE
        values = (0,) * length

        with pytest.raises(ValueError):
            # ACT
            GridState.new_puzzle(values)

    def test_value_returns_value_in_given_cell(self):
        # ARRANGE
        grid = GridState.create_empty()
        idx = 5
        cell = Cell.from_index(idx)
        grid._values[idx] = 9

        # ACT
        value = grid.value(cell)

        # ASSERT
        assert value == 9

    def test_write_value_adds_value_to_array(self):
        # ARRANGE
        grid = GridState.create_empty()
        idx = 5
        cell = Cell.from_index(idx)
        value = 1

        # ACT
        grid.write_value(cell, value)

        # ASSERT
        assert grid._values[idx] == value

    def test_puzzle_value_returns_value_of_original_puzzle(self):
        # ARRANGE
        cell_idx = 4
        cell = Cell.from_index(cell_idx)

        puzzle_values = [0] * 81
        puzzle_values[cell_idx] = 3
        puzzle_values = tuple(puzzle_values)

        grid = GridState.new_puzzle(puzzle_values)
        grid._values[cell_idx] = 5

        # ACT
        puzzle_value = grid.puzzle_value(cell)

        # ASSERT
        assert puzzle_value == 3

    def test_candidates_returns_mask_for_given_cell(self):
        # ARRANGE
        grid = GridState.create_empty()
        idx = 5
        cell = Cell.from_index(idx)
        set_candidates = 0b001100110
        grid._candidates[idx] = set_candidates

        # ACT
        candidates = grid.candidates(cell)

        # ASSERT
        assert candidates == set_candidates

    def test_add_candidates_stores_new_candidates(self):
        # ARRANGE
        values = [0] * 81
        candidates = [0] * 81
        grid = GridState(values, candidates, tuple(values))

        idx = 17
        cell = Cell.from_index(idx)

        mask = digit_mask(6)

        # ACT
        grid.add_candidates(cell, mask)

        # ASSERT
        assert grid._candidates[idx] == mask

    def test_eliminate_candidates_removes_new_candidates(self):
        # ARRANGE
        grid = GridState.create_empty()
        grid._candidates = [ALL_DIGITS] * 81

        idx = 17
        cell = Cell.from_index(idx)

        elimination_mask = 0b000100100
        expected = 0b111011011

        # ACT
        grid.eliminate_candidates(cell, elimination_mask)

        # ASSERT
        assert grid._candidates[idx] == expected

    def test_is_complete_on_empty_grid_is_false(self):
        # ARRANGE
        grid = GridState.create_empty()

        # ACT
        complete = grid.is_complete()

        # ASSERT
        assert not complete

    def test_is_complete_on_a_parial_grid_is_false(self):
        # ARRANGE
        grid = GridState.create_empty()
        for i in range(0, 81, 4):
            grid._values[i] = (i % 9) + 1

        # ACT
        complete = grid.is_complete()

        # ASSERT
        assert not complete

    def test_is_complete_on_a_complete_grid_is_true(self):
        # ARRANGE
        grid = GridState.create_empty()
        for i in range(81):
            grid._values[i] = (i % 9) + 1

        # ACT
        complete = grid.is_complete()

        # ASSERT
        assert complete

    def test_cell_empty_on_an_empty_cell(self):
        # ARRANGE
        grid = GridState.create_empty()
        cell = Cell(5, 5)

        # ACT
        empty = grid.cell_empty(cell)

        # ASSERT
        assert empty

    def test_cell_empty_on_an_filled_cell(self):
        # ARRANGE
        grid = GridState.create_empty()
        cell = Cell(5, 5)
        grid._values[cell.index] = 5

        # ACT
        empty = grid.cell_empty(cell)

        # ASSERT
        assert not empty

    def test_copy_returns_same_values_and_candidates(self):
        # ARRANGE
        grid = GridState.create_empty()
        grid._candidates = [ALL_DIGITS] * 81

        grid.write_value(Cell(0, 0), 5)
        grid.eliminate_candidates(Cell(1, 1), 0b000001000)

        # ACT
        copy = grid.copy()

        # ASSERT
        assert copy.value(Cell(0, 0)) == 5
        assert copy.candidates(Cell(1, 1)) == 0b111110111

        assert copy._candidates == grid._candidates
        assert copy._values == grid._values

    def test_copy_has_independent_values(self):
        # ARRANGE
        grid = GridState.create_empty()
        grid.write_value(Cell(0, 0), 5)

        # ACT
        copy = grid.copy()
        copy.write_value(Cell(0, 0), 7)

        # ASSERT
        assert copy.value(Cell(0, 0)) == 7
        assert grid.value(Cell(0, 0)) == 5

    def test_copy_has_independent_candidates(self):
        # ARRANGE
        grid = GridState.create_empty()
        grid._candidates = [ALL_DIGITS] * 81
        cell = Cell(0, 0)

        # ACT
        copy = grid.copy()
        copy.eliminate_candidates(cell, 0b000001000)

        # ASSERT
        assert copy.candidates(cell) != grid.candidates(cell)
        assert grid.candidates(cell) == ALL_DIGITS

    def test_changes_to_original_do_not_affect_copy(self):
        # ARRANGE
        grid = GridState.create_empty()
        grid._candidates = [ALL_DIGITS] * 81
        copy = grid.copy()

        # ACT
        grid.write_value(Cell(0, 0), 5)
        grid.eliminate_candidates(Cell(1, 1), 1 << 4)

        # ASSERT
        assert copy.value(Cell(0, 0)) == 0
        assert copy.candidates(Cell(1, 1)) == ALL_DIGITS

    def test_reset_clears_user_entered_values(self):
        # ARRANGE
        puzzle_values = (1,) * 81
        grid = GridState.new_puzzle(puzzle_values)
        grid._values = [2] * 81

        # ACT
        grid.reset()

        # ASSERT
        assert len(grid._values) == 81
        assert all(value == 1 for value in grid._values)

    def test_reset_sets_all_candidates_to_zero(self):
        # ARRANGE
        grid = GridState.create_empty()
        grid._candidates = [ALL_DIGITS] * 81

        # ACT
        grid.reset()

        # ASSERT
        assert len(grid._candidates) == 81
        assert all(candidate == 0 for candidate in grid._candidates)
