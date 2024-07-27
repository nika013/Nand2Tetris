from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Iterable

from n2t.core.hack_simulator.entities import Ram


def to_positive(number: int) -> int:
    positive_binary = bin(abs(number))[2:].zfill(16)
    flip_table = positive_binary.maketrans("01", "10")
    flipped_string = positive_binary.translate(flip_table)
    to_binary = bin(int(flipped_string, 2) + 1)
    return int(to_binary[2:], 2)


@dataclass
class HackSimulator:
    instructions: Iterable[str]
    cycles: int

    @classmethod
    def create(cls, instructions, cycles) -> HackSimulator:
        return cls(instructions, cycles)

    def execute(self) -> Iterable[str]:
        self.ram_states: Ram = Ram()
        instr_list = list(self.instructions)
        instr_size = len(instr_list)
        self.a_register: int = 0
        self.d_register: int = 0
        self.pc: int = 0

        while self.cycles > 0:
            if self.pc >= instr_size:
                break
            instruction = instr_list[self.pc]
            if instruction[0] == "0":
                self.deal_a_instruction(instruction)
            elif instruction[0] == "1":
                self.deal_c_instruction(instruction)
            self.cycles -= 1
        return self.to_json(self.ram_states)

    def deal_c_instruction(self, instruction: str) -> None:
        comp = instruction[3:10]
        dest = instruction[10:13]
        jump = instruction[13:]

        value: int = self.deal_compare(comp)
        self.deal_destination(dest, value)
        self.deal_jump(jump, value)

    def deal_compare(self, comp: str) -> int:
        if comp == "0101010":
            return 0
        elif comp == "0111111":
            return 1
        elif comp == "0111010":
            return -1
        elif comp == "0001100":
            return self.d_register
        elif comp == "0110000":
            return self.a_register
        elif comp == "0001101":
            return ~self.d_register
        elif comp == "0110001":
            return ~self.a_register
        elif comp == "0001111":
            return -self.d_register
        elif comp == "0110011":
            return -self.a_register
        elif comp == "0011111":
            return self.d_register + 1
        elif comp == "0110111":
            return self.a_register + 1
        elif comp == "0001110":
            return self.d_register - 1
        elif comp == "0110010":
            return self.a_register - 1
        elif comp == "0000010":
            return self.d_register + self.a_register
        elif comp == "0010011":
            return self.d_register - self.a_register
        elif comp == "0000111":
            return self.a_register - self.d_register
        elif comp == "0000000":
            return self.d_register & self.a_register
        elif comp == "0010101":
            return self.d_register | self.a_register
        elif comp == "1110000":
            return self.ram_states.get(self.a_register)
        elif comp == "1110001":
            return ~self.ram_states.get(self.a_register)
        elif comp == "1110011":
            return -self.ram_states.get(self.a_register)
        elif comp == "1110111":
            return self.ram_states.get(self.a_register) + 1
        elif comp == "1110010":
            return self.ram_states.get(self.a_register) - 1
        elif comp == "1000010":
            return self.d_register + self.ram_states.get(self.a_register)
        elif comp == "1010011":
            return self.d_register - self.ram_states.get(self.a_register)
        elif comp == "1000111":
            return self.ram_states.get(self.a_register) - self.d_register
        elif comp == "1000000":
            return self.d_register & self.ram_states.get(self.a_register)
        elif comp == "1010101":
            return self.d_register | self.ram_states.get(self.a_register)
        return -1

    def deal_destination(self, dest: str, value: int) -> None:
        if dest == "001":
            self.ram_states.assign(self.a_register, value)
        elif dest == "010":
            self.d_register = value
        elif dest == "011":
            self.ram_states.assign(self.a_register, value)
            self.d_register = value
        elif dest == "100":
            self.a_register = value
        elif dest == "101":
            self.ram_states.assign(self.a_register, value)
            self.a_register = value
        elif dest == "110":
            self.a_register = value
            self.d_register = value
        elif dest == "111":
            self.ram_states.assign(self.a_register, value)
            self.a_register = value
            self.d_register = value

    def deal_jump(self, jump: str, value: int) -> None:
        if jump == "001":
            self.make_jump(value > 0)
        elif jump == "010":
            self.make_jump(value == 0)
        elif jump == "011":
            self.make_jump(value >= 0)
        elif jump == "100":
            self.make_jump(value < 0)
        elif jump == "101":
            self.make_jump(value != 0)
        elif jump == "110":
            self.make_jump(value <= 0)
        elif jump == "111":
            self.pc = self.a_register
            self.make_jump(True)
        elif jump == "000":
            self.pc += 1

    def make_jump(self, condition: bool) -> None:
        if condition:
            self.pc = self.a_register
        else:
            self.pc += 1

    def deal_a_instruction(self, instruction: str) -> None:
        binary_string = instruction[1:]
        decimal_value = int(binary_string, 2)
        self.a_register = decimal_value
        self.pc += 1

    def to_json(self, ram_states: Ram) -> Iterable[str]:
        registers: dict = ram_states.registers

        sorted_registers = {k: registers[k] for k in sorted(registers.keys())}
        for key in sorted_registers:
            if sorted_registers[key] < 0:
                sorted_registers[key] = to_positive(sorted_registers[key])

        json_str = json.dumps({"RAM": sorted_registers}, indent=3)
        return [json_str]
