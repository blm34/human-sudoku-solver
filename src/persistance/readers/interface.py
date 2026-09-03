from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import TextIO

    from grid import GridState


class AbsSudokuReader(ABC):
    @abstractmethod
    def read(self, stream: TextIO) -> GridState:
        """Read a sukoku from a text stream."""
        raise NotImplementedError
