import importlib
import os

from solutions.runner.base_solution import BaseSolution


class SolutionRunner:

    def run_all(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        all_solutions = sorted([directory for directory in next(os.walk(os.path.dirname(dir_path)))[1] if
                         directory.startswith("day")], key=lambda day: int(day[3:]))
        print(f"Solutions found for the following days: {', '.join(all_solutions)}\n")
        for solution in all_solutions:
            self.run_solution(solution)

    def run_solution(self, day: str):
        loaded_module = importlib.import_module(f"solutions.{day}.solution")
        possible_solution_solver = [member for member in loaded_module.__dict__.values() if
                                    isinstance(member, type) and member != BaseSolution and issubclass(member,
                                                                                                       BaseSolution)]

        print("=" * 40)
        print(f"Running solutions for {day}: \n")
        for solution in possible_solution_solver:
            solution = solution()
            solution.solve()
        print("=" * 40, "\n\n")
