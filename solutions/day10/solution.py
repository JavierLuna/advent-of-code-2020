from collections import defaultdict

from solutions.runner.base_solution import BaseSolution
from solutions.runner.readers.numeric import IntListReader


class Day8Solution(BaseSolution):
    __reader__ = IntListReader

    def solve_first(self):
        sorted_adapters = sorted(self.input_data)
        self.bag["sorted_input"] = sorted_adapters = [0] + sorted_adapters + [sorted_adapters[-1] + 3]
        current_jolt = 0
        differences = defaultdict(int)
        for adapter in sorted_adapters[1:]:
            differences[adapter - current_jolt] += 1
            current_jolt = adapter
        return differences[1] * differences[3]

    def solve_second(self):
        adapters = self.bag["sorted_input"]
        arrangement_count = [1]
        for i in range(1, len(adapters)):
            past_arrangements = 0
            for j in range(max(0, i - 3), i):
                if adapters[j] + 3 >= adapters[i]:
                    past_arrangements += arrangement_count[j]
            arrangement_count.append(past_arrangements)
        return arrangement_count[-1]
