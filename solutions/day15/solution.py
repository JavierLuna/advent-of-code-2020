from collections import defaultdict
from typing import List

from solutions.runner.base_solution import BaseSolution
from solutions.runner.readers.lines import LinesReader


class Day15Reader(LinesReader):
    @staticmethod
    def transform_raw_line(line: str):
        return [int(n) for n in line.split(",")]


class Day15Solution(BaseSolution):
    __reader__ = Day15Reader

    def solve_first(self):
        max_turns = 2020
        numbers = self.input_data[0]
        return self._play_game(numbers, max_turns)

    @staticmethod
    def _play_game(numbers: List[int], max_turn: int) -> int:
        memory = defaultdict(list)
        [memory[n].append(t + 1) for t, n in enumerate(numbers)]
        last_spoken = numbers[-1]
        for turn in range(len(memory) + 1, max_turn + 1):
            if 1 < len(memory[last_spoken]):
                last_spoken = memory[last_spoken][-1] - memory[last_spoken][-2]
            else:
                last_spoken = 0
            memory[last_spoken].append(turn)
        return last_spoken

    def solve_second(self):
        # I have a 3.7Ghz CPU and haven't showered yet elves what did you expect huh?
        # I have to say what a shitty challenge of yours I hope it was worth it now
        # I smell like flowers and you smell like embarrassment. What, do these numbers
        # follow a weird series or do they repeat themselves or something? Guess what
        # let me care about that when I'm bored but I have an overpowered CPU that isn't
        # used that much aside from shitty python scripts and Minecraft and you know
        # damn well Im going to brute force this right here. See ya later lil hommies.
        max_turns = 30000000
        numbers = self.input_data[0]
        return self._play_game(numbers, max_turns)
