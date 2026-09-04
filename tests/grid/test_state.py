from grid.cell import Cell
from grid.state import GridState
from grid.utils import ALL_DIGITS, digit_mask


class TestGridState:
    def test_create_empty_initialises_empty_grid_of_values(self):
        # ARRANGE
        grid = GridState.create_empty()

        # ASSERT
        assert len(grid._values) == 81
        assert all(value == 0 for value in grid._values)

    def test_create_empty_initialises_empty_grid_of_candidates(self):
        # ARRANGE
        grid = GridState.create_empty()

        # ASSERT
        assert len(grid._candidates) == 81
        assert all(candidates == ALL_DIGITS for candidates in grid._candidates)

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

    def test_add_candidates_stores_new_candidates(self):
        # ARRANGE
        values = [0] * 81
        candidates = [0] * 81
        grid = GridState(values, candidates)

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

        grid.write_value(Cell(0, 0), 5)
        grid.eliminate_candidates(Cell(1, 1), 0b000001000)

        # ACT
        copy = grid.copy()

        # ASSERT
        assert copy.value(Cell(0, 0)) == 5
        assert copy._candidates[Cell(1, 1).index] == 0b111110111

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
        cell = Cell(0, 0)

        # ACT
        copy = grid.copy()
        copy.eliminate_candidates(cell, 0b000001000)

        # ASSERT
        assert copy._candidates[cell.index] != grid._candidates[cell.index]
        assert grid._candidates[cell.index] == ALL_DIGITS

    def test_changes_to_original_do_not_affect_copy(self):
        # ARRANGE
        grid = GridState.create_empty()
        copy = grid.copy()

        # ACT
        grid.write_value(Cell(0, 0), 5)
        grid.eliminate_candidates(Cell(1, 1), 1 << 4)

        # ASSERT
        assert copy.value(Cell(0, 0)) == 0
        assert copy._candidates[Cell(1, 1).index] == ALL_DIGITS
