"""Serializable package header + layout containers."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from modpack_cli.core.hashing import FileDigest


@dataclass(frozen=True, slots=True)
class PackageHeader:
    pack_name: str
    pack_version: str
    game: str
    game_version: str
    file_count: int
    total_bytes: int

    def to_bytes(self) -> bytes:
        return json.dumps({
            "pack_name": self.pack_name,
            "pack_version": self.pack_version,
            "game": self.game,
            "game_version": self.game_version,
            "file_count": self.file_count,
            "total_bytes": self.total_bytes,
        }, separators=(",", ":")).encode()

    @classmethod
    def from_bytes(cls, raw: bytes) -> "PackageHeader":
        d = json.loads(raw.decode())
        return cls(**d)


@dataclass(frozen=True, slots=True)
class PackageLayout:
    header: PackageHeader
    digests: list[FileDigest]
    archive_path: Path