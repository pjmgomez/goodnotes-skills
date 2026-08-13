---
applyTo: "skills/**/scripts/*.py,tools/*.py"
description: "House style for the Python helpers bundled with skills and the repo-level tools — stdlib only, argparse shape, and the builder vs validator error contract."
---

# Python helpers

Every script here is Python 3 **standard library only** — `argparse`, `csv`, `json`, `os`, `re`, `sys`. No third-party imports, no `requirements.txt`, nothing to install. Match [validate_study_set.py](../../skills/study-set-builder/scripts/validate_study_set.py) and [build_study_set.py](../../skills/study-set-builder/scripts/build_study_set.py).

## Shape

- `#!/usr/bin/env python3`, then a module docstring: one-sentence summary, then *why* the rules exist, then input/flag notes. Reuse it as `description=__doc__` with `formatter_class=argparse.RawDescriptionHelpFormatter`.
- `from __future__ import annotations` immediately after the docstring. Module constants in SHOUT_CASE.
- No function docstrings and no type annotations — a single `#` comment states *why*, never *what*.
- `_private` helpers; keep the public surface to `main()` plus the one function worth importing.
- All argparse wiring inside `main()`, guarded by `if __name__ == "__main__": main()`.
- Lowercase argparse help, no trailing period. Double-quoted strings, f-strings for interpolation.

## Error contract

- **Builders fail fast**: `sys.exit(f"error: …")` on the first bad input — message to stderr, exit 1.
- **Validators never raise**: accumulate `problems: list[str]`, turn `FileNotFoundError` and `UnicodeDecodeError` into problem strings, print `PASS:`/`FAIL:` lines, and end with `sys.exit(0 if ok else 1)` so the script can gate a build. Offer `--json` for a machine-readable report; it does not suppress the non-zero exit.

## Boundaries

- Duplicating a small helper across scripts is fine — self-containment beats DRY here.
- A script reads and writes only the paths its docstring documents. Anything wider is a security issue, not a feature ([SECURITY.md](../../SECURITY.md)).
- Skill scripts are invoked as `python3 scripts/<name>.py`, relative to the skill folder; repo-level tools run from the repository root.
