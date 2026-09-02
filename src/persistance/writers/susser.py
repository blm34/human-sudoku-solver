"""
If there are 81 groups of digits, the data is interpreted as a candidate grid.
All formatting is ignored.

If there are N digits and 81-N occurrences of another character, this character
will be interpreted as representing an empty cell. When multiple characters add
up to 81, the following preference list is used: '0', '.', 'X', '*', '_', ' '
"""

from typing import TYPE_CHECKING


from .interface import AbsSudokuWriter

if TYPE_CHECKING:
    from typing import TextIO
    from grid import GridState


class SusserWriter(AbsSudokuWriter):
    def write(self, grid: GridState, stream: TextIO):
        """Write a susser format from a text stream"""
        for value in grid._values:
            if value == 0:
                stream.write(".")
            else:
                stream.write(str(value))
