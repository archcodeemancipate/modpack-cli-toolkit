"""Packer: assemble staging tree into a .mpk archive with a manifest sidecar."""

from __future__ import annotations

import json
import logging
from pathlib import Path

import zstandard as zstd

from modpack_cli.core.hashing import hash_tree
from modpack_cli.core.manifest import PackManifest
from modpack_cli.models.package import PackageHeader, PackageLayout

_LOG = logging.getLogger("modpack_cli.core.packer")
_MAGIC = b"MPK1"
_HEADER_LEN = 512


class Packer:
    """Writes a .mpk: [512-byte header][zstd-compressed tar payload]."""

    def __init__(self, manifest: PackManifest, staging: Path, out_path: Path) -> None:
        self._manifest = manifest
        self._staging = staging
        self._out = out_path
        self._level = 19 if manifest.compression == "zstd" else 0

    def pack(self) -> PackageLayout:
        digests = hash_tree(self._staging)
        header = PackageHeader(
            pack_name=self._manifest.pack_name,
            pack_version=self._manifest.pack_version,
            game=self._manifest.game,
            game_version=self._manifest.game_version,
            file_count=len(digests),
            total_bytes=sum(d.size for d in digests),
        )
        self._out.parent.mkdir(parents=True, exist_ok=True)
        cctx = zstd.ZstdCompressor(level=self._level) if self._level else None

        with self._out.open("wb") as out_fh:
            out_fh.write(_MAGIC)
            out_fh.write(header.to_bytes().ljust(_HEADER_LEN - len(_MAGIC), b"\x00"))
            with (cctx.stream_writer(out_fh) if cctx else out_fh) as sink:
                for digest in digests:
                    src = self._staging / digest.path
                    sink.write(json.dumps({"path": digest.path, "blake3": digest.digest}).encode())
                    sink.write(b"\n")
                    sink.write(src.read_bytes())

        _LOG.info("packed %d files -> %s (%d bytes)", len(digests), self._out, header.total_bytes)
        return PackageLayout(header=header, digests=digests, archive_path=self._out)