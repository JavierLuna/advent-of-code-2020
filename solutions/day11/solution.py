from collections import defaultdict, Counter
from dataclasses import dataclass
from typing import List, Dict, Tuple, Set
from copy import deepcopy

from solutions.runner.base_solution import BaseSolution
from solutions.runner.readers.lines import LinesReader


class Day11Reader(LinesReader):
    @staticmethod
    def transform_raw_line(line: str):
        return list(line)


COORDINATE = Tuple[int, int]


@dataclass
class GridMode:
    limit: bool = True
    occupied_to_empty: int = 4


class Grid:
    EMPTY_SEAT = "L"
    FLOOR = "."
    OCCUPIED_SEAT = "#"

    def __init__(self, grid_data: List[List[str]], grid_mode: GridMode):
        self.grid_data = grid_data
        self.non_floor_coords = self._get_non_floor_cords()
        self.adjacents: Dict[COORDINATE, Set[COORDINATE]] = self._get_adjacents(grid_mode.limit)
        self.grid_mode = grid_mode

    def next(self):
        next_grid_data: List[Tuple[int, int, str]] = []
        for x, y in self.non_floor_coords:
            next_grid_data.append((x, y, self.transform_cell(x, y)))
        for x, y, seat in next_grid_data:
            self.grid_data[y][x] = seat

    def get_counter(self) -> Counter:
        return Counter("".join("".join(row) for row in self.grid_data))

    def transform_cell(self, x: int, y: int) -> str:
        seat = self.grid_data[y][x]
        if seat == self.EMPTY_SEAT and sum(
                self.grid_data[y_a][x_a] == self.OCCUPIED_SEAT for x_a, y_a in self.adjacents[(x, y)]) == 0:
            return self.OCCUPIED_SEAT
        if seat == self.OCCUPIED_SEAT and sum(
                self.grid_data[y_a][x_a] == self.OCCUPIED_SEAT for x_a, y_a in
                self.adjacents[(x, y)]) >= self.grid_mode.occupied_to_empty:
            return self.EMPTY_SEAT
        return seat

    def _get_adjacents(self, limit: bool) -> Dict[COORDINATE, Set[COORDINATE]]:
        adjacents = defaultdict(set)
        for x, y in self.non_floor_coords:
            adjacents[(x, y)] = self.get_cell_adjacents(x, y, limit)

        return adjacents

    def get_cell_adjacents(self, x: int, y: int, limit: bool) -> Set[COORDINATE]:
        adjacents = set()
        max_i = len(self.grid_data)
        if limit:
            max_i = 1

        for j_sign, i_sign in {(1, -1), (1, 1), (1, 0), (-1, -1), (-1, 1), (-1, 0), (0, -1), (0, 1)}:
            i, j = 0, 0
            for _ in range(1, max_i + 1):
                i, j = i + i_sign, j + j_sign
                if 0 <= y + i < len(self.grid_data) and \
                        0 <= x + j < len(self.grid_data[0]) and \
                        self.grid_data[y + i][x + j] != self.FLOOR:
                    adjacents.add((x + j, y + i))
                    break
        return adjacents

    def _get_non_floor_cords(self) -> Set[COORDINATE]:
        non_floor_cords = set()
        for y, row in enumerate(self.grid_data):
            for x, seat in enumerate(row):
                if seat != self.FLOOR:
                    non_floor_cords.add((x, y))
        return non_floor_cords

    def __str__(self):
        return "\n".join("".join(row) for row in self.grid_data)


class Day11Solution(BaseSolution):
    __reader__ = Day11Reader

    def solve_first(self):
        return self.generic_solve(self.input_data, GridMode(True, 4))

    def generic_solve(self, input_data, grid_mode: GridMode):
        grid = Grid(deepcopy(input_data), grid_mode)
        old_grid_data = None
        while 1:
            if old_grid_data == grid.grid_data:
                break
            old_grid_data = deepcopy(grid.grid_data)
            grid.next()
        return grid.get_counter()[grid.OCCUPIED_SEAT]

    def solve_second(self):
        return self.generic_solve(self.input_data, GridMode(False, 5))
