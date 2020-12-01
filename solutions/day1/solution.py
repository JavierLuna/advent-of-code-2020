from typing import Set, Tuple
import math
from solutions.runner.base_solution import BaseSolution
from solutions.runner.readers.numeric import IntSetReader


class Day1Solution(BaseSolution):
    __reader__ = IntSetReader
    TARGET = 2020

    def solve_first(self):
        return math.prod(self.find_sum_pair(self.input_data, self.TARGET))

    @staticmethod
    def find_sum_pair(numbers: Set[int], target: int) -> Tuple[int, int]:
        result = (-1, -1)
        for number in numbers:
            required_number = target - number
            if required_number in numbers:
                print(f"Numbers can be {number} and {required_number} which ammount to: {number * required_number}")
                result = (number, required_number)
                if required_number != number:
                    break
        return result

    def solve_second(self):
        return math.prod(self.find_sum_trice(self.input_data, self.TARGET))

    @classmethod
    def find_sum_trice(cls, numbers: Set[int], target: int) -> Tuple[int, int, int]:
        for number in numbers:
            required_number = target - number
            result = (number, *cls.find_sum_pair(numbers, required_number))
            if sum(result) == target:
                return result
