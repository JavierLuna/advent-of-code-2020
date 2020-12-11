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
            input_data = [self.transform_raw_line(line.strip()) for line in file if not (omit_empty and not line.strip())]

        if use_cache:
            self._content_cache[filename] = input_data
        return input_data

    @staticmethod
    def transform_raw_line(line: str):
        return line

    def read_input_data(self, filename: str) -> Any:
        return self._read_lines(filename)


class BaseGroupReader(BaseReader):
    __group_metadata__ = list, list.append

    def read_input_data(self, filename: str):
        structure, add_op = self.__group_metadata__
        # Group them dictionaries together
        transformed_lines = self._read_lines(filename, omit_empty=False)
        final_input_data = [structure()]
        for transformed_line in transformed_lines:
            if transformed_line:
                add_op(final_input_data[-1], transformed_line)
            else:
                final_input_data.append(structure())
        return final_input_data
