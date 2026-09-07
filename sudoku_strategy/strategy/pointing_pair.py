from dataclasses import dataclass
from typing import TYPE_CHECKING

from .abs_strategy import AbsStrategy
from .deduction import CellDigit, Deduction

if TYPE_CHECKING:
    from collections.abc import Generator

    from sudoku_strategy import Cell
    from sudoku_strategy.grid import GridAnalysis


@dataclass(frozen=True)
class PointingPair:
    digit: int
    box: int
    cells: tuple[Cell, ...]


class PointingPairStrategy(AbsStrategy):
    """Detect pointing pairs that can eliminate candidates."""

    def find(self, analysis: GridAnalysis) -> Deduction | None:
        """Check the grid for pointing pairs giving eliminations."""
        for pointing_pair in self._find_pointing_pairs(analysis):
            eliminations = self._get_eliminations(analysis, pointing_pair)

            if len(eliminations) == 0:
                continue

            elimination_cells = (
                f"R{elim.cell.row + 1}C{elim.cell.col + 1}" for elim in eliminations
            )
            elimination_cells = ", ".join(elimination_cells)

            return Deduction(
                strategy="Pointing Pair",
                explanation=f"Candidates for {pointing_pair.digit} in box {pointing_pair.box} allow for eliminations in {elimination_cells}.",
                eliminations=eliminations,
            )

        return None

    def _find_pointing_pairs(self, analysis: GridAnalysis) -> Generator[PointingPair]:
        """Find pointing pairs that may or may not result in an elimination"""
        for box_id in range(9):
            box_cells = analysis.iterate.box(box_id)

            for digit in range(1, 10):
                cells = analysis.get_cells_with_candidate(box_cells, digit)

                if len(cells) == 0 or len(cells) > 3:
                    continue

                # Check rows
                row = cells[0].row
                if all(cell.row == row for cell in cells):
                    yield PointingPair(
                        digit=digit,
                        box=box_id,
                        cells=analysis.iterate.row(row),
                    )

                # Check columns
                col = cells[0].col
                if all(cell.col == col for cell in cells):
                    yield PointingPair(
                        digit=digit,
                        box=box_id,
                        cells=analysis.iterate.col(col),
                    )

    def _get_eliminations(
        self,
        analysis: GridAnalysis,
        pointing_pair: PointingPair,
    ) -> list[CellDigit]:
        """Get eliminations inferred by a pointing pair."""
        eliminations = []
        for cell in pointing_pair.cells:
            if cell.box == pointing_pair.box:
                continue

            if analysis.cell_has_candidate(cell, pointing_pair.digit):
                eliminations.append(CellDigit(cell=cell, digit=pointing_pair.digit))

        return eliminations
