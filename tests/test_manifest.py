"""Manifest parsing + validation tests."""

from __future__ import annotations

from pathlib import Path

import pytest

from modpack_cli.core.manifest import PackManifest, load_manifest


def test_load_minimal_manifest(tmp_path: Path) -> None:
    mf = tmp_path / "pack.toml"
    mf.write_text(
        'schema_version = 1\n'
        'pack_name = "demo"\n'
        'pack_version = "0.1.0"\n'
        'game = "Skyrim"\n'
        'game_version = "1.6"\n'
        'author = "sam"\n'
    )
    m = load_manifest(mf)
    assert m.pack_name == "demo"
    assert m.compression == "zstd"
    assert m.mods == []


def test_rejects_unknown_compression() -> None:
    with pytest.raises(ValueError):
        PackManifest(
            pack_name="x", pack_version="0", game="g", game_version="1",
            author="a", compression="lzma-ultra",
        )


def test_rejects_mod_name_with_path_sep() -> None:
    with pytest.raises(ValueError):
        PackManifest(
            pack_name="x", pack_version="0", game="g", game_version="1",
            author="a",
            mods=[{"name": "../evil", "version": "1", "source": "s"}],
        )