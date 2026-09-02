from typing import TYPE_CHECKING

from .state import GridState
from .cell import Cell, CellIterators
from .utils import digit_mask

if TYPE_CHECKING:
    from typing import Iterable


class GridAnalysis:
    """Perform an analysis of a grid."""

    def __init__(self, grid: GridState, cell_iterators: CellIterators | None = None):
        self._grid = grid
        self.iterate = cell_iterators or CellIterators(grid)

    def get_cells_with_candidate(
        self,
        cells: Iterable[Cell],
        digit: int,
    ) -> tuple[Cell, ...]:
        """Get a list of cells with a given candidate.

        Out of the cells given, return those that have the given digit as a
        candidate.

        Args:
            cells: The cells to check
            digit: The candidate to check for

        Returns:
            The filtered list of cells that have the given candidate
        """
        candidate_mask = digit_mask(digit)
        return tuple(
            cell
            for cell in cells
            if self._grid._candidates[cell.index] & candidate_mask
        )

    def count_cells_with_candidate(self, cells: Iterable[Cell], digit: int) -> int:
        """Count how many cells have a given candidate.

        Out of the given cells, how many of them have the given digit as a
        candidate.

        Args:
            cells: The cells to check
            digit: The candidate to check for

        Returns:
            The number of cells that have the given candidate
        """
        return len(self.get_cells_with_candidate(cells, digit))

    def get_candidates_for_cell(self, cell: Cell) -> tuple[int, ...]:
        """Return an iterator of all the candidates for a given cell.

        Args:
            cell: The cell to get the candidates for
        """
        candidates = self._grid._candidates[cell.index]
        return tuple(digit for digit in range(1, 10) if candidates & 1 << (digit - 1))

    def count_candidates_in_cell(self, cell: Cell) -> int:
        """Count the number of candidates in a cell.

        Args:
            cell: The cell to count candidates in
        """
        candidates = self._grid._candidates[cell.index]
        return candidates.bit_count()
