import itertools
import math

from solutions.runner.base_solution import BaseSolution
from solutions.runner.readers.lines import LinesReader


class Day13Reader(LinesReader):
    @staticmethod
    def transform_raw_line(line: str):
        if line.isnumeric():
            return int(line)
        return sorted([(i, int(bus_id)) for i, bus_id in enumerate(line.split(',')) if bus_id != "x"])


class Day13Solution(BaseSolution):
    __reader__ = Day13Reader

    def solve_first(self):
        original_timestamp, bus_ids = self.input_data
        next_timestamps = sorted([(bus_id, bus_id * math.ceil(original_timestamp / bus_id)) for _, bus_id in bus_ids],
                                 key=lambda a: a[1])
        bus_id, timestamp = next_timestamps[0]
        return (timestamp - original_timestamp) * bus_id

    def solve_second(self):
        bus_ids = self.input_data[1]
        offset, period = 0, 1
        for i, bus_id in bus_ids:
            occurrences = (occurrence for occurrence in itertools.count(offset, period) if
                           not (occurrence + i) % bus_id)
            offset = next(occurrences)
            period = next(occurrences) - offset
        return offset
