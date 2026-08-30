from abc import ABC
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from grid import Cell


@dataclass
class AbsDeduction(ABC):
    """Abstract class for the result of a strategy."""

    strategy: str
    explanation: str


@dataclass
class EliminationDeduction(AbsDeduction):
    """Result of a strategy that allows candidates to be eliminated."""

    eliminations: list[tuple[Cell, int]]


@dataclass
class DigitDeduction(AbsDeduction):
    """Result of a strategy that allows a cell to be filled in."""

    cell: Cell
    digit: int
