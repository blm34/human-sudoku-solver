from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Self

    from .cell import Cell


class GridState:
    """Store grid state and provide information about candidates."""

    def __init__(
        self,
        values: list[int],
        candidates: list[int],
        puzzle_values: tuple[int, ...],
    ):
        self._values = values
        self._candidates = candidates
        self._puzzle_values = puzzle_values

    @classmethod
    def create_empty(cls) -> Self:
        return cls(
            values=[0] * 81,
            candidates=[0] * 81,
            puzzle_values=tuple([0] * 81),
        )

    @classmethod
    def new_puzzle(cls, puzzle_values: tuple[int, ...]) -> Self:
        if len(puzzle_values) != 81:
            raise ValueError("Sudoku puzzle must have 81 cells.")

        return cls(
            values=list(puzzle_values),
            candidates=[0] * 81,
            puzzle_values=puzzle_values,
        )

    def value(self, cell: Cell) -> int:
        return self._values[cell.index]

    def write_value(self, cell: Cell, value: int):
        if not 1 <= value <= 9:
            raise ValueError(
                f"Sudoku cell value must be from 1-9, {value} is not valid."
            )
        self._values[cell.index] = value

    def puzzle_value(self, cell: Cell) -> int:
        return self._puzzle_values[cell.index]

    def candidates(self, cell: Cell) -> int:
        """Get the candidates for the given cell.

        Candidates are returned as a bit mask with the most significant bit
        representing 9 and the least significant bit representing 1. 1 is used
        for bits that represent candidates, 0 for bits representing numbers
        that are not candidates."""
        return self._candidates[cell.index]

    def add_candidates(self, cell: Cell, mask: int):
        """Add candidates to a cell.

        Args:
            cell: The cell to add the candidates to
            mask: The maks that has ones set for the bits corresponding to the candidates to add
        """
        self._candidates[cell.index] |= mask

    def eliminate_candidates(self, cell: Cell, mask: int):
        """Eliminate candidates from a cell.

        Args:
            cell: The cell to remove the candidates from
            mask: The maks that has ones set for the bits corresponding to the candidates to remove
        """
        self._candidates[cell.index] &= ~mask

    def is_complete(self) -> bool:
        """Has the grid been fully filled in."""
        return all(value != 0 for value in self._values)

    def cell_empty(self, cell: Cell) -> bool:
        """Returns true if the given cell has no value set."""
        return self._values[cell.index] == 0

    def copy(self) -> GridState:
        """Returns a deep copy of the current grid state."""
        return GridState(
            values=self._values.copy(),
            candidates=self._candidates.copy(),
            puzzle_values=self._puzzle_values,
        )

    def reset(self):
        """Clear all user entered values and candidates."""
        self._values = list(self._puzzle_values)
        self._candidates = [0] * 81
