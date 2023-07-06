from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List

from n2t.core.compiler.entities import Tokenizer


@dataclass
class JackCompiler:
    className: str

    @classmethod
    def create(cls, className: str) -> JackCompiler:
        return cls(className)

    def compile(self, stream: Iterable[str]) -> List[str]:
        tokenizer = Tokenizer(stream)
        xml_out: List[str] = ["<tokens>"]
        while tokenizer.has_more_tokens():
            tokenizer.advance()
            if not tokenizer.is_comment() and not tokenizer.is_empty():
                next = tokenizer.next_token()
                xml_out = xml_out + next
        xml_out.append("</tokens>")
        return xml_out
