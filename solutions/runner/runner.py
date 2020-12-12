import importlib
import os
import json
from collections import defaultdict
from typing import Optional

from solutions.runner.base_solution import BaseSolution
from solutions.runner.config import SOLUTIONS_FOLDER, INPUTS_FOLDER
from solutions.runner.formatting import Color, print_sol
from solutions.runner.hash_utils import md5_dir


class SolutionRunner:

    def __init__(self, cache_path: Optional[str] = ".aoc_2020"):
        self._solution_cache = defaultdict(list)
        self._cache_path = cache_path
        if self._cache_path:
            self.load_cache(cache_path)

    def run_all(self):
        all_solutions = sorted([directory for directory in next(os.walk(SOLUTIONS_FOLDER))[1] if
                                directory.startswith("day")], key=lambda day: int(day[3:]))
        print(f"Solutions found for the following days: {', '.join(all_solutions)}\n")
        for solution in all_solutions:
            self.run_solution(solution)
        if self._cache_path:
            self.save_cache(self._cache_path)

    def run_solution(self, day: str):
        hash_input, hash_solution = [md5_dir(os.path.join(parent_folder, day)) for parent_folder in
                                     [INPUTS_FOLDER, SOLUTIONS_FOLDER]]
        general_hash = hash_input + hash_solution
        loaded_module = importlib.import_module(f"solutions.{day}.solution")
        possible_solution_solver = [member for member in loaded_module.__dict__.values() if
                                    isinstance(member, type) and member != BaseSolution and issubclass(member,
                                                                                                       BaseSolution)]
        assert len(possible_solution_solver) == 1, f"Solvers found for {day}: {len(possible_solution_solver)}"

        print(f"\n\t\t🎄⭐ {Color.BGREEN}~{day.capitalize()}~{Color.CLEAR} ⭐🎄 \n")
        if general_hash in self._solution_cache:
            print_sol(1, self._solution_cache[general_hash][0])
            print_sol(2, self._solution_cache[general_hash][1])
        else:
            solution = possible_solution_solver[0]()
            self._solution_cache[general_hash] = list(solution.solve())
            del solution

    def load_cache(self, cache_path: str):
        if not os.path.isfile(cache_path):
            print(f"Cache file '{cache_path}' not found, empty cache!")
            return
        with open(cache_path) as file:
            self._solution_cache = json.load(file)

    def save_cache(self, cache_path: str):
        with open(cache_path, 'w') as file:
            json.dump(self._solution_cache, file)
