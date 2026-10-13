"""Detached Ed25519 signing for .mpk archives. Key material lives in ~/.config/modpack-cli-toolkit."""

from __future__ import annotations

import logging
from pathlib import Path

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)

_LOG = logging.getLogger("modpack_cli.services.signing")
_KEY_DIR = Path.home() / ".config" / "modpack-cli-toolkit"
_PRIV = _KEY_DIR / "signing.key"
_PUB = _KEY_DIR / "signing.pub"


def _load_or_create_key() -> Ed25519PrivateKey:
    if _PRIV.is_file():
        return Ed25519PrivateKey.from_private_bytes(_PRIV.read_bytes())
    _KEY_DIR.mkdir(parents=True, exist_ok=True)
    key = Ed25519PrivateKey.generate()
    _PRIV.write_bytes(key.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption(),
    ))
    _PUB.write_bytes(key.public_key().public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    ))
    _LOG.warning("generated new signing key at %s — back it up", _PRIV)
    return key


def sign_archive(archive: Path) -> Path:
    key = _load_or_create_key()
    sig = key.sign(archive.read_bytes())
    sig_path = archive.with_suffix(archive.suffix + ".sig")
    sig_path.write_bytes(sig)
    return sig_path


def verify_signature(archive: Path) -> bool:
    sig_path = archive.with_suffix(archive.suffix + ".sig")
    if not sig_path.is_file() or not _PUB.is_file():
        return False
    pub = Ed25519PublicKey.from_public_bytes(_PUB.read_bytes())
    try:
        pub.verify(sig_path.read_bytes(), archive.read_bytes())
    except Exception:
        return False
    return True