import typer 
from typing import List
from pathlib import Path
from clumper import Clumper

def concat_jsonl(paths: List[Path] = typer.Argument(...), 
                 out: Path = typer.Argument(...), 
                 order: str = typer.Option("date")):
    Clumper.read_jsonl(paths).sort(lambda d: d[order]).write_csv(out)

if __name__ == "__main__":
    typer.run(concat_jsonl)
