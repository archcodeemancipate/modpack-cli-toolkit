"""`modpack inspect` — dump header + digest summary for a .mpk."""

from __future__ import annotations

from pathlib import Path

import click
from rich.console import Console
from rich.panel import Panel

from modpack_cli.services.archive_reader import read_layout

_console = Console()


@click.command(name="inspect")
@click.argument("archive", type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.option("--list-files", is_flag=True, help="Print every file digest.")
def inspect_cmd(archive: Path, list_files: bool) -> None:
    """Print metadata for ARCHIVE."""
    layout = read_layout(archive)
    h = layout.header
    _console.print(Panel.fit(
        f"[bold]{h.pack_name}[/] v{h.pack_version}\n"
        f"game: {h.game} ({h.game_version})\n"
        f"files: {h.file_count}  bytes: {h.total_bytes}",
        title=archive.name,
    ))
    if list_files:
        for d in layout.digests:
            _console.print(f"  {d.digest[:12]}  {d.size:>10}  {d.path}")