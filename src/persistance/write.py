from typing import TYPE_CHECKING

from .writers import SusserWriter

if TYPE_CHECKING:
    from pathlib import Path
    from grid import GridState
    from .writers.interface import AbsSudokuWriter


WRITERS = {
    ".txt": SusserWriter,
}


class SudokuFileWriter:
    def save(self, grid: GridState, path: Path):
        writer = self._writer_for(path)

        with path.open("w") as stream:
            writer.write(grid, stream)

    def _writer_for(self, path: Path) -> AbsSudokuWriter:

        extension = path.suffix
        writer = WRITERS.get(extension)

        if writer is None:
            raise ValueError(f"No writer found for files of type {extension}")

        return writer()
