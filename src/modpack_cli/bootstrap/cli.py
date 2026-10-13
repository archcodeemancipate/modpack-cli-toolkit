"""Top-level Click group. Wires handlers to subcommands and owns process exit codes."""

from __future__ import annotations

import logging
import signal
import sys
from typing import NoReturn

import click

from modpack_cli import __version__
from modpack_cli.bootstrap.context import CliContext
from modpack_cli.handlers import build as build_handler
from modpack_cli.handlers import diff as diff_handler
from modpack_cli.handlers import inspect as inspect_handler
from modpack_cli.handlers import sign as sign_handler
from modpack_cli.services.logging_setup import configure_logging

_LOG = logging.getLogger("modpack_cli.bootstrap")


def _install_sigint_handler() -> None:
    def _handler(signum: int, _frame: object) -> NoReturn:
        _LOG.warning("interrupted (signal %s), aborting cleanly", signum)
        sys.exit(130)

    signal.signal(signal.SIGINT, _handler)


@click.group(name="modpack", context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option(__version__, prog_name="modpack-cli-toolkit")
@click.option("--verbose", "-v", count=True, help="Increase log verbosity (-vv for debug).")
@click.option("--quiet", "-q", is_flag=True, help="Suppress non-error output.")
@click.option(
    "--workdir",
    type=click.Path(file_okay=False),
    default=None,
    help="Override working directory for staging and cache.",
)
@click.pass_context
def main(ctx: click.Context, verbose: int, quiet: bool, workdir: str | None) -> None:
    """modpack-cli-toolkit — package, sign, and ship game mods."""
    configure_logging(verbosity=verbose, quiet=quiet)
    ctx.obj = CliContext(workdir=workdir, verbosity=verbose, quiet=quiet)
    _install_sigint_handler()


main.add_command(build_handler.build_cmd, name="build")
main.add_command(sign_handler.sign_cmd, name="sign")
main.add_command(diff_handler.diff_cmd, name="diff")
main.add_command(inspect_handler.inspect_cmd, name="inspect")


if __name__ == "__main__":
    main()