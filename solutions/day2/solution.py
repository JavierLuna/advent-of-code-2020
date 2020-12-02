from solutions.runner.base_solution import BaseSolution
from solutions.runner.readers.base_reader import BaseReader
from collections import Counter


class Day2Reader(BaseReader):
    @staticmethod
    def transform_raw_line(line: str):
        "5-6 d: dcdddt -> (5, 6, d, dcdddt)"
        bounds, char, password = line.strip().split(" ")

        # cleaning
        lower_bound, upper_bound = [int(x) for x in bounds.split("-")]
        char = char[:-1]
        return (lower_bound, upper_bound, char, password)


class Day2Solution(BaseSolution):
    __reader__ = Day2Reader

    def solve_first(self):
        n_good_passwords = 0
        for combo in self.input_data:
            l, u, c, p = combo
            if l <= Counter(p)[c] <= u:
                n_good_passwords += 1
        return n_good_passwords

    def solve_second(self):
        n_good_passwords = 0
        for combo in self.input_data:
            l, u, c, p = combo
            if sum(int(c == position) for position in [p[l-1], p[u-1]]) == 1:
                n_good_passwords += 1
        return n_good_passwords
