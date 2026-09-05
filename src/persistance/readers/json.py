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

from grid import Cell, GridModifier, GridState

from .interface import AbsSudokuReader

if TYPE_CHECKING:
    from typing import TextIO


class JsonReader(AbsSudokuReader):
    def read(self, stream: TextIO) -> GridState:
        """Read a json format from a text stream."""
        grid_dict = json.load(stream)

        # Create grid with the given puzzle values
        grid = GridState.new_puzzle(tuple(grid_dict["puzzle_values"]))
        modifier = GridModifier(grid)

        # Add the entered values to the grid
        for idx, val in enumerate(grid_dict["values"]):
            if val != 0:
                cell = Cell.from_index(idx)
                grid.write_value(cell, val)

        # Update the puzzle's candidates
        for idx, candidate_list in enumerate(grid_dict["candidate_values"]):
            if len(candidate_list) != 0:
                cell = Cell.from_index(idx)
                modifier.add_candidates(candidate_list, cell)

        return grid
