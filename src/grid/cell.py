from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Self
    from .state import GridState


@dataclass(frozen=True)
class Cell:
    """Represent a single cell in a sudoku grid.

    Attributes:
        row: The row of the cell (0-8)
        col: The column of the cell (0-8)

    Properties:
        index: The index of the cell in the grid (0-80)
        box: The index of the box containing the cel (0-8)
    """

    row: int
    col: int

    @classmethod
    def from_index(cls, index: int) -> Self:
        """Create a cell from it's index on the board.

        The indexes start from 0 in the top left cell and work along each row
        and then down each column up to 80 in the bottom left cell.

        Args:
            index: The index of the cell.
        """
        row, col = divmod(index, 9)
        return cls(row, col)

    @property
    def index(self) -> int:
        """Gets the index of the cell."""
        return self.row * 9 + self.col

    @property
    def box(self) -> int:
        """Gets the index of the box the cell is in (0-8)."""
        return (self.row // 3) * 3 + self.col // 3


class CellIterators:
    """Contains iterators over regions of the grid.

    Methods:
        cells
        empty_cells
        row
        col
        box
        peers
    """

    def __init__(self, grid: "GridState"):
        self._grid = grid

    def cells(self) -> tuple[Cell, ...]:
        """Iterate over all cells in the grid.

        Returns:
            A generator yielding cells
        """
        return tuple(Cell.from_index(idx) for idx in range(81))

    def empty_cells(self) -> tuple[Cell, ...]:
        """Iterate over all the empty cells in the grid.

        Returns:
            A generator yielding empty cells
        """
        return tuple(cell for cell in self.cells() if self._grid.cell_empty(cell))

    def units(self) -> tuple[tuple[Cell, ...], ...]:
        return tuple(
            unit
            for idx in range(9)
            for unit in (self.row(idx), self.col(idx), self.box(idx))
        )

    def row(self, row_num: int) -> tuple[Cell, ...]:
        """Iterate over cells in a row.

        Args:
            row_num: The row to iterate over

        Returns:
            A generator yielding cells from the given row
        """
        return tuple(Cell(row_num, col) for col in range(9))

    def col(self, col_num: int) -> tuple[Cell, ...]:
        """Iterate over cells in a column.

        Args:
            col_num: The column to iterate over

        Returns:
            A generator yielding cells from the given column
        """
        return tuple(Cell(row, col_num) for row in range(9))

    def box(self, box_num: int) -> tuple[Cell, ...]:
        """Iterate over cells in a box.

        Args:
            box_num: The index of the box to iterate over

        Returns:
            A generator yielding cells from the given box
        """
        box_row, box_col = divmod(box_num, 3)
        return tuple(
            Cell(box_row * 3 + row, box_col * 3 + col)
            for row in range(3)
            for col in range(3)
        )

    def peers(self, cell: Cell) -> tuple[Cell, ...]:
        """Iterate over all the peers of a given cell.

        Args:
            cell: The cell to find peers of

        Returns:
            A generator yielding cells that are peers of the given cell
        """
        peers = (
            set(self.row(cell.row)) | set(self.col(cell.col)) | set(self.box(cell.box))
        )
        peers.remove(cell)
        return tuple(peers)
