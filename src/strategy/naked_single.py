from typing import TYPE_CHECKING


from .abs_strategy import AbsStrategy
from .deduction import DigitDeduction


if TYPE_CHECKING:
    from grid import Cell, GridAnalysis


class NakedSingleStrategy(AbsStrategy):
    """Detect naked singles in a sudoku grid."""

    def find(self, analysis: GridAnalysis) -> DigitDeduction | None:
        """Check the grid for naked singles."""
        cell = self._find_naked_single_cell(analysis)

        if cell is None:
            return None

        value = self._get_value_of_naked_single(analysis, cell)

        return DigitDeduction(
            strategy="Naked Single",
            cell=cell,
            digit=value,
            explanation=f"Cell R{cell.row + 1}C{cell.col + 1} is a naked single with value {value}.",
        )

    def _find_naked_single_cell(self, analysis: GridAnalysis) -> Cell | None:
        """Locate the cell that has a naked single.

        If none are found, returns None.

        Returns:
            A cell that contains a naked single
        """
        for cell in analysis.iterate.empty_cells():
            if analysis.count_candidates_in_cell(cell) == 1:
                return cell
        return None

    def _get_value_of_naked_single(self, analysis: GridAnalysis, cell: Cell) -> int:
        """Get the value of a naked single.

        The given ``cell`` must be a naked single - return it's one candidate

        Args:
            cell: The cell that contains a naked single

        Returns:
            The value of the naked single
        """
        return analysis.get_candidates_for_cell(cell)[0]
