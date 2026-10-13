"""Process-scoped context object passed through Click's ctx.obj."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(slots=True)
class CliContext:
    """Carries CLI-wide state: working dir, verbosity, cache location."""

    workdir: str | None = None
    verbosity: int = 0
    quiet: bool = False
    cache_dir: Path = field(default_factory=lambda: Path.home() / ".cache" / "modpack-cli-toolkit")

    def resolved_workdir(self) -> Path:
        return Path(self.workdir).resolve() if self.workdir else Path.cwd().resolve()

    def ensure_cache(self) -> Path:
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        return self.cache_dir