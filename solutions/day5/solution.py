from solutions.runner.base_solution import BaseSolution
from solutions.runner.readers.base_reader import BaseReader


class Day5Reader(BaseReader):
    @staticmethod
    def transform_raw_line(line: str):
        return int("".join("01"[c in {"B", "R"}] for c in line.strip()), base=2)


class Day5Solution(BaseSolution):
    __reader__ = Day5Reader

    def solve_first(self):
        self.bag['seat_ids'] = sorted(self.input_data)
        return self.bag['seat_ids'][-1]

    def solve_second(self):
        seat_ids = self.bag['seat_ids']
        for real_seat_id, control_seat_id in zip(seat_ids, range(seat_ids[0], seat_ids[-1] + 1)):
            if real_seat_id != control_seat_id:
                return control_seat_id
