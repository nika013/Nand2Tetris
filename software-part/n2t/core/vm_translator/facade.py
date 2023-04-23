from dataclasses import dataclass
from typing import Iterable, List


def arithmetic_op(op: str) -> str:
    instr = "D=D+M\n" if op == "+" else "D=M-D\n"
    res = "@SP\n" + "A=M-1\n" + "D=M\n"  # get first num
    res += "A=A-1\n" + instr  # make op second num and save in D register
    res += "M=D\n"  # save new val in proper place of stack
    res += "@SP\n" + "M=M-1"  # decrease stack
    return res


def and_or_asm(op: str) -> str:
    asm = "@SP\n" + "A=M-1\n" + "D=M\n" + "A=A-1\n"
    asm += "M=D" + op + "M\n"
    asm += "@SP\n" + "M=M-1"
    return asm


@dataclass
class VMTranslator:
    @classmethod
    def create(cls):
        return cls()

    def my_init(self) -> None:
        self.cmp = 1

    def translate(self, vm_code: Iterable[str]) -> Iterable[str]:
        self.my_init()
        for command in vm_code:
            if command[0:2] != "//" and command.strip() != "":
                yield self.translate_one(command)

    def translate_one(self, word: str) -> str:
        out = "// " + word + "\n"
        statement = word.split()
        type_command = statement[0]
        if type_command == "push":
            out += self.handle_push(statement)
        elif type_command == "pop":
            out += self.handle_pop(statement)
        elif type_command == "add":
            out += self.handle_arithmetic(type_command)
        elif type_command == "sub":
            out += self.handle_arithmetic(type_command)
        elif type_command == "neg":
            out += self.handle_neg()
        elif type_command == "eq":
            out += self.handle_logicals(type_command)
        elif type_command == "gt":
            out += self.handle_logicals(type_command)
        elif type_command == "lt":
            out += self.handle_logicals(type_command)
        elif type_command == "and":
            out += self.handle_bit_wise(type_command)
        elif type_command == "or":
            out += self.handle_bit_wise(type_command)
        elif type_command == "not":
            out += self.handle_not()
        return out

    def handle_not(self) -> str:
        asm = "@SP\n" + "A=M-1\n" + "M=!M"
        return asm

    def handle_bit_wise(self, type_comm: str) -> str:
        if type_comm == "and":
            return and_or_asm("&")
        elif type_comm == "or":
            return and_or_asm("|")
        return ""

    def handle_logicals(self, log_comm: str) -> str:
        return self.compose_compare(log_comm.upper())

    def compose_compare(self, op: str) -> str:
        cur_cmp = str(self.cmp)
        asm = "@SP\n" + "A=M-1\n" + "D=M\n" + "A=A-1\n" + "D=M-D\n"
        asm += "@TRUE" + cur_cmp + "\n" + "D;J" + op + "\n" + "@SP\n" + "A=M-1\n"
        asm += "A=A-1\n" + "M=0\n" + "@CONT" + cur_cmp + "\n" + "0;JMP\n"
        asm += "(TRUE" + cur_cmp + ")\n" + "@SP\n" + "A=M-1\n" + "A=A-1\n"
        asm += "M=-1\n" + "(CONT" + cur_cmp + ")\n" + "@SP\n" + "M=M-1\n"
        self.cmp += 1
        return asm

    def handle_neg(self) -> str:
        res = "@SP\n" + "A=M-1\n" + "M=-M"
        return res

    def handle_arithmetic(self, type_command: str) -> str:
        if type_command == "add":
            return arithmetic_op("+")
        elif type_command == "sub":
            return arithmetic_op("-")
        else:
            raise ValueError("Some error in handle_arithm method")

    def handle_push(self, statement: List[str]) -> str:
        if statement[2].isnumeric() and statement[1] == "constant":
            return self.save_value(statement[2])
        else:
            return self.move_to_stack(statement)

    def save_value(self, val: str) -> str:
        res = "@" + val + "\n"  # save value at A register
        res += "D=A\n" + "@SP\n" + "A=M\n" + "M=D\n"  # write in RAM[SP] = val
        res += "@SP\n" + "M=M+1"  # sp++
        return res

    def handle_pop(self, statement: List[str]) -> str:
        if len(statement) == 1:
            asm = "@SP\n" + "D=M\n" + "M=M-1\n"
        else:
            segment = self.define_segment(statement[1])
            idx = statement[2]
            if segment == "static" or segment == "temp" or segment == "pointer":
                return self.temp_register_pop(segment, idx)
            asm = "@" + idx + "\n" + "D=A\n"  # save idx
            asm += "@" + segment + "\n" + "D=M+D\n"
            asm += "@15\n" + "M=D\n"  # temporary save
            asm += "@SP\n" + "AM=M-1\n" + "D=M\n"
            asm += "@15\n" + "A=M\n" + "M=D\n"
        return asm

    def move_to_stack(self, statement: List[str]) -> str:
        segment = self.define_segment(statement[1])
        idx = str(statement[2])
        if segment == "static" or segment == "temp" or segment == "pointer":
            return self.temp_register_push(segment, idx)
        res = "@" + idx + "\n" + "D=A\n"  # save idx at D register
        res += "@" + segment + "\n" + "A=M+D\n"  # add offset
        res += "D=M\n" + "@SP\n" + "A=M\n" + "M=D\n"  # save value to stack
        res += "@SP\n" + "M=M+1"  # sp++
        return res

    def temp_register_pop(self, segment: str, idx: str) -> str:
        if segment == "static":
            offset = 16
        elif segment == "temp":
            offset = 5
        elif segment == "pointer":
            offset = 3
        address = str(int(idx) + offset)
        res = "@" + address + "\n" + "D=A\n"
        res += "@15\n" + "M=D\n"
        res += "@SP\n" + "AM=M-1\n" + "D=M\n"
        res += "@15\n" + "A=M\n" + "M=D\n"
        return res

    def temp_register_push(self, segment: str, idx: str) -> str:
        if segment == "static":
            offset = 16
        elif segment == "temp":
            offset = 5
        elif segment == "pointer":
            offset = 3
        address = str(int(idx) + offset)
        res = "@" + address + "\n" + "D=M\n"
        res += "@SP\n" + "A=M\n" + "M=D\n"
        res += "@SP\n" + "M=M+1"  # sp++
        return res

    def define_segment(self, segment: str) -> str:
        if segment == "local":
            return "LCL"
        elif segment == "argument":
            return "ARG"
        elif segment == "this":
            return "THIS"
        elif segment == "that":
            return "THAT"
        elif segment == "static":
            return "static"
        elif segment == "temp":
            return "temp"
        elif segment == "pointer":
            return "pointer"
        return ""
