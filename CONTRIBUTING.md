# Contributing to modpack-cli-toolkit

Thanks for wanting to help. This repo is a Windows-focused Python CLI for
building, signing, diffing, and shipping game mod packages. It is used by
mod authors and pack maintainers who want a reproducible pipeline instead
of hand-zipping folders.

## Development setup

```powershell
git clone https://github.com/modpack-cli-toolkit/modpack-cli-toolkit
cd modpack-cli-toolkit
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev,signing]"
```

## Layout

```
src/modpack_cli/
  bootstrap/   entry point, Click group, process context
  core/        manifest, hashing, packer, verifier
  handlers/    one module per CLI subcommand
  services/    staging, signing, archive reading, logging
  models/      dataclasses + typed errors
  utils/       path + size helpers
  config/      defaults and templates
tests/         pytest suites (manifest, packer round-trip)
```

Keep the layering honest: handlers call services and core, never the
reverse. Core must not import Click or Rich.

## Style

- `ruff` for lint + format, `mypy --strict` for types.
- Line length 100. Type every public function.
- No `print()` in library code — use `logging` or `rich.console.Console`.

## Tests

```powershell
pytest
```

New behavior needs a test. Bug fixes need a regression test. The packer
round-trip test is the reference for anything touching the archive format.

## Commit messages

`<area>: <what>` — e.g. `packer: stream zstd writer to bound memory`,
`handlers/diff: sort output by path`.

## Manifest format changes

Any change to `PackManifest` or the `.mpk` header bumps `schema_version`
and needs a migration note in the PR description. Do not silently change
field semantics.

## Reporting issues

Include: OS build, Python version, `modpack --version`, the manifest, and
the full traceback with `-vv`. Reproducing packer bugs is much easier with
the offending archive attached.

## Code of conduct

Be decent. Modding communities live and die on shared knowledge. Credit
sources, don't leak private payloads, don't ship someone else's work as
your own.