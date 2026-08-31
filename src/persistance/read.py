from typing import TYPE_CHECKING

from .readers import SusserReader

if TYPE_CHECKING:
    from pathlib import Path
    from grid import GridState
    from .readers.interface import AbsSudokuReader


READERS = {
    ".txt": SusserReader,
}


class SudokuFileReader:
    def load(self, path: Path) -> GridState:
        reader = self._reader_for(path)

        with path.open("r") as stream:
            return reader.read(stream)

    def _reader_for(self, path: Path) -> AbsSudokuReader:
        extension = path.suffix
        reader = READERS.get(extension)

        if reader is None:
            raise ValueError(f"No reader found for {extension} file types.")

        return reader()
