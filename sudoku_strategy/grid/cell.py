from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterator
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
        """The index of the cell (0-80).

        Index 0 is the top left cell, indexes increase along each row and then
        down each column to 80 in the bottom right cell.
        """
        return self.row * 9 + self.col

    @property
    def box(self) -> int:
        """The index of the box the cell is in (0-8).

        Box 0 is top left, with 1 to its left etc. down to box 8 in the bottom
        right.
        """
        return (self.row // 3) * 3 + self.col // 3

    def __str__(self) -> str:
        return f"R{self.row + 1}C{self.col + 1}"


class Cells:
    """Represent a collection of cells.

    Cells are represented by a bit mask. Bits are set in positions corresponding
    to the indexes of cells that are included.
    """

    _MASK = (1 << 81) - 1

    def __init__(self, mask):
        self._mask = mask

    def _mask_for_cell(self, cell: Cell) -> int:
        """Get the mask for the given cell."""
        return 1 << cell.index

    def remove(self, cell: Cell):
        """Remove the given cell."""
        mask = self._mask_for_cell(cell)
        self._mask &= ~mask

    def add(self, cell: Cell):
        """Add the given cell"""
        mask = self._mask_for_cell(cell)
        self._mask |= mask

    def __and__(self, other: Cells) -> Cells:
        """Performs an intersection on two sets of cells."""
        mask = self._mask & other._mask
        return Cells(mask)

    def __or__(self, other: Cells) -> Cells:
        """Performs a union on two sets of cells."""
        mask = self._mask | other._mask
        return Cells(mask)

    def __invert__(self) -> Cells:
        """Returns the complementary set of cells."""
        mask = ~self._mask & self._MASK
        return Cells(mask)

    def __len__(self) -> int:
        """Counts how many cells are in the set."""
        return self._mask.bit_count()

    def __contains__(self, cell: Cell) -> bool:
        """Is the given cell in the set."""
        cell_mask = self._mask_for_cell(cell)
        return bool(cell_mask & self._mask)

    def __iter__(self) -> Iterator[Cell]:
        """Iterate over the cells."""
        mask = self._mask

        while mask:
            bit = mask & -mask
            index = bit.bit_length() - 1
            yield Cell.from_index(index)
            mask ^= bit


class CellIterators:
    """Contains iterators over regions of the grid.

    Methods:
        cells
        empty_cells
        filled_cells
        units
        lines
        row
        col
        box
        peers
    """

    _ALL_CELLS = (1 << 81) - 1
    _ROW_MASKS = tuple(((1 << 9) - 1) << row * 9 for row in range(9))
    _COL_MASKS = tuple(
        sum(1 << (col + 9 * row) for row in range(9)) for col in range(9)
    )
    _BOX_MASKS = tuple(
        sum(
            1 << (row * 9 + col)
            for row in range(box_row * 3, box_row * 3 + 3)
            for col in range(box_col * 3, box_col * 3 + 3)
        )
        for box_row in range(3)
        for box_col in range(3)
    )

    def __init__(self, grid: GridState):
        self._grid = grid

    def cells(self) -> Cells:
        """Get all cells in the grid.

        Returns:
            A tuple of all cells in the grid
        """
        return Cells(self._ALL_CELLS)

    def empty_cells(self) -> Cells:
        """Get all the empty cells in the grid.

        Returns:
            A tuple of empty cells
        """
        mask = sum(
            1 << cell.index for cell in self.cells() if self._grid.cell_empty(cell)
        )
        return Cells(mask)

    def filled_cells(self) -> Cells:
        """Get all non-empty cells in the grid.

        Returns:
            A tuple of filled cells
        """
        mask = sum(
            1 << cell.index for cell in self.cells() if not self._grid.cell_empty(cell)
        )
        return Cells(mask)

    def units(self) -> tuple[Cells, ...]:
        """Get a tuple of all rows, cols, and boxes."""
        return tuple(
            unit
            for idx in range(9)
            for unit in (self.row(idx), self.col(idx), self.box(idx))
        )

    def lines(self) -> tuple[Cells, ...]:
        """Get a tuple of all rows and columns."""
        return tuple(
            unit for idx in range(9) for unit in (self.row(idx), self.col(idx))
        )

    def row(self, row_num: int) -> Cells:
        """Get the cells for the given row.

        Args:
            row_num: The row to iterate over

        Returns:
            A tuple of cells from the given row
        """
        mask = self._ROW_MASKS[row_num]
        return Cells(mask)

    def col(self, col_num: int) -> Cells:
        """Get the cells for the given column.

        Args:
            col_num: The column to iterate over

        Returns:
            A tuple of cells from the given column
        """
        mask = self._COL_MASKS[col_num]
        return Cells(mask)

    def box(self, box_num: int) -> Cells:
        """Get the cells for the given box.

        Args:
            box_num: The index of the box to iterate over

        Returns:
            A tuple of cells from the given box
        """
        mask = self._BOX_MASKS[box_num]
        return Cells(mask)

    def peers(self, cell: Cell) -> Cells:
        """Iterate over all the peers of a given cell.

        Args:
            cell: The cell to find peers of

        Returns:
            A tuple of cells that are peers of the given cell
        """
        peers = self.row(cell.row) | self.col(cell.col) | self.box(cell.box)
        peers.remove(cell)
        return peers
