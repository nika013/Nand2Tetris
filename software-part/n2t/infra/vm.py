from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterator

from n2t.core import VMTranslator as DefaultVMTranslator
from n2t.infra.io import File, FileFormat


@dataclass
class VmProgram:  # TODO: your work for Projects 7 and 8 starts here
    path: Path
    vm_translator: DefaultVMTranslator = field(
        default_factory=DefaultVMTranslator.create
    )

    @classmethod
    def load_from(cls, file_or_directory_name: str) -> VmProgram:
        return cls(Path(file_or_directory_name))

    def __post_init__(self) -> None:
        FileFormat.vm.validate(self.path)

    def translate(self) -> None:
        asm_file = File(FileFormat.asm.convert(self.path))
        asm_file.save(self.vm_translator.translate(self))

    def __iter__(self) -> Iterator[str]:
        yield from File(self.path).load()


# class VMTranslator(Protocol):  # pragma: no cover
#     def translate(self, words: Iterable[str]) -> Iterable[str]:
#         pass
