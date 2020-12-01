from typing import Set

from solutions.runner.readers.base_reader import BaseReader


class IntListReader(BaseReader):
    @staticmethod
    def transform_raw_line(line: str) -> int:
        return int(line)


class IntSetReader(IntListReader):
    def read_input_data(self, filename: str) -> Set[int]:
        return set(super().read_input_data(filename))
