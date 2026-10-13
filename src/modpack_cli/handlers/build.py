"""`modpack build` — stage a source tree, pack it, optionally sign."""

from __future__ import annotations

import logging
from pathlib import Path

import click
from rich.console import Console

from modpack_cli.bootstrap.context import CliContext
from modpack_cli.core.manifest import load_manifest
from modpack_cli.core.packer import Packer
from modpack_cli.services.staging import stage_tree

_LOG = logging.getLogger("modpack_cli.handlers.build")
_console = Console()


@click.command(name="build")
@click.argument("manifest", type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.option("--out", "-o", type=click.Path(path_type=Path), default=Path("out"), show_default=True)
@click.option("--sign/--no-sign", default=False, help="Sign the resulting .mpk with the local key.")
@click.pass_obj
def build_cmd(ctx: CliContext, manifest: Path, out: Path, sign: bool) -> None:
    """Build a .mpk from MANIFEST."""
    m = load_manifest(manifest)
    staging = ctx.resolved_workdir() / "staging" / m.pack_name
    stage_tree(source_root=manifest.parent, staging=staging, manifest=m)
    out_path = (ctx.resolved_workdir() / out / f"{m.pack_name}-{m.pack_version}.mpk").resolve()
    layout = Packer(m, staging, out_path).pack()
    _console.print(f"[green]built[/] {layout.archive_path} ({layout.header.file_count} files)")
    if sign:
        from modpack_cli.services.signing import sign_archive

        sig = sign_archive(layout.archive_path)
        _console.print(f"[green]signed[/] {sig}")