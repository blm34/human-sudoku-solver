from typing import TYPE_CHECKING

from .abs_strategy import AbsStrategy
from .deduction import EliminationDeduction

if TYPE_CHECKING:
    from sudoku_strategy import Cell
    from sudoku_strategy.grid import GridAnalysis


class EliminateCandidatesStrategy(AbsStrategy):
    """Detect candidates that can be trivially eliminated."""

    def find(self, analysis: GridAnalysis) -> EliminationDeduction | None:
        """Check the grid for candidates to eliminate."""
        eliminations = self._get_eliminatable_candidates(analysis)

        if len(eliminations) == 0:
            return None

        return EliminationDeduction(
            strategy="Candidate Elimination",
            explanation="The given candidates are already accounted for in a given unit",
            eliminations=eliminations,
        )

    def _get_eliminatable_candidates(
        self,
        analysis: GridAnalysis,
    ) -> list[tuple[Cell, int]]:
        """Find all candidates that can be trivially eliminated."""
        cells = []

        for cell in analysis.iterate.filled_cells():
            value = analysis.get_value_in_cell(cell)
            peers = analysis.iterate.peers(cell)
            eliminatable = analysis.get_cells_with_candidate(peers, value)
            cells += [(cell, value) for cell in eliminatable]

        return cells
