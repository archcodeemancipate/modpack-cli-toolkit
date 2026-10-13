"""Stage a source tree into a clean directory honoring manifest include/exclude globs."""

from __future__ import annotations

import fnmatch
import logging
import shutil
from pathlib import Path

from modpack_cli.core.manifest import PackManifest

_LOG = logging.getLogger("modpack_cli.services.staging")


def _included(rel: str, manifest: PackManifest) -> bool:
    if any(fnmatch.fnmatch(rel, pat) for pat in manifest.exclude_globs):
        return False
    return any(fnmatch.fnmatch(rel, pat) for pat in manifest.include_globs)


def stage_tree(source_root: Path, staging: Path, manifest: PackManifest) -> Path:
    """Copy matching files from source_root into staging. Clears staging first."""
    if staging.exists():
        shutil.rmtree(staging)
    staging.mkdir(parents=True, exist_ok=True)
    copied = 0
    for src in sorted(source_root.rglob("*")):
        if not src.is_file():
            continue
        rel = src.relative_to(source_root).as_posix()
        if not _included(rel, manifest):
            continue
        dest = staging / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
        copied += 1
    _LOG.info("staged %d files into %s", copied, staging)
    return staging