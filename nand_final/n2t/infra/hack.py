from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from n2t.core import Assembler, HackSimulator
from n2t.infra.io import File, FileFormat


@dataclass
class HackProgram:
    path: Path
    cycles: int

    @classmethod
    def load_from(cls, file_name: str, cycles: int) -> HackProgram:
        return cls(Path(file_name), cycles)

    def execute(self) -> None:
        try:
            FileFormat.hack.validate(self.path)
            instructions: Iterable[str] = File(self.path).load()
        except AssertionError:
            FileFormat.asm.validate(self.path)
            assembly = File(self.path).load()
            instructions = Assembler.create().assemble(assembly)
        sim: HackSimulator = HackSimulator.create(instructions, self.cycles)
        json_file = File(FileFormat.json.convert(self.path))
        json_file.save(sim.execute())
