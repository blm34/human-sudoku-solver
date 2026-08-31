from typing import TYPE_CHECKING

from strategy.abs_strategy import AbsStrategy
from strategy.deduction import DigitDeduction

if TYPE_CHECKING:
    from grid import Cell, GridAnalysis
    from typing import Callable, Iterable

    UnitGetter = Callable[[int], Iterable[Cell]]


class HiddenSingleStrategy(AbsStrategy):
    """Detect hidden singles in a sudoku grid."""

    def find(self, analysis: GridAnalysis) -> DigitDeduction | None:
        """Check the grid for hidden singles."""
        result = self._find_hidden_single(analysis)

        if result is None:
            return None

        cell, value = result

        return DigitDeduction(
            strategy="Hidden Single",
            cell=cell,
            digit=value,
            explanation=f"{value} is a hidden single in cell R{cell.row + 1}C{cell.col + 1}",
        )

    def _find_hidden_single(self, analysis: GridAnalysis) -> tuple[Cell, int] | None:
        """Find a cell containing a hidden single.

        If none are found returns (None, None)

        Returns:
            The cell containing a hidden single and it's value
        """
        for cells in analysis.iterate.units():
            for digit in range(1, 10):
                candidate_cells = analysis.get_cells_with_candidate(cells, digit)
                if len(candidate_cells) == 1:
                    return candidate_cells[0], digit
        return None
