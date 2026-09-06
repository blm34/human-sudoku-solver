from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sudoku_strategy.grid import GridAnalysis
    from sudoku_strategy.strategy.deduction import Deduction


class AbsStrategy(ABC):
    """An interface for strategies to progress a sudoku."""

    @abstractmethod
    def find(self, analysis: GridAnalysis) -> Deduction | None:
        """Find one valid deduction if one exists, otherwise return None."""
        raise NotImplementedError
