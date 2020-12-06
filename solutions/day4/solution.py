from typing import Callable, Dict
import re

from solutions.runner.base_solution import BaseSolution
from solutions.runner.readers.base_reader import BaseReader
from solutions.runner.readers.groups import DictionaryGroupReader


class PassportReader(DictionaryGroupReader):

    @staticmethod
    def transform_raw_line(line: str):
        line = line.strip()
        if line:
            pairs = line.split(" ")
            return dict([pair.split(":") for pair in pairs])


class Day4Solution(BaseSolution):
    __reader__ = PassportReader

    def solve_first(self):
        n_valid_passports = 0
        required_fields = [
            "byr",
            "iyr",
            "eyr",
            "hgt",
            "hcl",
            "ecl",
            "pid"
        ]
        for passport_data in self.input_data:
            if all(required_field in passport_data for required_field in required_fields):
                n_valid_passports += 1
        return n_valid_passports

    def solve_second(self):
        n_valid_passports = 0

        _between = lambda a, b: lambda x: a <= int(x) <= b

        def _validate_height(x: str) -> bool:
            if len(x) < 3:
                return False
            value, unit = int(x[:-2]), x[-2:]
            if unit == "cm":
                return _between(150, 193)(value)
            if unit == "in":
                return _between(59, 76)(value)
            return False

        required_fields: Dict[str, Callable[[str], bool]] = {
            "byr": _between(1920, 2002),
            "iyr": _between(2010, 2020),
            "eyr": _between(2020, 2030),
            "hgt": _validate_height,
            "hcl": lambda x: re.match(r"#[0-9a-x]{6}", x),
            "ecl": lambda x: x in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"],
            "pid": lambda x: len(x) == 9 and re.match(r"0*[1-9]+", x)
        }
        for passport_data in self.input_data:
            if all(required_field in passport_data and val_function(passport_data[required_field]) for
                   required_field, val_function in required_fields.items()):
                n_valid_passports += 1
        return n_valid_passports
