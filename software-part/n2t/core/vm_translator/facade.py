from dataclasses import dataclass
from typing import Iterable
from n2t.core.vm_translator.entities import Stack
from typing import List


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
    st: Stack = Stack()

    @classmethod
    def create(cls):
        return cls()

    def my_init(self) -> None:
        self.st = Stack()
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
            out += self.handle_pop()
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
        num = self.st.pop()
        self.st.push(~num)
        asm = "@SP\n" + "A=M-1\n" + "M=!M"
        return asm

    def handle_bit_wise(self, type_comm: str) -> str:
        y = self.st.pop()
        x = self.st.pop()
        if type_comm == "and":
            op = "&"
            self.st.push(x & y)
            return and_or_asm(op)
        elif type_comm == "or":
            op = "|"
            self.st.push(x | y)
            return and_or_asm(op)

    def handle_logicals(self, log_comm: str) -> str:
        y = self.st.pop()
        x = self.st.pop()
        if log_comm == "eq":
            self.st.push(1 if x == y else 0)
        elif log_comm == "gt":
            self.st.push(1 if x > y else 0)
        elif log_comm == "lt":
            self.st.push(1 if x < y else 0)
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
        to_neg = self.st.pop()
        self.st.push(to_neg * -1)
        res = "@SP\n" + "A=M-1\n" + "M=-M"
        return res

    def handle_arithmetic(self, type_command: str) -> str:
        y = self.st.pop()
        x = self.st.pop()
        if type_command == "add":
            self.st.push(x + y)
            return arithmetic_op("+")
        elif type_command == "sub":
            self.st.push(x - y)
            return arithmetic_op("-")
        else:
            raise ValueError("Some error in handle_arithm method")

    def handle_push(self, statement: List[str]) -> str:
        if statement[2].isnumeric():
            return self.save_value(statement[2])

    def save_value(self, val: str) -> str:
        res = "@" + val + "\n"  # save value at A register
        res += "D=A\n" + "@SP\n" + "A=M\n" + "M=D\n"  # write in RAM[SP] = val
        res += "@SP\n" + "M=M+1"  # sp++
        self.st.push(int(val))
        return res

    def handle_pop(self) -> str:
        res = "@SP\n" + "D=M\n" + "M=M-1"
        self.st.pop()
        return res
