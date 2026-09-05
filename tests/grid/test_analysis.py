from unittest.mock import Mock

import pytest

from grid.analysis import GridAnalysis
from grid.cell import Cell, CellIterators
from grid.state import GridState
from grid.utils import ALL_DIGITS


class TestGridAnalysis:
    def test_uses_supplied_cell_relations(self):
        # ARRANGE
        relations = Mock()
        state = GridState.create_empty()

        # ACT
        grid = GridAnalysis(state, relations)

        # ASSERT
        assert grid.iterate is relations

    def test_creates_cell_relations_when_none_supplied(self):
        # ARRANGE
        state = GridState.create_empty()

        # ACT
        grid = GridAnalysis(state)

        # ASSERT
        assert isinstance(grid.iterate, CellIterators)

    @pytest.mark.parametrize("cell_idx", range(81))
    def test_get_candidates_for_empty_grid_returns_no_digits(self, cell_idx):
        # ARRANGE
        state = GridState.create_empty()
        analysis = GridAnalysis(state)
        cell = Cell.from_index(cell_idx)

        # ACT
        candidates = list(analysis.get_candidates_for_cell(cell))

        # ASSERT
        assert candidates == []

    @pytest.mark.parametrize("cell_idx", range(81))
    def test_get_candidates_for_cell_with_all_candidates_returns_all(self, cell_idx):
        # ARRANGE
        state = GridState.create_empty()
        analysis = GridAnalysis(state)
        cell = Cell.from_index(cell_idx)
        state.add_candidates(cell, 0b111111111)

        # ACT
        candidates = list(analysis.get_candidates_for_cell(cell))

        # ASSERT
        assert candidates == list(range(1, 10))

    @pytest.mark.parametrize("cell_idx", range(81))
    def test_count_candidates_for_empty_cell_returns_zero(self, cell_idx):
        # ARRANGE
        state = GridState.create_empty()
        analysis = GridAnalysis(state)
        cell = Cell.from_index(cell_idx)

        # ACT
        count = analysis.count_candidates_in_cell(cell)

        # ASSERT
        assert count == 0

    @pytest.mark.parametrize("cell_idx", range(81))
    def test_count_candidates_for_cell_with_all_candidates_returns_nine(self, cell_idx):
        # ARRANGE
        state = GridState.create_empty()
        analysis = GridAnalysis(state)
        cell = Cell.from_index(cell_idx)
        state.add_candidates(cell, 0b111111111)

        # ACT
        count = analysis.count_candidates_in_cell(cell)

        # ASSERT
        assert count == 9

    def test_get_cells_with_candidate_returns_all_cells_with_that_candidate(self):
        # ARRANGE
        state = GridState.create_empty()
        state._candidates = [ALL_DIGITS] * 81
        analysis = GridAnalysis(state)
        cells = [Cell(0, col) for col in range(9)]

        # ACT
        result = list(analysis.get_cells_with_candidate(cells, 7))

        # ASSERT
        assert result == cells

    def test_count_cells_with_candidate_returns_nine_initially(self):
        # ARRANGE
        state = GridState.create_empty()
        state._candidates = [ALL_DIGITS] * 81
        analysis = GridAnalysis(state)
        cells = (Cell(0, col) for col in range(9))

        # ACT
        count = analysis.count_cells_with_candidate(cells, 7)

        # ASSERT
        assert count == 9

    def test_get_cells_with_candidate_filters_cells(self):
        # ARRANGE
        state = GridState.create_empty()
        target = Cell(0, 0)
        state._candidates = [ALL_DIGITS] * 81
        state._candidates[target.index] = 0b111101111
        analysis = GridAnalysis(state)
        cells = (Cell(0, col) for col in range(9))

        # ACT
        candidates = analysis.get_cells_with_candidate(cells, 5)

        # ASSERT
        assert target not in candidates
        assert len(candidates) == 8

    def test_count_cells_with_candidate_filters_cells(self):
        # ARRANGE
        state = GridState.create_empty()
        target = Cell(0, 0)
        written_value = 5
        state._candidates = [ALL_DIGITS] * 81
        state._candidates[target.index] = 0b111101111
        analysis = GridAnalysis(state)
        cells = (Cell(0, col) for col in range(9))

        # ACT
        count = analysis.count_cells_with_candidate(cells, written_value)

        # ASSERT
        assert count == 8

    def test_get_candidates_for_cell_returns_only_remaining_candidates(self):
        # ARRANGE
        state = GridState.create_empty()
        cell = Cell(0, 3)
        state._candidates[cell.index] = 0b011101101

        analysis = GridAnalysis(state)

        # ACT
        candidates = list(analysis.get_candidates_for_cell(cell))

        # ASSERT
        assert candidates == [1, 3, 4, 6, 7, 8]

    def test_count_candidates_for_cell_returns_remaining_count(self):
        # ARRANGE
        state = GridState.create_empty()
        cell = Cell(0, 3)
        state._candidates[cell.index] = 0b011101101

        analysis = GridAnalysis(state)

        # ACT
        count = analysis.count_candidates_in_cell(cell)

        # ASSERT
        assert count == 6
