"""Default values merged into new manifests via `modpack init`."""

from __future__ import annotations

DEFAULT_MANIFEST_TEMPLATE: str = """\
schema_version = 1
pack_name = "my-modpack"
pack_version = "0.1.0"
game = "Skyrim"
game_version = "1.6.1170"
author = "your-handle"
license = "MIT"
target_platform = "windows"
compression = "zstd"
include_globs = ["**/*"]
exclude_globs = ["**/__pycache__/**", "**/.git/**"]

[[mods]]
name = "ExampleMod"
version = "1.2.3"
source = "mods/ExampleMod"
load_order = 10
required = true
tags = ["gameplay"]
"""

DEFAULT_EXCLUDE_GLOBS: tuple[str, ...] = (
    "**/__pycache__/**",
    "**/.git/**",
    "**/*.pyc",
    "**/.DS_Store",
)