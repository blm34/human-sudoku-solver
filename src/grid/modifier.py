from typing import TYPE_CHECKING

from strategy.deduction import DigitDeduction, EliminationDeduction

from .cell import CellIterators
from .utils import ALL_DIGITS, digit_mask

if TYPE_CHECKING:
    from collections.abc import Iterable

    from strategy.deduction import AbsDeduction

    from .cell import Cell
    from .state import GridState


class GridModifier:
    """Modify a given grid's state."""

    def __init__(
        self,
        state: GridState,
        cell_iterators: CellIterators | None = None,
    ):
        self._state = state
        self._cell_iterators = cell_iterators or CellIterators(state)

    def write_value(self, value: int, cell: Cell):
        """Write a value as confirmed to a cell.

        Writes the value to the cell and updates the candidates in unset cells.
        Board state is updated to remain consistent.

        Args:
            value: The value to write to the cell
            cell: The cell to write the value to
        """
        self._state.write_value(cell, value)

        self._state.eliminate_candidates(cell, ALL_DIGITS)

        for peer in self._cell_iterators.peers(cell):
            self.remove_candidate(value, peer)

    def _get_candidate_mask(self, values: Iterable[int]) -> int:
        """Takes a list of values from 1-9 and turn them into a candidate bit mask."""
        mask = 0
        for digit in values:
            mask |= digit_mask(digit)
        return mask

    def remove_candidate(self, value: int, cell: Cell):
        """Remove a candidate from a cell.

        If the given cell does not have the given candidate, no action is taken.

        Args:
            value: The value of the candidate to remove
            cell: The cell to remove the candidate from
        """
        mask = digit_mask(value)
        self._state.eliminate_candidates(cell, mask)

    def remove_candidates(self, values: Iterable[int], cell: Cell):
        """Remove candidates from a cell.

        Args:
            values: A list of candidates to remove from the cell
            cell: The cell to remove the candidates from
        """
        mask = self._get_candidate_mask(values)
        self._state.eliminate_candidates(cell, mask)

    def add_candidate(self, value: int, cell: Cell):
        """Add a cadidate to a cell.

        Args:
            value: The value of the cadidate to add
            cell: The cell to add the candidate to
        """
        mask = digit_mask(value)
        self._state.add_candidates(cell, mask)

    def add_candidates(self, values: Iterable[int], cell: Cell):
        """Add candidates to a cell.

        Args:
            values: A list of candidates to add to the cell
            cell: The cell to add the candidates to
        """
        mask = self._get_candidate_mask(values)
        self._state.add_candidates(cell, mask)

    def apply(self, deduction: AbsDeduction):
        """Apply a deduction to a grid.

        Args:
            deduction: The deduction to apply
        """
        if isinstance(deduction, DigitDeduction):
            self._apply_digit_deduction(deduction)

        elif isinstance(deduction, EliminationDeduction):
            self._apply_elimination_deduction(deduction)

    def _apply_digit_deduction(self, deduction: DigitDeduction):
        self.write_value(deduction.digit, deduction.cell)

    def _apply_elimination_deduction(self, deduction: EliminationDeduction):
        for cell, digit in deduction.eliminations:
            self.remove_candidate(digit, cell)

    def compute_candidates(self):
        """Compute all candidates based off the current values in the grid."""
        for cell in self._cell_iterators.cells():
            self._state.add_candidates(cell, ALL_DIGITS)

        for cell in self._cell_iterators.cells():
            value = self._state.value(cell)
            if value != 0:
                self.write_value(value, cell)
