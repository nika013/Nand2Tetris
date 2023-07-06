import re
from typing import Iterable, List, Tuple


class Variable:
    def __init__(self, name: str, type: str, kind: str) -> None:
        self.name = name
        self.type = type
        self.kind = kind

    def set_id(self, id: int) -> None:
        self.id = id

    def get_name(self) -> str:
        return self.name

    def get_kind(self) -> str:
        return self.kind

    def get_type(self) -> str:
        return self.type

    def get_id(self) -> int:
        return self.id

    def to_string(self) -> str:
        res = "name: " + self.name + " type: " + self.type
        res += " kind: " + self.kind + " #: " + str(self.id)
        return res


class Table:
    def __init__(self) -> None:
        self.variables: List[Variable] = []
        self.locals = 0
        self.fields = 0
        self.statics = 0
        self.arguments = 0
        self.total = 0
        self.next = None

    def add_variable(self, variable: Variable) -> None:
        kind = variable.get_kind()
        if kind == "field":
            variable.set_id(self.fields)
            self.fields += 1
            self.total += 1
        elif kind == "local":
            variable.set_id(self.locals)
            self.locals += 1
            self.total += 1
        elif kind == "argument":
            variable.set_id(self.arguments)
            self.arguments += 1
            self.total += 1
        elif kind == "static":
            variable.set_id(self.statics)
            self.statics += 1
            self.total += 1
        self.variables.append(variable)

    def find(self, var_name: str) -> Variable:
        for var in self.variables:
            if var.get_name() == var_name:
                return var


class Iterator:
    def __init__(self, tokens: List[str]) -> None:
        self.tokens = tokens
        self.length = len(self.tokens)
        self.i = 0
        self.cur_type = None

    @staticmethod
    def get_type(word: str) -> str:
        start_idx = word.index("<") + 1
        end_idx = word.index(">")
        return word[start_idx:end_idx]

    def has_next(self) -> bool:
        return self.i != self.length

    def peek(self) -> Tuple[str, str]:
        tag = self.tokens[self.i]
        content = Iterator.extract(self.tokens[self.i])
        return tag, content

    def next(self) -> str:
        if self.i != self.length:
            item = self.extract(self.tokens[self.i])
            self.i += 1
            return item
        return ""

    def get_attr(self) -> str:
        item = self.tokens[self.i]
        self.i += 1
        return item

    def get_whole(self) -> Tuple[str, str]:
        tag = self.tokens[self.i]
        content = Iterator.extract(self.tokens[self.i])
        self.i += 1
        return tag, content

    def skip(self) -> None:
        self.i += 1

    def prev(self) -> None:
        self.i -= 1

    @staticmethod
    def extract(word: str) -> str:
        start_idx = word.index(">") + 2
        end_idx = word.index("<", start_idx - 1) - 1
        content = word[start_idx:end_idx]
        return content


class Tokenizer:
    SYMBOLS_MAP = {"<": "&lt;", ">": "&gt;", "&": "&amp;"}

    SYMBOLS = {
        "{",
        "}",
        "(",
        ")",
        "[",
        "]",
        ".",
        ",",
        ";",
        "+",
        "+",
        "-",
        "*",
        "/",
        "&",
        "|",
        "<",
        ">",
        "=",
        "~",
    }

    KEYWORDS = {
        "class",
        "constructor",
        "function",
        "method",
        "field",
        "static",
        "var",
        "int",
        "char",
        "boolean",
        "void",
        "true",
        "false",
        "null",
        "this",
        "let",
        "do",
        "if",
        "else",
        "while",
        "return",
    }

    def __init__(self, stream: Iterable[str]) -> None:
        self.__cur_comm__ = ""
        self.stream = stream
        self.iter = iter(self.stream)

    def has_more_tokens(self) -> bool:
        self.__cur_comm__ = next(self.iter, "NO COMMAND")
        return self.__cur_comm__ != "NO COMMAND"

    def advance(self) -> None:
        curr = self.__cur_comm__.split("//", 1)[0]
        self.__cur_comm__ = curr.strip()

    def is_comment(self) -> bool:
        return (
            self.__cur_comm__.startswith("//")
            or self.__cur_comm__.startswith("*")
            or self.__cur_comm__.startswith("/**")
            or self.__cur_comm__.startswith("*/")
        )

    def is_empty(self) -> bool:
        return not self.__cur_comm__

    def tokenize_line(self) -> List[str]:
        tokens = re.split(r"(\W)", self.__cur_comm__)
        ans: List[str] = list()
        i = 0
        while i < len(tokens):
            if tokens[i] != '"':
                ans.append(tokens[i])
                i = i + 1
            else:
                ans.append(tokens[i])
                j = i + 1
                word = ""
                while tokens[j] != '"':
                    word = word + tokens[j]
                    j = j + 1
                ans.append(word)
                ans.append(tokens[j])
                i = j + 1
        return ans

    def next_token(self) -> List[str]:
        current_line = self.tokenize_line()
        return self.tokenize(current_line)

    def tokenize(self, line: Iterable[str]) -> List[str]:
        tokens = []
        inside_string = False
        current_word = ""

        for word in line:
            category = "identifier"

            if not word.strip():
                continue

            if word == '"':
                inside_string = not inside_string
                if not inside_string:
                    category = "stringConstant"
                    tokens.append(" ".join(self.modify(category, current_word)))
                    current_word = ""
                continue

            if inside_string:
                if not current_word:
                    current_word = word
                elif word not in self.SYMBOLS:
                    current_word += f" {word}"
                else:
                    current_word += word
                continue

            if word in self.KEYWORDS:
                category = "keyword"
            elif word in self.SYMBOLS:
                category = "symbol"
                if word in self.SYMBOLS_MAP:
                    word = self.SYMBOLS_MAP[word]
            elif word.isdigit():
                category = "integerConstant"
            tokens.append(" ".join(self.modify(category, word)))
        return tokens

    def modify(self, category: str, word: str) -> List[str]:
        res: List[str] = []
        res.append(f"<{category}>")
        res.append(f"{word}")
        res.append(f"</{category}>")
        return res
