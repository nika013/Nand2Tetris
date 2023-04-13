from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from n2t.core.assembler.entities import SymbolsTable, Validator


@dataclass
class Assembler:
    validator: Validator = Validator()
    symb_table: SymbolsTable = SymbolsTable()

    def my_init(self) -> None:
        self.symb_table = SymbolsTable()
        self.validator = Validator()

    @classmethod
    def create(cls) -> Assembler:
        return cls()

    def assemble(self, assembly: Iterable[str]) -> Iterable[str]:
        self.my_init()
        assembly = self.validator.validate(assembly, self.symb_table)
        for instruction in assembly:
            yield self.assemble_one(instruction)

    def assemble_one(self, instruction: str) -> str:
        if instruction[0] == "@":
            return self.deal_a_instruction(instruction)
        else:
            return self.deal_c_instruction(instruction)

    def deal_a_instruction(self, a_instr: str) -> str:
        symbol = a_instr[1:].split()[0]
        if self.symb_table.is_symbol(symbol):
            value = self.symb_table.get(symbol)
        elif not symbol[0].isnumeric():
            self.symb_table.add(symbol)
            value = int(self.symb_table.get(symbol))
        else:
            value = int(symbol)
        zeros = "0000000000000000"
        to_binary = bin(value)[2:]
        res = zeros[: -len(to_binary)] + to_binary
        # print(res)
        return res

    def deal_c_instruction(self, c_instr: str) -> str:
        res = "111"
        if "=" in c_instr and ";" in c_instr:
            operations = c_instr.split("=")
            comp_and_jump = operations[1].split(";")
            dest = operations[0]
            comp = comp_and_jump[0]
            jump = comp_and_jump[1]
            first = self.symb_table.get_comp(comp)
            second = self.symb_table.get_dest(dest)
            third = self.symb_table.get_jump(jump)
            res += first + second + third
        elif "=" in c_instr and ";" not in c_instr:
            dest_and_comp = c_instr.split("=")
            # print(c_instr)
            # print(dest_and_comp[0], dest_and_comp[1].split()[0])
            left = self.symb_table.get_comp(dest_and_comp[1].split()[0])
            right = self.symb_table.get_dest(dest_and_comp[0])
            res += left + right + "000"
        elif ";" in c_instr and "=" not in c_instr:
            comp_and_jump = c_instr.split(";")
            # print("printiiiiing")
            # print(comp_and_jump[0].split()[0])
            # print(comp_and_jump[1].split()[0])
            left = self.symb_table.get_comp(comp_and_jump[0].split()[0])
            right = self.symb_table.get_jump(comp_and_jump[1].split()[0])
            # print(left)
            # print(right)
            res += left + "000" + right
        else:
            res += self.symb_table.get_comp(c_instr.split()[0]) + "000000"
        return res
