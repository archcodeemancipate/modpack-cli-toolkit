"""`modpack sign` — attach a detached signature to an existing .mpk."""

from __future__ import annotations

from pathlib import Path

import click
from rich.console import Console

from modpack_cli.services.signing import sign_archive, verify_signature

_console = Console()


@click.command(name="sign")
@click.argument("archive", type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.option("--verify", is_flag=True, help="Verify an existing signature instead of creating one.")
def sign_cmd(archive: Path, verify: bool) -> None:
    """Sign or verify ARCHIVE."""
    if verify:
        ok = verify_signature(archive)
        _console.print(f"[{'green' if ok else 'red'}]{'valid' if ok else 'invalid'}[/] signature for {archive}")
        raise SystemExit(0 if ok else 2)
    sig_path = sign_archive(archive)
    _console.print(f"[green]wrote[/] {sig_path}")