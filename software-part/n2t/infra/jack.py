from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from n2t.core.compiler.compiler import CompilationEngine
from n2t.core.compiler.facade import JackCompiler
from n2t.core.compiler.generator import CodeGenerator
from n2t.infra.io import File


@dataclass
class JackProgram:
    filePath: str

    @classmethod
    def load_from(cls, file_or_directory_name: str) -> JackProgram:
        return cls(file_or_directory_name)

    def compile(self) -> None:
        path = Path(self.filePath)
        if not path.is_dir():
            self.compile_one(self.filePath)
        else:
            for file in list(path.glob("**/*.jack")):
                self.compile_one(file.as_posix())

    def compile_one(self, path: str) -> None:
        # create and save *T.cmp file
        stream: Iterable[str] = File(Path(path)).load()

        jack_compiler = JackCompiler(path)
        tokens = jack_compiler.compile(stream)
        # save_file = path[:-5] + "T.cmp"
        # File(Path(save_file)).save(tokens)
        # build complete version
        engine = CompilationEngine(tokens)
        xml = engine.compile()
        outputFilePath = path[:-5] + ".xml"
        File(Path(outputFilePath)).save(xml)
        generator = CodeGenerator(xml)
        vm_code = generator.compile()
        outputFilePath = path[:-5] + ".vm"
        File(Path(outputFilePath)).save(vm_code)
