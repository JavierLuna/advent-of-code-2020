import math
from typing import Tuple, Set

from solutions.runner.base_solution import BaseSolution

from solutions.runner.readers.base_reader import BaseReader


class Day3Reader(BaseReader):
    TREE = "#"

    @staticmethod
    def transform_raw_line(line: str):
        line = line.strip()
        return {i for i, c in enumerate(line) if c == Day3Reader.TREE}, len(line)


class Day3Solution(BaseSolution):
    __reader__ = Day3Reader

    def solve_first(self):
        return self._count_trees(self.input_data, 1, 3)

    def _count_trees(self, input_data: Tuple[Set[int], int], down: int, right: int):
        tree_count = 0
        x_position = 0
        for i, (tree_positions, line_length) in enumerate(input_data):
            if i % down != 0:
                continue
            if x_position in tree_positions:
                tree_count += 1
            x_position += right
            x_position = x_position % line_length
        return tree_count

    def solve_second(self):
        combos = [
            (1, 1),
            (1, 3),
            (1, 5),
            (1, 7),
            (2, 1)
        ]
        input_data = self.input_data
        return math.prod([self._count_trees(input_data, *combo) for combo in combos])
