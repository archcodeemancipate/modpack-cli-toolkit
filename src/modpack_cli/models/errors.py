"""Typed exceptions so handlers can map them to exit codes."""

from __future__ import annotations


class ModpackError(Exception):
    """Base for all toolkit errors."""


class ManifestError(ModpackError):
    """Manifest missing, malformed, or failed schema validation."""


class PackError(ModpackError):
    """Packing failed (disk, permission, compression)."""


class SignatureError(ModpackError):
    """Signing or verification failed."""