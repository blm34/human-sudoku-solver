from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from grid import GridAnalysis
    from strategy.deduction import AbsDeduction


class AbsStrategy(ABC):
    """An interface for strategies to progress a sudoku."""

    @abstractmethod
    def find(self, analysis: GridAnalysis) -> AbsDeduction | None:
        """Find one valid deduction if one exists, otherwise return None."""
        raise NotImplementedError
