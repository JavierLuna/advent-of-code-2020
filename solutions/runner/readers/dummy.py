from typing import Any

from solutions.runner.readers.base_reader import BaseReader


class DummyReader(BaseReader):
    def read_input_data(self, filename: str) -> Any:
        return []
