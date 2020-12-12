import inspect
import os
import sys
from abc import ABCMeta, abstractmethod
from typing import Dict

from solutions.runner.config import INPUTS_FOLDER
from solutions.runner.formatting import Color, print_sol
from solutions.runner.readers.numeric import IntListReader


class BaseSolution(metaclass=ABCMeta):
    __input_files__: Dict[str, str] = {
        "solve_first": "input.txt",
        "solve_second": "input.txt"
    }

    __reader__ = IntListReader

    def __init__(self):
        self._input_data = None
        self._reader = self.__reader__()
        self._solutions = {
            "solve_first": None,
            "solve_second": None
        }
        self.bag = {}

    def solve(self) -> tuple:
        self._solutions["solve_first"] = self.solve_first()
        print_sol(1, self._solutions["solve_first"])
        self._solutions["solve_second"] = self.solve_second()
        print_sol(2, self._solutions["solve_second"])
        return self._solutions["solve_first"], self._solutions["solve_second"]

    @abstractmethod
    def solve_first(self):
        pass

    @abstractmethod
    def solve_second(self):
        pass

    @property
    def input_data(self):
        curframe = inspect.currentframe()
        calframe = inspect.getouterframes(curframe, 2)
        caller_name = calframe[1][3]
        if caller_name not in self.__input_files__:
            raise Exception(f"Property caller must be one of the following: {list(self.__input_files__)}")
        return self.get_input_data(self.__input_files__[caller_name])

    def get_input_data(self, filename: str):
        full_path = os.path.join(INPUTS_FOLDER, self._get_solution_day(), filename)
        return self._reader.read_input_data(full_path)

    @classmethod
    def _get_solution_day(cls):
        filename = sys.modules[cls.__module__].__file__
        day_name = filename.split(os.sep)[-2]
        return day_name
