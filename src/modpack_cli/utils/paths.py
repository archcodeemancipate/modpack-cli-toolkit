"""Path helpers with Windows-aware normalization."""

from __future__ import annotations

from pathlib import Path


def normalize_rel(path: str) -> str:
    """Force forward slashes and strip leading ./ for cross-platform manifests."""
    p = path.replace("\\", "/")
    while p.startswith("./"):
        p = p[2:]
    return p


def safe_join(root: Path, rel: str) -> Path:
    """Join root/rel and refuse anything that escapes root."""
    candidate = (root / normalize_rel(rel)).resolve()
    if root.resolve() not in candidate.parents and candidate != root.resolve():
        raise ValueError(f"path escapes root: {rel}")
    return candidate