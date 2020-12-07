import re
from typing import Tuple, List, Set, Dict
import functools

from solutions.runner.base_solution import BaseSolution
from solutions.runner.readers.groups import DictionaryGroupReader


class Day7Reader(DictionaryGroupReader):
    @staticmethod
    def transform_raw_line(line: str):
        transformed_line = {}
        container, content = line.strip().split("contain")
        container = container.replace("bags", "").strip()
        transformed_line[container] = set()
        if content != " no other bags.":
            for bag in content[:-1].split(", "):
                match = re.match(r"(\d+) (.*) bags?", bag.strip())
                transformed_line[container].add((int(match[1]), match[2]))
        return transformed_line


class Day7Solution(BaseSolution):
    __reader__ = Day7Reader

    TARGET = "shiny gold"

    def solve_first(self):

        different_bags = functools.reduce(lambda a, b: set(a).union(set(b)),
                                          self._get_all_paths_to_target(self.TARGET, self.input_data[0]))
        return len(different_bags) - 1

    def _get_all_paths_to_target(self,
                                 target: str,
                                 graph: Dict[str, Set[Tuple[int, str]]]) -> List[List[str]]:
        conclusive_paths: List[List[str]] = []
        known_conclusive_nodes: Set[str] = set()
        paths_to_expand: List[List[str]] = [[k] for k in set(graph.keys()).difference({target})]
        while paths_to_expand:
            path = paths_to_expand.pop()
            neighbors = [neighborg for _, neighborg in graph[path[-1]] if neighborg not in path]
            for neighbor in neighbors:
                if neighbor == target or neighbor in known_conclusive_nodes:
                    conclusive_paths.append(path + [neighbor])
                    known_conclusive_nodes.add(neighbor)
                else:
                    paths_to_expand.append(path + [neighbor])
        return conclusive_paths

    def solve_second(self):
        return self._recursive_find(self.TARGET, self.input_data[0])

    def _recursive_find(self, current_bag: str, bag_data: Dict[str, Set[Tuple[int, str]]]) -> int:
        return sum(a + a * self._recursive_find(b, bag_data) for a, b in bag_data[current_bag])
