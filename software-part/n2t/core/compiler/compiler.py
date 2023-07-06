from __future__ import annotations

from dataclasses import dataclass
from typing import List

from n2t.core.compiler.entities import Iterator


@dataclass
class CompilationEngine:
    tokens: List[str]

    KEYWORD_CONSTANTS = {"true", "false", "null", "this"}

    STATEMENTS = {"let", "do", "if", "while", "return"}

    OP = {"+", "-", "*", "/", "&amp;", "|", "&lt;", "&gt;", "="}
    UNARY = ["-", "~"]
    TAB = "  "

    @classmethod
    def create(cls, tokens: List[str]) -> CompilationEngine:
        return cls(tokens)

    def compile(self) -> List[str]:
        self.iterator = Iterator(self.tokens)
        xml: List[str] = ["<class>"]
        xml += self.compile_class()
        xml.append("</class>")
        return xml

    def compile_class(self) -> List[str]:
        indents = 1
        xml: List[str] = list()
        self.iterator.skip()
        xml.append(indents * self.TAB + self.iterator.get_attr())
        xml.append(indents * self.TAB + self.iterator.get_attr())
        xml.append(indents * self.TAB + self.iterator.get_attr())
        tag, content = self.iterator.get_whole()
        while content == "static" or content == "field":
            xml += self.compile_class_var_dec(indents, tag)
            tag, content = self.iterator.get_whole()

        while content == "constructor" or content == "method" or content == "function":
            xml += self.compile_subroutine_dec(indents, tag)
            tag, content = self.iterator.get_whole()

        xml.append(indents * self.TAB + tag)
        return xml

    def compile_class_var_dec(self, indents: int, tag: str) -> List[str]:
        cur_xml: List[str] = [indents * self.TAB + "<classVarDec>"]
        cur_xml.append((indents + 1) * self.TAB + tag)
        tag, content = self.iterator.get_whole()
        while content != ";":
            cur_xml.append((indents + 1) * self.TAB + tag)
            tag, content = self.iterator.get_whole()
        cur_xml.append((indents + 1) * self.TAB + tag)
        cur_xml.append(indents * self.TAB + "</classVarDec>")
        return cur_xml

    def compile_subroutine_dec(self, indents: int, tag: str) -> List[str]:
        cur_xml: List[str] = [indents * self.TAB + "<subroutineDec>"]
        cur_xml.append(
            (indents + 1) * self.TAB + tag
        )  # constructor | method | function
        cur_xml.append((indents + 1) * self.TAB + self.iterator.get_attr())
        cur_xml.append((indents + 1) * self.TAB + self.iterator.get_attr())
        cur_xml.append((indents + 1) * self.TAB + self.iterator.get_attr())
        cur_xml += self.compile_parameter_list(
            indents + 1
        )  # add paramters and ) symbol
        cur_xml += self.compile_subroutine_body(indents + 1)
        cur_xml.append(indents * self.TAB + "</subroutineDec>")
        return cur_xml

    def compile_parameter_list(self, indents: int) -> List[str]:
        cur_xml: List[str] = [indents * self.TAB + "<parameterList>"]

        tag, content = self.iterator.get_whole()
        while content != ")":
            cur_xml.append((indents + 1) * self.TAB + tag)
            tag, content = self.iterator.get_whole()

        cur_xml.append(indents * self.TAB + "</parameterList>")
        cur_xml.append(indents * self.TAB + tag)
        return cur_xml

    def compile_subroutine_body(self, indents: int) -> List[str]:
        cur_xml: List[str] = [indents * self.TAB + "<subroutineBody>"]
        tag = self.iterator.get_attr()
        cur_xml.append((indents + 1) * self.TAB + tag)  # add { symbol

        # add variables
        tag, content = self.iterator.get_whole()
        while content == "var":
            cur_xml += self.compile_var_dec(indents + 1, tag)
            tag, content = self.iterator.get_whole()

        # compile statements
        cur_xml.append((indents + 1) * self.TAB + "<statements>")
        while content in self.STATEMENTS:
            cur_xml += self.compile_statements(indents + 1, tag, content)
            tag, content = self.iterator.get_whole()

        cur_xml.append((indents + 1) * self.TAB + "</statements>")

        cur_xml.append((indents + 1) * self.TAB + tag)
        cur_xml.append(indents * self.TAB + "</subroutineBody>")
        return cur_xml

    def compile_var_dec(self, indents: int, tag: str) -> List[str]:
        cur_xml: List[str] = [indents * self.TAB + "<varDec>"]
        cur_xml.append((indents + 1) * self.TAB + tag)

        tag, content = self.iterator.get_whole()
        while content != ";":
            cur_xml.append((indents + 1) * self.TAB + tag)
            tag, content = self.iterator.get_whole()

        cur_xml.append((indents + 1) * self.TAB + tag)
        cur_xml.append(indents * self.TAB + "</varDec>")
        return cur_xml

    def compile_statements(self, indents: int, tag: str, content: str) -> List[str]:
        cur_xml: List[str] = []
        if content == "let":
            cur_xml += self.compile_let(indents + 1, tag)
        elif content == "if":
            cur_xml += self.compile_if(indents + 1, tag)
        elif content == "while":
            cur_xml += self.compile_while(indents + 1, tag)
        elif content == "do":
            cur_xml += self.compile_do(indents + 1, tag)
        elif content == "return":
            cur_xml += self.compile_return(indents + 1, tag)
        return cur_xml

    def compile_let(self, indents: int, tag: str) -> List[str]:
        cur_xml: List[str] = [indents * self.TAB + "<letStatement>"]

        cur_xml.append((indents + 1) * self.TAB + tag)  # keyword let
        cur_xml.append(
            (indents + 1) * self.TAB + self.iterator.get_attr()
        )  # identifier
        tag, content = self.iterator.get_whole()
        if content == "[":
            cur_xml.append((indents + 1) * self.TAB + tag)  # symbol [
            cur_xml += self.compile_expression(indents + 1)
            cur_xml.append((indents + 1) * self.TAB + "<symbol> ] </symbol>")  # add ]
        if content == "=":
            cur_xml.append((indents + 1) * self.TAB + tag)  # add symbol =
        else:
            cur_xml.append(
                (indents + 1) * self.TAB + self.iterator.get_attr()
            )  # add symbol =
        cur_xml += self.compile_expression(indents + 1)
        tag, content = self.iterator.peek()
        if content == ";":
            self.iterator.skip()
        cur_xml.append(
            (indents + 1) * self.TAB + "<symbol> ; </symbol>"
        )  # add symbol ;
        cur_xml.append(indents * self.TAB + "</letStatement>")
        # print(self.iterator.get_whole(), self.iterator.get_whole())
        return cur_xml

    def compile_if(self, indents: int, tag: str) -> List[str]:
        cur_xml: List[str] = [indents * self.TAB + "<ifStatement>"]
        cur_xml.append((indents + 1) * self.TAB + tag)  # keyword if
        cur_xml.append((indents + 1) * self.TAB + self.iterator.get_attr())  # symbol (
        cur_xml += self.compile_expression(indents + 1)
        cur_xml.append((indents + 1) * self.TAB + "<symbol> ) </symbol>")
        cur_xml.append((indents + 1) * self.TAB + self.iterator.get_attr())  # symbol {
        tag, content = self.iterator.get_whole()

        cur_xml.append((indents + 1) * self.TAB + "<statements>")
        while content in self.STATEMENTS:
            cur_xml += self.compile_statements(indents + 1, tag, content)
            tag, content = self.iterator.get_whole()

        cur_xml.append((indents + 1) * self.TAB + "</statements>")
        cur_xml.append((indents + 1) * self.TAB + "<symbol> } </symbol>")  # symbol }
        tag, content = self.iterator.peek()
        if content == "else":
            self.iterator.skip()
            cur_xml.append((indents + 1) * self.TAB + tag)  # keyword else
            cur_xml.append(
                (indents + 1) * self.TAB + self.iterator.get_attr()
            )  # symbol {
            cur_xml.append((indents + 1) * self.TAB + "<statements>")
            tag, content = self.iterator.get_whole()
            while content in self.STATEMENTS:
                cur_xml += self.compile_statements(indents + 1, tag, content)
                tag, content = self.iterator.get_whole()

            cur_xml.append((indents + 1) * self.TAB + "</statements>")
            cur_xml.append(
                (indents + 1) * self.TAB + "<symbol> } </symbol>"
            )  # symbol }

        cur_xml.append(indents * self.TAB + "</ifStatement>")
        return cur_xml

    def compile_while(self, indents: int, tag: str) -> List[str]:
        cur_xml: List[str] = [indents * self.TAB + "<whileStatement>"]
        cur_xml.append((indents + 1) * self.TAB + tag)  # keyword while
        cur_xml.append((indents + 1) * self.TAB + self.iterator.get_attr())  # symbol (
        cur_xml += self.compile_expression(indents + 1)
        cur_xml.append((indents + 1) * self.TAB + "<symbol> ) </symbol>")
        cur_xml.append((indents + 1) * self.TAB + self.iterator.get_attr())  # symbol {
        tag, content = self.iterator.get_whole()
        cur_xml.append((indents + 1) * self.TAB + "<statements>")
        while content in self.STATEMENTS:
            cur_xml += self.compile_statements(indents + 1, tag, content)
            tag, content = self.iterator.get_whole()

        cur_xml.append((indents + 1) * self.TAB + "</statements>")
        cur_xml.append((indents + 1) * self.TAB + "<symbol> } </symbol>")  # symbol }

        cur_xml.append(indents * self.TAB + "</whileStatement>")
        return cur_xml

    def compile_do(self, indents: int, tag: str) -> List[str]:
        cur_xml: List[str] = [indents * self.TAB + "<doStatement>"]
        cur_xml.append((indents + 1) * self.TAB + tag)  # keyword do
        cur_xml.append(
            (indents + 1) * self.TAB + self.iterator.get_attr()
        )  # identifier
        tag, content = self.iterator.peek()
        if content == ".":
            self.iterator.skip()
            cur_xml.append((indents + 1) * self.TAB + tag)  # add .
            cur_xml.append(
                (indents + 1) * self.TAB + self.iterator.get_attr()
            )  # identifier
        cur_xml.append((indents + 1) * self.TAB + self.iterator.get_attr())  # add (
        cur_xml += self.compile_expression_list(indents + 1)
        # cur_xml.append((indents + 1) * self.TAB + "<symbol> ) </symbol>")  # add )
        tag, content = self.iterator.peek()
        if content == ")":
            self.iterator.skip()
        cur_xml.append((indents + 1) * self.TAB + self.iterator.get_attr())  # add ;

        cur_xml.append(indents * self.TAB + "</doStatement>")

        return cur_xml

    def compile_return(self, indents: int, tag: str) -> List[str]:
        cur_xml: List[str] = [indents * self.TAB + "<returnStatement>"]
        cur_xml.append((indents + 1) * self.TAB + tag)  # keyword return

        tag, content = self.iterator.peek()
        if content != ";":
            cur_xml += self.compile_expression(indents + 1)
        tag, content = self.iterator.peek()
        if content == ";":
            self.iterator.skip()
        cur_xml.append((indents + 1) * self.TAB + "<symbol> ; </symbol>")
        cur_xml.append(indents * self.TAB + "</returnStatement>")
        return cur_xml

    # leaves last character in this method f.i ; or ] should be added manually
    def compile_expression(self, indents: int) -> List[str]:
        cur_xml: List[str] = [indents * self.TAB + "<expression>"]
        expr = self.compile_term(indents + 1)
        cur_xml += expr
        tag, content = self.iterator.get_whole()
        if content in self.OP:
            cur_xml.append((indents + 1) * self.TAB + tag)
            cur_xml += self.compile_term(indents + 1)
            tag, content = self.iterator.get_whole()

        cur_xml.append(indents * self.TAB + "</expression>")
        return cur_xml

    # adds ) at the end
    def compile_expression_list(self, indents: int) -> List[str]:
        cur_xml: List[str] = [indents * self.TAB + "<expressionList>"]
        tag, content = self.iterator.peek()
        if content != ")":
            cur_xml += self.compile_expression(indents + 1)
            tag, content = self.iterator.peek()
            while content != ";":
                cur_xml.append((indents + 1) * self.TAB + "<symbol> , </symbol>")
                cur_xml += self.compile_expression(indents + 1)
                tag, content = self.iterator.peek()
                # print(content)

        cur_xml.append(indents * self.TAB + "</expressionList>")
        cur_xml.append(indents * self.TAB + "<symbol> ) </symbol>")
        return cur_xml

    def compile_term(self, indents: int) -> List[str]:
        cur_xml: List[str] = [indents * self.TAB + "<term>"]
        tag, content = self.iterator.get_whole()
        if self.get_type(tag) == "integerConstant":
            cur_xml.append((indents + 1) * self.TAB + tag)
        elif self.get_type(tag) == "stringConstant":
            cur_xml.append((indents + 1) * self.TAB + tag)
        elif content in self.KEYWORD_CONSTANTS:
            cur_xml.append((indents + 1) * self.TAB + tag)
        elif content in self.UNARY:
            cur_xml.append((indents + 1) * self.TAB + tag)
            cur_xml += self.compile_term(indents + 1)
        elif content == "(":
            cur_xml.append((indents + 1) * self.TAB + tag)
            cur_xml += self.compile_expression(indents + 1)
            cur_xml.append((indents + 1) * self.TAB + "<symbol> ) </symbol>")
        elif self.get_type(tag) == "identifier":
            cur_xml.append((indents + 1) * self.TAB + tag)
            tag, content = self.iterator.peek()
            if self.get_type(tag) == "symbol" and content == "[":
                self.iterator.skip()
                cur_xml.append((indents + 1) * self.TAB + tag)
                cur_xml += self.compile_expression(indents + 1)
                cur_xml.append((indents + 1) * self.TAB + "<symbol> ] </symbol>")
            elif self.get_type(tag) == "symbol" and content == "(":
                self.iterator.skip()
                cur_xml.append((indents + 1) * self.TAB + tag)
                cur_xml += self.compile_expression_list(indents + 1)
            elif self.get_type(tag) == "symbol" and content == ".":
                self.iterator.skip()
                cur_xml.append((indents + 1) * self.TAB + tag)
                # add method call
                cur_xml.append((indents + 1) * self.TAB + self.iterator.get_attr())
                # add ( symbol
                cur_xml.append((indents + 1) * self.TAB + self.iterator.get_attr())
                cur_xml += self.compile_expression_list(indents + 1)

        cur_xml.append(indents * self.TAB + "</term>")
        return cur_xml

    def get_type(self, tag: str) -> str:
        strIdx = tag.index("<") + 1
        endIdx = tag.index(">")
        return tag[strIdx:endIdx]
