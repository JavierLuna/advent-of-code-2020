import functools
from typing import Set, List, Callable

from solutions.runner.base_solution import BaseSolution

from solutions.runner.readers.groups import ListGroupReader


class Day6Reader(ListGroupReader):  # 6583, 3290
    @staticmethod
    def transform_raw_line(line: str):
        return set(line.strip())


class Day6Solution(BaseSolution):
    __reader__ = Day6Reader

    def solve_first(self):
        return self._get_group_resolution(self.input_data, set.union)

    def _get_group_resolution(self, input_data: List[Set[str]],
                              reduce_set_op: Callable[[Set[str], Set[str]], Set[str]]):
        return sum(len(functools.reduce(reduce_set_op, group)) for group in input_data)

    def solve_second(self):
        return self._get_group_resolution(self.input_data, set.intersection)
