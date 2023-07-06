from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterator, List

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
        if not self.path.is_dir():
            FileFormat.vm.validate(self.path)

    def translate(self) -> None:
        if self.path.is_dir():
            file_paths = self.path.glob("*.vm")
            saved_name = str(self.path) + "/sys"
            asm_code: List[str] = []
            asm_file = File(FileFormat.asm.convert(Path(saved_name)))
            for vm_path in file_paths:
                self.path = vm_path
                asm_code.extend(self.vm_translator.translate(self))
            if self.vm_translator.sys_enc and not self.vm_translator.bootstrap_added:
                boot = self.vm_translator.add_bootstrap()
                asm_code[0:0] = [boot]
                self.vm_translator.bootstrap_added = True
            asm_file.save(asm_code)
        else:
            asm_file = File(FileFormat.asm.convert(self.path))
            asm_file.save(self.vm_translator.translate(self))

    def __iter__(self) -> Iterator[str]:
        yield from File(self.path).load()


# class VMTranslator(Protocol):  # pragma: no cover
#     def translate(self, words: Iterable[str]) -> Iterable[str]:
#         pass
