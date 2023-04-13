from typing import Iterable


class SymbolsTable:
    symbols_map = {
        "R0": 0,
        "R1": 1,
        "R2": 2,
        "R3": 3,
        "R4": 4,
        "R5": 5,
        "R6": 6,
        "R7": 7,
        "R8": 8,
        "R9": 9,
        "R10": 10,
        "R11": 11,
        "R12": 12,
        "R13": 13,
        "R14": 14,
        "R15": 15,
        "SCREEN": 16384,
        "KBD": 24576,
        "SP": 0,
        "LCL": 1,
        "ARG": 2,
        "THIS": 3,
        "THAT": 4,
    }

    destination_map = {
        "": "000",
        "M": "001",
        "D": "010",
        "MD": "011",
        "A": "100",
        "AM": "101",
        "AD": "110",
        "AMD": "111",
    }

    jump_map = {
        "": "000",
        "JGT": "001",
        "JEQ": "010",
        "JGE": "011",
        "JLT": "100",
        "JNE": "101",
        "JLE": "110",
        "JMP": "111",
    }

    comp_map = {
        "0": "0101010",
        "1": "0111111",
        "-1": "0111010",
        "D": "0001100",
        "A": "0110000",
        "M": "1110000",
        "!D": "0001101",
        "!A": "0110001",
        "!M": "1110001",
        "-D": "0001111",
        "-A": "0110011",
        "-M": "1110011",
        "D+1": "0011111",
        "A+1": "0110111",
        "M+1": "1110111",
        "D-1": "0001110",
        "A-1": "0110010",
        "M-1": "1110010",
        "D+A": "0000010",
        "D+M": "1000010",
        "D-A": "0010011",
        "A-D": "0000111",
        "D-M": "1010011",
        "M-D": "1000111",
        "D&A": "0000000",
        "D&M": "1000000",
        "D|A": "0010101",
        "D|M": "1010101",
    }

    def get_comp(self, comp: str) -> str:
        return self.comp_map.get(comp)

    def get_jump(self, jump: str) -> str:
        return self.jump_map.get(jump)

    def get_dest(self, dest: str) -> str:
        return self.destination_map.get(dest)

    def __init__(self) -> None:
        self.free_register = 16

    def is_symbol(self, symb: str) -> bool:
        return symb in self.symbols_map.keys()

    def get(self, symb: str) -> int:
        if self.is_symbol(symb):
            return self.symbols_map.get(symb)
        else:
            raise Exception("InvalidSyntaxException")

    def add(self, key: str, value: int = -1) -> None:
        if value == -1:
            self.symbols_map[key] = self.free_register
            self.free_register += 1
        else:
            self.symbols_map[key] = value


class Validator:
    def __init__(self) -> None:
        pass

    @staticmethod
    def is_label(instr: str) -> bool:
        return instr[0] == "(" and instr[-1] == ")"

    def save_label(self, instr: str, symb_table: SymbolsTable, cur_num: int) -> None:
        if not symb_table.is_symbol(instr):
            symb_table.add(instr[1:-1], cur_num)

    @staticmethod
    def is_comment(instr: str) -> bool:
        return instr[0:2] == "//"

    def not_valid(self, instr: str) -> bool:
        return self.is_comment(instr) or instr.isspace() or not instr

    def validate(self, assembly: Iterable[str], table: SymbolsTable) -> Iterable[str]:
        validated_assembly = []
        validated_instructions = 0

        for instruction in assembly:
            if self.not_valid(instruction):
                continue
            elif self.is_label(instruction):
                self.save_label(instruction, table, validated_instructions)
            else:
                validated_assembly.append(instruction)
                validated_instructions += 1

        return validated_assembly
