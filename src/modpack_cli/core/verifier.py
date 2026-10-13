"""Verifier: re-hash a .mpk payload and compare against embedded digests."""

from __future__ import annotations

from dataclasses import dataclass

from modpack_cli.models.package import PackageLayout


@dataclass(frozen=True, slots=True)
class VerifyReport:
    ok: bool
    mismatches: list[str]
    missing: list[str]


def verify_layout(layout: PackageLayout, actual_digests: dict[str, str]) -> VerifyReport:
    """Compare expected digests (from layout) against actual_digests keyed by rel path."""
    mismatches: list[str] = []
    missing: list[str] = []
    for expected in layout.digests:
        got = actual_digests.get(expected.path)
        if got is None:
            missing.append(expected.path)
        elif got != expected.digest:
            mismatches.append(expected.path)
    return VerifyReport(ok=not mismatches and not missing, mismatches=mismatches, missing=missing)