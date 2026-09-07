from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Self

    from .cell import Cell


class GridState:
    """Store grid state and provide information about candidates."""

    def __init__(
        self,
        digits: list[int],
        candidates: list[int],
        puzzle_digits: tuple[int, ...],
    ):
        self._digits = digits
        self._candidates = candidates
        self._puzzle_digits = puzzle_digits

    @classmethod
    def create_empty(cls) -> Self:
        return cls(
            digits=[0] * 81,
            candidates=[0] * 81,
            puzzle_digits=tuple([0] * 81),
        )

    @classmethod
    def new_puzzle(cls, puzzle_digits: tuple[int, ...]) -> Self:
        if len(puzzle_digits) != 81:
            raise ValueError("Sudoku puzzle must have 81 cells.")

        return cls(
            digits=list(puzzle_digits),
            candidates=[0] * 81,
            puzzle_digits=puzzle_digits,
        )

    def digit(self, cell: Cell) -> int:
        return self._digits[cell.index]

    def write_digit(self, cell: Cell, digit: int):
        if not 1 <= digit <= 9:
            raise ValueError(
                f"Sudoku cell digit must be from 1-9, {digit} is not valid."
            )
        self._digits[cell.index] = digit

    def puzzle_digit(self, cell: Cell) -> int:
        return self._puzzle_digits[cell.index]

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
        return all(digit != 0 for digit in self._digits)

    def cell_empty(self, cell: Cell) -> bool:
        """Returns true if the given cell has no digit set."""
        return self._digits[cell.index] == 0

    def copy(self) -> GridState:
        """Returns a deep copy of the current grid state."""
        return GridState(
            digits=self._digits.copy(),
            candidates=self._candidates.copy(),
            puzzle_digits=self._puzzle_digits,
        )

    def reset(self):
        """Clear all user entered digits and candidates."""
        self._digits = list(self._puzzle_digits)
        self._candidates = [0] * 81
