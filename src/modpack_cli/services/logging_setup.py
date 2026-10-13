"""Rich-aware logging config. Verbosity maps to level; quiet silences everything but errors."""

from __future__ import annotations

import logging


def configure_logging(verbosity: int, quiet: bool) -> None:
    level = logging.WARNING
    if quiet:
        level = logging.ERROR
    elif verbosity >= 2:
        level = logging.DEBUG
    elif verbosity == 1:
        level = logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)-7s %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )