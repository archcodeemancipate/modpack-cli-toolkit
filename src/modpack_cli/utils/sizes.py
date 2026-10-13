"""Byte formatting for CLI output."""

from __future__ import annotations


def human_bytes(n: int) -> str:
    units = ["B", "KiB", "MiB", "GiB", "TiB"]
    f = float(n)
    for unit in units:
        if f < 1024 or unit == units[-1]:
            return f"{f:.1f} {unit}" if unit != "B" else f"{int(f)} B"
        f /= 1024
    return f"{n} B"