import re
from math import prod

from solutions.runner.base_solution import BaseSolution
from solutions.runner.readers.base_reader import BaseReader


class Day16Reader(BaseReader):
    def _read_lines(self,
                    filename: str,
                    omit_empty: bool = True,
                    use_cache: bool = True):
        data = {"conditions": [],
                "tickets": []}
        with open(filename) as file:
            for line in file:
                line = line.strip()
                if match := re.match(r"(.+): (\d+)-(\d+) or (\d+)-(\d+)", line):
                    groups = match.groups()
                    data["conditions"].append({"name": groups[0],
                                               "limits": set(range(int(groups[1]), int(groups[2]) + 1)).union(
                                                   set(range(int(groups[3]), int(groups[4]) + 1)))
                                               })
                if re.match(r"\d", line):
                    data['tickets'].append([int(n) for n in line.split(",")])
        data["my_ticket"] = data["tickets"].pop(0)
        return data

    def read_input_data(self, filename: str):
        return self._read_lines(filename)


class Day16Solution(BaseSolution):
    __reader__ = Day16Reader

    def solve_first(self):
        scanning_error_rate = 0
        valid_nums = set()
        invalid_vals = set()
        self.bag["valid_tickets"] = list()

        for i, ticket in enumerate(self.input_data["tickets"]):
            valid_ticket = True
            for val in ticket:
                if val in valid_nums:
                    continue
                if val in invalid_vals or not self.check_conditions(val, self.input_data["conditions"]):
                    scanning_error_rate += val
                    invalid_vals.add(val)
                    valid_ticket = False
                    break
                valid_nums.add(val)
            if valid_ticket:
                self.bag["valid_tickets"].append(ticket)
        return scanning_error_rate

    def check_conditions(self, val: int, conditions: list) -> bool:
        return any(self.check_condition(val, c) for c in conditions)

    def check_condition(self, val: int, condition: dict) -> bool:
        return val in condition["limits"]

    def solve_second(self):
        conditions = list(self.input_data["conditions"])
        tickets = [self.input_data["my_ticket"]] + self.bag["valid_tickets"]
        final_conditions = []
        for i in range(len(self.input_data["my_ticket"])):
            final_conditions.append([])
            for j, condition in enumerate(conditions[:]):

                if all(self.check_condition(ticket[i], condition) for ticket in tickets):
                    final_conditions[-1].append(condition["name"])

        while not all(len(final_condition) == 1 for final_condition in final_conditions):
            for i, final_condition in enumerate(final_conditions[:]):
                if len(final_condition) == 1:
                    condition = final_condition[0]
                    for j, f_conditions in enumerate(final_conditions):
                        if i != j and condition in f_conditions:
                            f_conditions.remove(condition)

        return prod(
            val for val, label in zip(self.input_data["my_ticket"], final_conditions) if label[0].startswith("departure"))
