"""Pack -> read -> verify round trip."""

from __future__ import annotations

from pathlib import Path

from modpack_cli.core.hashing import hash_tree
from modpack_cli.core.manifest import PackManifest
from modpack_cli.core.packer import Packer
from modpack_cli.core.verifier import verify_layout
from modpack_cli.services.archive_reader import read_layout


def _make_manifest() -> PackManifest:
    return PackManifest(
        pack_name="roundtrip", pack_version="0.0.1",
        game="Skyrim", game_version="1.6", author="sam",
    )


def test_pack_then_verify(tmp_path: Path) -> None:
    staging = tmp_path / "staging"
    staging.mkdir()
    (staging / "a.txt").write_text("alpha")
    (staging / "sub").mkdir()
    (staging / "sub" / "b.txt").write_text("bravo")

    out = tmp_path / "roundtrip.mpk"
    layout = Packer(_make_manifest(), staging, out).pack()
    assert out.is_file()
    assert layout.header.file_count == 2

    reread = read_layout(out)
    actual = {d.path: d.digest for d in hash_tree(staging)}
    report = verify_layout(reread, actual)
    assert report.ok, report