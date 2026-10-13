"""Manifest model + TOML loader. Manifest is the source of truth for a package."""

from __future__ import annotations

import tomllib
from pathlib import Path

from pydantic import BaseModel, Field, field_validator


class ModEntry(BaseModel):
    """A single mod inside the pack."""

    name: str
    version: str
    source: str = Field(description="Relative path or URL to the mod payload.")
    load_order: int = Field(default=0, ge=0)
    required: bool = True
    tags: list[str] = Field(default_factory=list)

    @field_validator("name")
    @classmethod
    def _no_path_seps(cls, v: str) -> str:
        if any(sep in v for sep in ("/", "\\", "..")):
            raise ValueError(f"mod name must not contain path separators: {v!r}")
        return v


class PackManifest(BaseModel):
    """Root manifest for a modpack-cli-toolkit package."""

    schema_version: int = 1
    pack_name: str
    pack_version: str
    game: str
    game_version: str
    author: str
    license: str = "MIT"
    target_platform: str = "windows"
    compression: str = "zstd"
    mods: list[ModEntry] = Field(default_factory=list)
    include_globs: list[str] = Field(default_factory=lambda: ["**/*"])
    exclude_globs: list[str] = Field(default_factory=lambda: ["**/__pycache__/**", "**/.git/**"])

    @field_validator("compression")
    @classmethod
    def _known_compression(cls, v: str) -> str:
        allowed = {"zstd", "7z", "store"}
        if v not in allowed:
            raise ValueError(f"compression must be one of {sorted(allowed)}, got {v!r}")
        return v


def load_manifest(path: Path) -> PackManifest:
    """Parse a TOML manifest. Raises FileNotFoundError / ValueError on bad input."""
    if not path.is_file():
        raise FileNotFoundError(f"manifest not found: {path}")
    with path.open("rb") as fh:
        raw = tomllib.load(fh)
    return PackManifest.model_validate(raw)