from functools import lru_cache
from typing import List, Tuple

from solutions.runner.base_solution import BaseSolution
from solutions.runner.readers.numeric import IntListReader


class Window:
    def __init__(self, input_data: List[int], window_size: int):
        self.input_data = input_data
        self.window_size = window_size
        self._w_delta = 0

    @property
    def preamble(self) -> List[int]:
        return self._get_preamble(self._w_delta, self.window_size)

    @lru_cache(maxsize=None)
    def _get_preamble(self, delta: int, window_size: int) -> List[int]:
        return sorted(self.input_data[delta: delta + window_size])

    def next(self):
        self._w_delta += 1


class Day9Solution(BaseSolution):
    __reader__ = IntListReader
    WINDOW_SIZE = 25

    def solve_first(self):
        window = Window(self.input_data, self.WINDOW_SIZE)
        for target_number in self.input_data[self.WINDOW_SIZE:]:
            valid = False
            for i, p_number in enumerate(window.preamble):
                missing_pair = target_number - p_number
                if missing_pair in window.preamble[:i] or missing_pair in window.preamble[i + 1:]:
                    valid = True
                    break
            if not valid:
                return target_number
            window.next()

    @staticmethod
    def _find_contagious_set(target: int, input_data: List[int]) -> Tuple[bool, int, int]:
        contagious_sum = 0
        contagious_highest = 0
        for i, entry in enumerate(input_data):
            contagious_sum += entry
            if entry > contagious_highest:
                contagious_highest = entry
            if contagious_sum == target and i > 0:
                return True, input_data[0], contagious_highest
            if contagious_sum > target:
                break
        return False, input_data[0], contagious_highest

    def solve_second(self):
        target = self._solutions["solve_first"]
        for i, _ in enumerate(self.input_data):
            is_contagious, lowest, highest = self._find_contagious_set(target, self.input_data[i:])
            if is_contagious:
                return lowest + highest
