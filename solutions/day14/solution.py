import re
from collections import defaultdict, Counter
from typing import List

from solutions.runner.base_solution import BaseSolution
from solutions.runner.readers.lines import LinesReader


class Day14Reader(LinesReader):
    @staticmethod
    def transform_raw_line(line: str):
        if line.startswith("mask"):
            value = line.replace(" ", "").split("=")[1]
            return "mask", value
        memory_address, value = re.match(r"mem\[(\d+)\] = (\d+)", line).groups()
        return int(memory_address), int(value)


class Day14Solution(BaseSolution):
    __reader__ = Day14Reader

    def solve_first(self):
        memory = defaultdict(int)
        mask: str = ""
        for op, val in self.input_data:
            if op == "mask":
                mask = val
            else:
                memory[op] = self.apply_mask(val, mask, 1)[0]
        return sum(memory.values())

    @staticmethod
    def apply_mask(val: int, mask: str, version: int) -> List[int]:
        def _mask_value(val: int, mask:str, no_change_char: str) -> str:
            return "".join([bit if mask_bit == no_change_char else mask_bit for mask_bit, bit in zip(mask, f"{val:036b}")])
        if version == 1:
            return [int(_mask_value(val, mask, "X"), base=2)]
        if version == 2:
            masked_val = _mask_value(val, mask, "0")
            n_x = Counter(masked_val)["X"]
            if not n_x:
                return [int(masked_val, base=2)]

            parallel_values = []
            masked_val_template = masked_val.replace("X", "{}")
            for floating_combination in range(2 ** n_x):
                floating_combination = list(f"{floating_combination:b}".rjust(n_x, "0"))
                parallel_values.append(int(masked_val_template.format(*floating_combination), base=2))
            return parallel_values

    def solve_second(self):
        memory = defaultdict(int)
        mask: str = ""
        for op, val in self.input_data:
            if op == "mask":
                mask = val
            else:
                for masked_addr in self.apply_mask(op, mask, 2):
                    memory[masked_addr] = val

        return sum(memory.values())
