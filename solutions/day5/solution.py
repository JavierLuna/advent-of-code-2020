import functools
from solutions.runner.base_solution import BaseSolution
from solutions.runner.readers.base_reader import BaseReader


class Day5Reader(BaseReader):
    @staticmethod
    def transform_raw_line(line: str):
        line = line.strip()
        row, column = line[:7], line[7:]
        return row.replace("F", "0").replace("B", "1"), column.replace("L", "0").replace("R", "1")


class Day5Solution(BaseSolution):
    __reader__ = Day5Reader

    def solve_first(self):
        seat_ids = []
        for identifier in self.input_data:
            row, column = identifier
            seat_id = self._funnel(0, 127, row) * 8 + self._funnel(0, 7, column)
            seat_ids.append(seat_id)
        seat_ids = sorted(seat_ids)
        self.bag['seat_ids'] = seat_ids
        return seat_ids[-1]

    def _funnel(self, low_bound: int, high_bound: int, values: str) -> int:
        if not values:
            return low_bound
        bound = self._get_bounds(low_bound, high_bound)[int(values[0])]
        return self._funnel(*bound, values=values[1:])

    @functools.lru_cache(maxsize=None)
    def _get_bounds(self, low_bound: int, high_bound: int):
        middle = int((high_bound - low_bound) / 2) + low_bound
        return (low_bound, middle), (middle + 1, high_bound)

    def solve_second(self):
        seat_ids = self.bag['seat_ids']
        for real_seat_id, control_seat_id in zip(seat_ids, range(seat_ids[0], seat_ids[-1] + 1)):
            if real_seat_id != control_seat_id:
                return control_seat_id
