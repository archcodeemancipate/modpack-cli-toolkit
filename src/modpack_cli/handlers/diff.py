"""`modpack diff` — compare two .mpk archives by content hash."""

from __future__ import annotations

from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

from modpack_cli.services.archive_reader import read_layout

_console = Console()


@click.command(name="diff")
@click.argument("left", type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.argument("right", type=click.Path(exists=True, dir_okay=False, path_type=Path))
def diff_cmd(left: Path, right: Path) -> None:
    """Show added / removed / changed files between LEFT and RIGHT."""
    a = {d.path: d.digest for d in read_layout(left).digests}
    b = {d.path: d.digest for d in read_layout(right).digests}
    table = Table(title=f"{left.name} -> {right.name}")
    table.add_column("status")
    table.add_column("path")
    for path in sorted(set(a) | set(b)):
        if path not in a:
            table.add_row("[green]+[/]", path)
        elif path not in b:
            table.add_row("[red]-[/]", path)
        elif a[path] != b[path]:
            table.add_row("[yellow]~[/]", path)
    _console.print(table)