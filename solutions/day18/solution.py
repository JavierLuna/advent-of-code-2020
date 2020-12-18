from solutions.day18.executor import execute_expression
from solutions.day18.parsers import Part1Parser, Part2Parser
from solutions.runner.base_solution import BaseSolution
from solutions.runner.readers.lines import LinesReader


class Day18Solution(BaseSolution):
    __reader__ = LinesReader

    def solve_first(self):
        return sum(execute_expression(expression, Part1Parser) for expression in self.input_data)

    def solve_second(self):
        return sum(execute_expression(expression, Part2Parser) for expression in self.input_data)
