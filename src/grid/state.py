from .cell import Cell, CellIterators
from .utils import ALL_DIGITS, digit_mask


class GridState:
    """Store grid state and provide information about candidates.

    Methods:
        write_value
        remove_candidate
    """

    def __init__(self, cell_iterators: CellIterators | None = None):
        # The confirmed value for each cell in the grid (0 means not yet known)
        self.values = [0] * 81
        # A bit mask for the candidates for each cell in the grid
        self.candidates = [ALL_DIGITS] * 81

        self._cell_iterators = cell_iterators or CellIterators(self)

    def write_value(self, value: int, cell: Cell):
        """Write a value as confirmed to a cell.

        Writes the value to the cell and updates the candidates in unset cells.
        Board state is updated to remain consistent.

        Args:
            value: The value to write to the cell
            cell: The cell to write the value to
        """
        self.values[cell.index] = value

        self.candidates[cell.index] = 0

        for peer in self._cell_iterators.peers(cell):
            self.remove_candidate(value, peer)

    def remove_candidate(self, value: int, cell: Cell):
        """Remove a candidate from a cell.

        If the given cell does not have the given candidate, no action is taken.

        Args:
            value: The value of the candidate to remove
            cell: The cell to remove the candidate from
        """
        mask = ~digit_mask(value)
        self.candidates[cell.index] &= mask
