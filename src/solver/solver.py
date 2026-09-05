from logging import getLogger
from typing import TYPE_CHECKING

from grid import GridAnalysis, GridModifier
from strategy import HiddenSingleStrategy, NakedSingleStrategy

if TYPE_CHECKING:
    from collections.abc import Sequence

    from grid.state import GridState
    from strategy.abs_strategy import AbsStrategy
    from strategy.deduction import AbsDeduction


_logger = getLogger(__name__)


STRATEGIES = (
    NakedSingleStrategy(),
    HiddenSingleStrategy(),
)


class Solver:
    def __init__(self, strategies: Sequence[AbsStrategy] = STRATEGIES):
        self._strategies = strategies

    def find_next(self, grid: GridState) -> AbsDeduction | None:
        """Find the next move for the given grid.

        Args:
            grid: The grid to find the next move for

        Returns:
            The next move, or None if none are found
        """
        analysis = GridAnalysis(grid)

        for strategy in self._strategies:
            deduction = strategy.find(analysis)

            if deduction is not None:
                return deduction

        return None

    def solve(self, grid: GridState) -> list[AbsDeduction]:
        """Find all the moves to solve the sudoku.

        Args:
            grid: The state of the puzzle to be solved

        Returns:
            A list of moves to solve the puzzle
        """
        working_grid = grid.copy()
        modifier = GridModifier(working_grid)
        deductions = []

        while not working_grid.is_complete():
            deduction = self.find_next(working_grid)

            if deduction is None:
                _logger.warning("No next step found for puzzle.")
                break

            deductions.append(deduction)

            modifier.apply(deduction)

        return deductions
