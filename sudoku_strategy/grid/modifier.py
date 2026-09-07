from typing import TYPE_CHECKING

from .cell import CellIterators
from .utils import ALL_DIGITS, digit_mask

if TYPE_CHECKING:
    from collections.abc import Iterable

    from sudoku_strategy.strategy.deduction import Deduction

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

    def add_digit(self, digit: int, cell: Cell):
        """Write a digit to a cell and update relevant candidates.

        Writes the digit to the cell and updates the candidates in unset cells.
        Board state is updated to remain consistent.

        Args:
            digit: The digit to write to the cell
            cell: The cell to write the digit to
        """
        self.write_digit(digit, cell)
        self.update_candidates(digit, cell)

    def write_digit(self, digit: int, cell: Cell):
        """Write a digit to a cell.

        Args:
            digit: The digit to write to the cell
            cell: The cell to write the digit to
        """
        self._state.write_digit(cell, digit)

    def update_candidates(self, digit: int, cell: Cell):
        """Update candidates based on a digit in a cell.

        Args:
            digit: The digit in the cell causing eliminations
            cell: The cell whose peers are to be updated
        """
        self._state.eliminate_candidates(cell, ALL_DIGITS)

        for peer in self._cell_iterators.peers(cell):
            self.remove_candidate(digit, peer)

    def _get_candidate_mask(self, digits: Iterable[int]) -> int:
        """Takes a list of digits from 1-9 and turn them into a candidate bit mask."""
        mask = 0
        for digit in digits:
            mask |= digit_mask(digit)
        return mask

    def remove_candidate(self, digit: int, cell: Cell):
        """Remove a candidate from a cell.

        If the given cell does not have the given candidate, no action is taken.

        Args:
            digits: The digits of the candidate to remove
            cell: The cell to remove the candidate from
        """
        mask = digit_mask(digit)
        self._state.eliminate_candidates(cell, mask)

    def remove_candidates(self, digits: Iterable[int], cell: Cell):
        """Remove candidates from a cell.

        Args:
            digits: A list of candidates to remove from the cell
            cell: The cell to remove the candidates from
        """
        mask = self._get_candidate_mask(digits)
        self._state.eliminate_candidates(cell, mask)

    def add_candidate(self, digit: int, cell: Cell):
        """Add a cadidate to a cell.

        Args:
            digit: The digit of the cadidate to add
            cell: The cell to add the candidate to
        """
        mask = digit_mask(digit)
        self._state.add_candidates(cell, mask)

    def add_candidates(self, digits: Iterable[int], cell: Cell):
        """Add candidates to a cell.

        Args:
            digits: A list of candidates to add to the cell
            cell: The cell to add the candidates to
        """
        mask = self._get_candidate_mask(digits)
        self._state.add_candidates(cell, mask)

    def apply(self, deduction: Deduction):
        """Apply a deduction to a grid.

        Args:
            deduction: The deduction to apply
        """
        if deduction.assignment is not None:
            self.add_digit(deduction.assignment.digit, deduction.assignment.cell)

        for elimination in deduction.eliminations:
            self.remove_candidate(elimination.digit, elimination.cell)

    def compute_candidates(self):
        """Compute all candidates based off the current digits in the grid."""
        for cell in self._cell_iterators.cells():
            self._state.add_candidates(cell, ALL_DIGITS)

        for cell in self._cell_iterators.filled_cells():
            digit = self._state.digit(cell)
            self.update_candidates(digit, cell)
