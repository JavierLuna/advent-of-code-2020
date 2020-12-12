from dataclasses import dataclass
from typing import Tuple

from solutions.runner.base_solution import BaseSolution
from solutions.runner.readers.lines import BaseReader


class Day12Reader(BaseReader):
    @staticmethod
    def transform_raw_line(line: str):
        return line[0], int(line[1:])


@dataclass
class Coordinate:
    x: int = 0
    y: int = 0


@dataclass
class Ship(Coordinate):
    facing: int = 90

    @property
    def orientation(self) -> str:
        return "NESW"[int(self.facing / 90)]


class Day12Solution(BaseSolution):
    __reader__ = Day12Reader

    def solve_first(self):
        ship = Ship()
        for op, val in self.input_data:
            self._execute_simple(ship, op, val)
        return abs(ship.x) + abs(ship.y)

    def _execute_simple(self, ship: Ship, op: str, val: int):
        self._move_orientation(ship, op, val)
        if op == "F":
            self._execute_simple(ship, ship.orientation, val)
        if op == "L":
            ship.facing = (ship.facing - val) % 360
        if op == "R":
            ship.facing = (ship.facing + val) % 360

    @staticmethod
    def _move_orientation(c: Coordinate, orientation: str, val: int):
        deltas = {
            "N": (0, 1),
            "S": (0, -1),
            "E": (1, 0),
            "W": (-1, 0)
        }
        d_x, d_y = deltas.get(orientation, (0, 0))
        c.x, c.y = c.x + val * d_x, c.y + val * d_y

    @staticmethod
    def _rotate_coordinate(c: Coordinate, deg: int):
        """
        Fast rotate. No trigonometry as degrees are always either 90, 180 or 270.
        """
        if deg in {90, 270}:
            c.x, c.y = c.y, c.x
        if deg in {180, 270}:
            c.x *= -1
        if deg in {90, 180}:
            c.y *= -1

    def _execute_with_waypoint(self, ship: Ship, waypoint: Coordinate, op: str, val: int) -> Tuple[Ship, Coordinate]:
        self._move_orientation(waypoint, op, val)
        if op == "F":
            ship.x += waypoint.x * val
            ship.y += waypoint.y * val
        if op in "RL":
            if op == "L":
                val = 360 - val
            self._rotate_coordinate(waypoint, val)
        return ship, waypoint

    def solve_second(self):
        ship = Ship()
        waypoint = Coordinate(10, 1)
        for op, val in self.input_data:
            self._execute_with_waypoint(ship, waypoint, op, val)
        return abs(ship.x) + abs(ship.y)
