"""Read a .mpk header + digest table without decompressing the payload."""

from __future__ import annotations

import json
from pathlib import Path

from modpack_cli.core.hashing import FileDigest
from modpack_cli.models.package import PackageHeader, PackageLayout

_MAGIC = b"MPK1"
_HEADER_LEN = 512


def read_layout(archive: Path) -> PackageLayout:
    with archive.open("rb") as fh:
        magic = fh.read(4)
        if magic != _MAGIC:
            raise ValueError(f"not an .mpk archive: {archive}")
        raw_header = fh.read(_HEADER_LEN - 4).rstrip(b"\x00")
        header = PackageHeader.from_bytes(raw_header)
        digests: list[FileDigest] = []
        for line in fh.read().split(b"\n"):
            if not line.strip():
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                break
            digests.append(FileDigest(path=rec["path"], size=0, digest=rec["blake3"]))
    return PackageLayout(header=header, digests=digests, archive_path=archive)