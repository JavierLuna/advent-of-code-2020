from abc import ABCMeta
from typing import Any, List


class BaseReader(metaclass=ABCMeta):

    def __init__(self):
        self._content_cache = {}

    def _read_lines(self,
                    filename: str,
                    omit_empty: bool = True,
                    use_cache: bool = True) -> List[Any]:

        if filename in self._content_cache and use_cache:
            return self._content_cache[filename]

        with open(filename) as file:
            input_data = [self.transform_raw_line(line) for line in file if not (omit_empty and not line.strip())]

        if use_cache:
            self._content_cache[filename] = input_data
        return input_data

    @staticmethod
    def transform_raw_line(line: str):
        return line

    def read_input_data(self, filename: str) -> Any:
        return self._read_lines(filename)
