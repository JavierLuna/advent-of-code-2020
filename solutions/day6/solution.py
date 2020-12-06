from typing import Set, List, Callable

from solutions.runner.base_solution import BaseSolution
from solutions.runner.readers.base_reader import BaseReader
import functools


class Day6Reader(BaseReader):
    def read_input_data(self, filename: str):
        # Group them dictionaries together
        groups = self._read_lines(filename, omit_empty=False)
        final_input_data = [[]]
        for group in groups:
            group = group.strip()
            if group:
                final_input_data[-1].append(set(group))
            else:
                final_input_data.append([])
        return final_input_data


class Day6Solution(BaseSolution):
    __reader__ = Day6Reader

    def solve_first(self):
        return self._get_group_resolution(self.input_data, set.union)

    def _get_group_resolution(self, input_data: List[Set[str]],
                              reduce_set_op: Callable[[Set[str], Set[str]], Set[str]]):
        return sum(len(functools.reduce(reduce_set_op, group)) for group in input_data)

    def solve_second(self):
        return self._get_group_resolution(self.input_data, set.intersection)
