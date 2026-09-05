"""
A json object containing three fields:
    * puzzle_values: A list of 81 numbers representing the puzzles initial
        starting numbers. 0 is used to represent an empty cell.
    * values: A list of 81 numbers representing the values filled in the grid.
        This includes the values set in puzzle_values uses 0 to represent an
        empty cell.
    * candidate_values: A list of 81 lists. Each sub list can contain the
        numbers 1-9 representing the candidates for the relevant cell.

Example of the json format:

{
  "puzzle_values": [0, 0, 3, 0, ...],
  "values": [1, 0, 3, 0, ...],
  "candidate_values": [
    [],
    [7, 8, 9],
    [],
    ...
  ]
}
"""

import json
from typing import TYPE_CHECKING

from grid import GridAnalysis

from .interface import AbsSudokuWriter

if TYPE_CHECKING:
    from typing import TextIO

    from grid import GridState


class JsonWriter(AbsSudokuWriter):
    def write(self, grid: GridState, stream: TextIO):
        """Read a json format from a text stream."""
        analysis = GridAnalysis(grid)

        grid_dict = {
            "puzzle_values": [],
            "values": [],
            "candidate_values": [],
        }

        for cell in analysis.iterate.cells():
            grid_dict["puzzle_values"].append(grid.puzzle_value(cell))

            grid_dict["values"].append(grid.value(cell))

            candidates = analysis.get_candidates_for_cell(cell)
            grid_dict["candidate_values"].append(list(candidates))

        json.dump(grid_dict, stream)
