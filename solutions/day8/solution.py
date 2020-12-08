from collections import defaultdict
from dataclasses import dataclass, field
from typing import Tuple, List, Dict

from solutions.runner.base_solution import BaseSolution
from solutions.runner.readers.lines import LinesReader


class InstructionReader(LinesReader):
    @staticmethod
    def transform_raw_line(line: str):
        op, num = line.split(" ")
        return op, int(num)


@dataclass
class VMState:
    instructions: List[Tuple[str, int]]
    p_i: int = 0
    acc: int = 0
    n_exec_per_instruction: Dict[int, int] = field(default_factory=lambda: defaultdict(int))

    @property
    def instruction(self) -> Tuple[str, int]:
        return self.instructions[self.p_i]

    def has_finished_execution(self) -> bool:
        return self.p_i >= len(self.instructions)

    def reset(self):
        self.p_i = 0
        self.acc = 0
        self.n_exec_per_instruction = defaultdict(int)

    def __str__(self):
        op, arg = ("finished", 1) if self.has_finished_execution() else self.instruction
        return f"<VM acc: {self.acc} | current_instruction: '{op} {arg}' (executed {self.n_exec_per_instruction[self.p_i]} times) | p_i: {self.p_i}  >"

    def __repr__(self):
        return str(self)


class VMExecutor:
    UNLIMITED_LOOPS = -1

    @staticmethod
    def execute_op(vm_state: VMState) -> VMState:
        op, arg = vm_state.instruction
        op_p_i = vm_state.p_i
        vm_state.prev_pi = vm_state.p_i
        vm_state.p_i += 1
        if op == "acc":
            vm_state.acc += arg
        if op == "jmp":
            vm_state.p_i = op_p_i + arg
        vm_state.n_exec_per_instruction[op_p_i] += 1
        return vm_state

    @classmethod
    def execute_vm(cls, vm_state: VMState, loop_limit: int = UNLIMITED_LOOPS) -> VMState:
        while not vm_state.has_finished_execution() and (
                loop_limit == cls.UNLIMITED_LOOPS or vm_state.n_exec_per_instruction[vm_state.p_i] < loop_limit):
            cls.execute_op(vm_state)
        return vm_state


class Day8Solution(BaseSolution):
    __reader__ = InstructionReader

    def solve_first(self):
        vm_state = VMState(self.input_data)
        VMExecutor.execute_vm(vm_state, loop_limit=1)
        return vm_state.acc

    def solve_second(self):
        possible_suspects = self._generate_possible_suspects(self.input_data)
        vm_state = VMState(self.input_data)

        for suspect in possible_suspects:
            vm_state = self._flip_instruction(vm_state, suspect)
            vm_state = VMExecutor.execute_vm(vm_state, loop_limit=1)
            if vm_state.has_finished_execution():
                return vm_state.acc
            vm_state.reset()
            self._flip_instruction(vm_state, suspect)

    @staticmethod
    def _flip_instruction(vm_state: VMState, p_i: int) -> VMState:
        mods = {"nop": "jmp", "jmp": "nop"}
        op, arg = vm_state.instructions[p_i]
        vm_state.instructions[p_i] = (mods[op], arg)
        return vm_state

    @staticmethod
    def _generate_possible_suspects(instructions: List[Tuple[str, int]]) -> List[int]:
        possible_suspects: List[int] = []
        for p_i, (op, arg) in enumerate(instructions):
            if op == "nop":
                if arg == 0:
                    continue
                possible_suspects.append(p_i)
            if op == "jmp":
                if arg == 0:
                    possible_suspects = [p_i]
                    break
                possible_suspects.append(p_i)
        return possible_suspects
