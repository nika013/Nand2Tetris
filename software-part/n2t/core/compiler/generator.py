from dataclasses import dataclass
from typing import List

from n2t.core.compiler.entities import Iterator, Table, Variable


@dataclass
class CodeGenerator:
    xml: List[str]
    CLASS_VARIABLE = "classVarDec"
    LOCAL_VARIABLE = "varDec"
    LOCAL_VARIABLE_END = "/varDec"
    ARGUMENT = "parameterList"
    ARGUMENT_END = "/parameterList"
    SUBROUTINE = "subroutineDec"
    SUBROUTINE_END = "/subroutineDec"
    COMMA = ","
    SEMICOLON = "<symbol> ; </symbol>"
    SYMBOL = "symbol"
    EXPRESSION = "expression"
    EXPRESSION_END = "/expression"
    EXPRESSION_LIST_END = "/expressionList"
    CONSTRUCTOR = "constructor"
    METHOD = "method"
    STATEMENTS = "statements"
    STATEMENTS_END = "/statements"
    LET_STATEMENT = "letStatement"
    IF_STATEMENT = "ifStatement"
    IF_STATEMENT_END = "/ifStatement"
    WHILE_STATEMENT = "whileStatement"
    DO_STATEMENT = "doStatement"
    RET_STATEMENT = "returnStatement"
    TERM = "term"
    TERM_END = "/term"
    INTCONS = "integerConstant"
    STRCONS = "stringConstant"
    LEFT_PARENTHESIS = "("
    RIGHT_PARENTHESIS = ")"
    FUNCTION = "function"
    PRIMITIVES = {"int", "boolean", "char"}
    IDENTIFIER = "identifier"
    operators = {
        "-": "sub",
        "+": "add",
        "*": "call Math.multiply 2",
        "/": "call Math.divide 2",
        "=": "eq",
        "&gt;": "gt",
        "&lt;": "lt",
        "&amp;": "and",
        "|": "or",
    }

    unary_ops = {"~": "not", "-": "neg"}
    CONSTANTS = {"this", "true", "false", "null"}

    @classmethod
    def create(cls, xml: List[str]):
        return cls(xml)

    def compile(self) -> List[str]:
        vm_code: List[str] = []
        self.create_symbols_table()
        self.generate_vm(vm_code)
        return vm_code

    def is_var(self, sub_table: Table, content: str) -> bool:
        bool_1 = sub_table.find(content) is not None
        bool_2 = self.class_table.find(content) is not None
        return bool_1 or bool_2

    def generate_vm(self, vm_code: List[str]) -> None:
        iterator: Iterator = Iterator(self.xml)
        self.count_if = 0
        self.count_while = 0
        while iterator.has_next():
            tag = iterator.get_attr()
            type = Iterator.get_type(tag)
            if type == self.SUBROUTINE:
                self.generate_subroutine(iterator, vm_code)

    def generate_subroutine(self, iterator: Iterator, vm_code: List[str]) -> None:
        routine_type = iterator.next()  # get type of routine
        iterator.skip()  # skip return type
        routine_name = iterator.next()  # name of the routine
        func_name = self.class_name + "." + routine_name
        sub_table = self.sub_tables[func_name]
        self.cur_routine_name = func_name
        vm_code.append("function " + func_name + " " + str(sub_table.locals))

        if routine_type == self.CONSTRUCTOR:
            self.start_constructor(vm_code, self.class_table.fields)
        elif routine_type == self.METHOD:
            self.start_method(vm_code)

        tag = iterator.get_attr()
        tag_type = Iterator.get_type(tag)
        while tag_type != self.STATEMENTS:
            tag_type = Iterator.get_type(iterator.get_attr())

        self.compile_statements(sub_table, iterator, vm_code)

    def compile_statements(
        self, sub_table: Table, iterator: Iterator, vm_code: List[str]
    ) -> None:
        tag = iterator.get_attr()
        tag_type = Iterator.get_type(tag)  # get first type of statement
        while tag_type != self.STATEMENTS_END:
            if tag_type == self.LET_STATEMENT:
                self.compile_let(sub_table, iterator, vm_code)
            elif tag_type == self.IF_STATEMENT:
                self.compile_if(sub_table, iterator, vm_code)
            elif tag_type == self.WHILE_STATEMENT:
                self.compile_while(sub_table, iterator, vm_code)
            elif tag_type == self.DO_STATEMENT:
                self.compile_do(sub_table, iterator, vm_code)
            elif tag_type == self.RET_STATEMENT:
                self.compile_return(sub_table, iterator, vm_code)
            tag = iterator.get_attr()
            tag_type = Iterator.get_type(tag)  # get first type of statement

    def compile_let(
        self, sub_table: Table, iterator: Iterator, vm_code: List[str]
    ) -> None:
        iterator.skip()  # skip let keyword
        var_name = iterator.next()
        # lookup in the table
        equal_or_arr = iterator.next()  # skip the equal sign
        if equal_or_arr == "=":
            iterator.skip()  # skip expression tag
            self.compile_expression(sub_table, iterator, vm_code)
            var: Variable = sub_table.find(var_name)
            var = var if var is not None else self.class_table.find(var_name)
            kind = var.get_kind()
            kind = "this" if kind == "field" else kind
            pop_comm = "pop " + kind + " " + str(var.get_id())
            vm_code.append(pop_comm)
        else:
            var = sub_table.find(var_name)
            var = var if var is not None else self.class_table.find(var_name)
            kind = var.get_kind()
            kind = "that" if kind == "field" else kind
            vm_code.append("push " + kind + " " + str(var.get_id()))
            iterator.skip()  # skip expression tag
            self.compile_expression(sub_table, iterator, vm_code)
            vm_code.append("add")
            iterator.skip()  # skip ] symbol
            iterator.skip()  # skip = symbol
            iterator.skip()  # skip expression symb
            self.compile_expression(sub_table, iterator, vm_code)
            vm_code.append("pop temp 0")
            vm_code.append("pop pointer 1")
            vm_code.append("push temp 0")
            vm_code.append("pop that 0")

    def compile_if(
        self, sub_table: Table, iterator: Iterator, vm_code: List[str]
    ) -> None:
        iterator.skip()  # skip if keyword
        iterator.skip()  # skip ( symbol
        iterator.skip()  # skip expression tag
        self.compile_expression(sub_table, iterator, vm_code)
        vm_code.append("not")

        label = self.cur_routine_name + "_if_" + str(self.count_if)
        label_one = label + "1"
        label_two = label + "2"
        vm_code.append("if-goto " + label_one)
        iterator.skip()  # skip ) symbol
        iterator.skip()  # skip } symbol
        iterator.skip()  # skip statements tag
        self.compile_statements(sub_table, iterator, vm_code)
        vm_code.append("goto " + label_two)
        vm_code.append("label " + label_one)

        # generate else statements if it is
        iterator.skip()  # skip } symbol
        tag = iterator.get_attr()
        tag_type = Iterator.get_type(tag)
        # if so then there is else
        if tag_type != self.IF_STATEMENT_END:
            iterator.skip()  # skip { symbol
            iterator.skip()  # skip statements tag
            self.compile_statements(sub_table, iterator, vm_code)
            iterator.skip()  # skip } symbol
            iterator.skip()  # skip end tag of ifStatement

        vm_code.append("label " + label_two)
        self.count_if += 1

    def compile_while(
        self, sub_table: Table, iterator: Iterator, vm_code: List[str]
    ) -> None:
        iterator.skip()  # skip while keyword
        iterator.skip()  # skip ( symbol
        iterator.skip()  # skip expression keyword
        label = self.cur_routine_name + "_while_" + str(self.count_while)
        label_one = label + "1"
        label_two = label + "2"
        vm_code.append("label " + label_one)
        self.compile_expression(sub_table, iterator, vm_code)
        vm_code.append("not")
        vm_code.append("if-goto " + label_two)
        # here should be statements
        iterator.skip()  # skip ) symbol
        iterator.skip()  # skip { symbol
        iterator.skip()  # skip statements symbol
        self.compile_statements(sub_table, iterator, vm_code)
        vm_code.append("goto " + label_one)
        vm_code.append("label " + label_two)
        iterator.skip()  # skip } symbol
        iterator.skip()  # skip whileStatement end tag

    def compile_do(
        self, sub_table: Table, iterator: Iterator, vm_code: List[str]
    ) -> None:
        iterator.skip()  # skip do keyword
        to_call = iterator.next()
        params = 0
        if self.is_var(sub_table, to_call):
            var: Variable = sub_table.find(to_call)
            var = var if var is not None else self.class_table.find(to_call)
            to_call = var.get_type()
            kind = var.get_kind()
            kind = "this" if kind == "field" else kind
            vm_code.append("push " + kind + " " + str(var.get_id()))
            params += 1
        symb = iterator.next()
        if symb != self.LEFT_PARENTHESIS:
            to_call += symb + iterator.next()
            iterator.skip()  # skip left parenthesis
        else:
            vm_code.append("push pointer 0")
            to_call = self.class_name + "." + to_call
            params += 1
        tag = iterator.get_attr()  # expressionList tag
        tag_type = Iterator.get_type(tag)
        while tag_type != self.EXPRESSION_LIST_END:
            if tag_type == self.EXPRESSION:
                self.compile_expression(sub_table, iterator, vm_code)
                params += 1
            tag = iterator.get_attr()  # expressionList tag
            tag_type = Iterator.get_type(tag)
        vm_code.append("call " + to_call + " " + str(params))
        vm_code.append("pop temp 0")

    def compile_return(
        self, sub_table: Table, iterator: Iterator, vm_code: List[str]
    ) -> None:
        iterator.skip()  # skip return keyword
        tag = iterator.get_attr()
        tag_type = Iterator.get_type(tag)
        if tag_type == self.EXPRESSION:
            self.compile_expression(sub_table, iterator, vm_code)
        else:
            vm_code.append("push constant 0")
        iterator.skip()  # skip the end tag of return statement
        vm_code.append("return")

    def compile_expression(
        self, sub_table: Table, iterator: Iterator, vm_code: List[str]
    ) -> None:
        tag = iterator.get_attr()
        tag_type = Iterator.get_type(tag)  # get term tag
        while tag_type != self.EXPRESSION_END:
            if tag_type == self.TERM:
                self.compile_term(
                    sub_table, iterator, vm_code
                )  # should end on closing term tag
            next_tag = iterator.get_attr()
            tag_type = Iterator.get_type(next_tag)
            if tag_type == self.EXPRESSION_END:
                break
            if tag_type == self.SYMBOL:
                operator = Iterator.extract(next_tag)
                iterator.skip()  # skip term tag and compile term
                self.compile_term(sub_table, iterator, vm_code)
                vm_code.append(self.operators[operator])
                tag_type = Iterator.get_type(iterator.get_attr())  # get term tag

    def compile_term(
        self, sub_table: Table, iterator: Iterator, vm_code: List[str]
    ) -> None:
        tag = iterator.get_attr()
        tag_type = Iterator.get_type(tag)
        content = Iterator.extract(tag)
        # should go to end tag of the term
        if tag_type == self.INTCONS:
            vm_code.append("push constant " + content)
        elif tag_type == self.STRCONS:
            self.compile_string(iterator, vm_code, content)
        elif tag_type == self.IDENTIFIER and self.is_var(sub_table, content):
            var: Variable = sub_table.find(content)
            var = var if var is not None else self.class_table.find(content)
            var_type = var.get_type()
            next_tag = iterator.get_attr()
            term_type = Iterator.get_type(next_tag)
            iterator.prev()
            if var_type == "Array" and term_type != self.TERM_END:
                iterator.skip()  # skip [ symbol
                iterator.skip()  # skip expression tag
                kind = var.get_kind()
                kind = "this" if kind == "field" else kind
                command = "push " + kind + " " + str(var.get_id())
                vm_code.append(command)
                self.compile_expression(sub_table, iterator, vm_code)
                vm_code.append("add")
                vm_code.append("pop pointer 1")
                vm_code.append("push that 0")
            else:
                kind = var.get_kind()
                kind = "this" if kind == "field" else kind
                command = "push " + kind + " " + str(var.get_id())
                vm_code.append(command)
                if var_type not in self.PRIMITIVES:
                    self.compile_function(sub_table, iterator, vm_code, tag)
        elif tag_type == self.SYMBOL and content != self.LEFT_PARENTHESIS:  # unaryOp
            iterator.skip()  # skip the term tag
            self.compile_term(sub_table, iterator, vm_code)
            vm_code.append(self.unary_ops[content])  # outupt op
        elif tag_type == self.SYMBOL and content == self.LEFT_PARENTHESIS:
            iterator.skip()  # skip expression tag
            self.compile_expression(sub_table, iterator, vm_code)
            iterator.skip()  # skip right parenthesis
        elif content in self.CONSTANTS:
            self.compile_constants(content, vm_code)
        elif tag_type == self.IDENTIFIER:
            self.compile_function(sub_table, iterator, vm_code, tag)
        iterator.skip()  # skip the end tag of the term
        # handle functions and calls

    def compile_string(
        self, iterator: Iterator, vm_code: List[str], content: str
    ) -> None:
        length = len(content)
        vm_code.append("push constant " + str(length))
        vm_code.append("call String.new 1")
        for letter in content:
            vm_code.append("push constant " + str(ord(letter)))
            vm_code.append("call String.appendChar 2")

    def compile_function(
        self, sub_table: Table, iterator: Iterator, vm_code: List[str], tag: str
    ) -> None:
        call_name = Iterator.extract(tag)
        dot_tag = iterator.get_attr()
        dot_type = Iterator.get_type(dot_tag)
        if dot_type == self.TERM_END:
            iterator.prev()
            return
        call_name += Iterator.extract(dot_tag)  # add . symbol
        func_name = iterator.next()
        call_name += func_name
        iterator.skip()  # skip ( symbol
        tag = iterator.get_attr()  # expressionList tag
        tag_type = Iterator.get_type(tag)
        params = 0
        while tag_type != self.EXPRESSION_LIST_END:
            if tag_type == self.EXPRESSION:
                self.compile_expression(sub_table, iterator, vm_code)
                params += 1
            tag = iterator.get_attr()  # expressionList tag
            tag_type = Iterator.get_type(tag)
        vm_code.append("call " + call_name + " " + str(params))

    def compile_constants(self, content: str, vm_code: List[str]) -> None:
        if content == "true":
            vm_code.append("push constant 1")
            vm_code.append("neg")
        elif content == "false" or content == "null":
            vm_code.append("push constant 0")
        elif content == "this":
            vm_code.append("push pointer 0")

    def start_constructor(self, vm_code: List[str], fields: int) -> None:
        vm_code.append("push constant " + str(fields))
        vm_code.append("call Memory.alloc 1")
        vm_code.append("pop pointer 0")

    def start_method(self, vm_code: List[str]) -> None:
        vm_code.append("push argument 0")  # get 0 index arg which is object
        vm_code.append("pop pointer 0")  # write it to this segment

    def create_symbols_table(self) -> None:
        iterator: Iterator = Iterator(self.xml)
        self.class_table: Table = Table()
        self.sub_tables: dict[str, Table] = {}
        iterator.skip()  # skip class tag
        iterator.skip()  # skip keyword tag
        self.class_name: str = iterator.next()
        tag = iterator.get_attr()
        while iterator.has_next():
            type = Iterator.get_type(tag)
            if type == self.CLASS_VARIABLE:
                self.generate_class_table(self.class_table, iterator)
            elif type == self.SUBROUTINE:
                sub_type = iterator.next()  # skip type of subroutine
                iterator.skip()  # skip return type
                routine_name = iterator.next()  # get name of the routine
                sub_table = self.generate_sub_table(iterator, sub_type)
                key = self.class_name + "." + routine_name
                self.sub_tables[key] = sub_table
            tag = iterator.get_attr()

    def generate_class_table(self, class_table: Table, iterator: Iterator) -> None:
        kind: str = iterator.next()
        type: str = iterator.next()
        name: str = iterator.next()
        variable: Variable = Variable(name, type, kind)
        class_table.add_variable(variable)
        tag = iterator.get_attr()
        cur_type = Iterator.get_type(tag)
        if cur_type == self.SYMBOL:
            content = Iterator.extract(tag)
        while content == self.COMMA:
            name = iterator.next()
            variable = Variable(name, type, kind)
            class_table.add_variable(variable)
            tag = iterator.get_attr()
            cur_type = Iterator.get_type(tag)
            if cur_type == self.SYMBOL:
                content = Iterator.extract(tag)

    def generate_sub_table(self, iterator: Iterator, sub_type: str) -> Table:
        sub_table = Table()
        if sub_type == "method":
            sub_table.add_variable(Variable("this", self.class_name, "argument"))
        tag = iterator.get_attr()
        type = Iterator.get_type(tag)
        while type != self.SUBROUTINE_END:
            if type == self.ARGUMENT:  # consider commas in arguments
                self.generate_args(sub_table, type, iterator)
            elif type == self.LOCAL_VARIABLE:
                self.generate_locals(sub_table, type, iterator)
            tag = iterator.get_attr()
            type = Iterator.get_type(tag)
        return sub_table

    def generate_args(
        self, sub_tabel: Table, cur_type: str, iterator: Iterator
    ) -> None:
        # tag = iterator.get_attr()
        # cur_type = Iterator.get_type(tag)
        while cur_type != self.ARGUMENT_END:
            next_tag = iterator.get_attr()
            tag_type = Iterator.get_type(next_tag)
            if tag_type == self.ARGUMENT_END:
                break
            var_type = Iterator.extract(next_tag)
            name = iterator.next()
            kind = "argument"
            var = Variable(name, var_type, kind)
            sub_tabel.add_variable(var)
            tag = iterator.get_attr()
            cur_type = Iterator.get_type(tag)

    def generate_locals(
        self, sub_tabel: Table, cur_type: str, iterator: Iterator
    ) -> None:
        iterator.skip()  # skip var keyword
        type = iterator.next()
        name = iterator.next()
        kind = "local"
        var = Variable(name, type, kind)
        sub_tabel.add_variable(var)
        tag = iterator.get_attr()
        content = Iterator.extract(tag)
        while content == self.COMMA:
            name = iterator.next()
            var = Variable(name, type, kind)
            sub_tabel.add_variable(var)
            tag, content = iterator.get_whole()  # get next symbol comma or semicolon
        # go iterator to the end of the varDec tag
        if content == self.SEMICOLON:
            iterator.skip()
