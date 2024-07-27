from typer import Typer, echo

from n2t.infra import AsmProgram, HackProgram

cli = Typer(
    name="Nand 2 Tetris Software",
    no_args_is_help=True,
    add_completion=False,
)


@cli.command("assemble", no_args_is_help=True)
def run_assembler(assembly_file: str) -> None:
    echo(f"Assembling {assembly_file}")
    AsmProgram.load_from(assembly_file).assemble()
    echo("Done!")


@cli.command("execute", no_args_is_help=True)
def run_simulator(hack_file: str, cycles: int = 10000) -> None:
    echo(f"Executing {hack_file} with {cycles} cycles")
    HackProgram.load_from(hack_file, cycles).execute()
    echo("Done!")
