"""Content-addressed hashing for mod payloads. BLAKE3 with a stable chunk size."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from blake3 import blake3

CHUNK_SIZE = 1 << 20  # 1 MiB — matches the reader used by the packer


@dataclass(frozen=True, slots=True)
class FileDigest:
    path: str
    size: int
    digest: str


def hash_file(path: Path, *, chunk_size: int = CHUNK_SIZE) -> FileDigest:
    """Stream-hash a file. Memory stays bounded at chunk_size regardless of file size."""
    hasher = blake3()
    total = 0
    with path.open("rb") as fh:
        while chunk := fh.read(chunk_size):
            hasher.update(chunk)
            total += len(chunk)
    return FileDigest(path=str(path), size=total, digest=hasher.hexdigest())


def hash_tree(root: Path) -> list[FileDigest]:
    """Hash every regular file under root, sorted by relative path for determinism."""
    digests: list[FileDigest] = []
    for entry in sorted(root.rglob("*")):
        if entry.is_file():
            rel = entry.relative_to(root).as_posix()
            fd = hash_file(entry)
            digests.append(FileDigest(path=rel, size=fd.size, digest=fd.digest))
    return digests