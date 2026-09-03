from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import TextIO

    from grid import GridState


class AbsSudokuWriter(ABC):
    @abstractmethod
    def write(self, grid: GridState, stream: TextIO):
        """Write a sudoku to a text stream."""
        raise NotImplementedError
