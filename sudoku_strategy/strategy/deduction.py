from abc import ABC
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sudoku_strategy.grid import Cell


@dataclass(frozen=True)
class CellDigit:
    """Represents a value or candidate that can be changed in a cell."""

    cell: Cell
    digit: int


@dataclass(frozen=True)
class Deduction(ABC):
    """Abstract class for the result of a strategy."""

    strategy: str
    explanation: str
    eliminations: list[CellDigit] = field(default_factory=list)
    assignment: CellDigit | None = None
