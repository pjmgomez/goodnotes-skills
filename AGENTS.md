# goodnotes-skills — agent guide

A library of reusable **Agent Skills** in the [SKILL.md format](https://code.visualstudio.com/docs/copilot/customization/agent-skills). Markdown-only: no build, no test runner, no dependencies. Each skill is a self-contained folder that an agent discovers by its `description` and loads on demand.

## Where to look

- **This file** — quick, always-on orientation for working in the repo.
- [CONTRIBUTING.md](CONTRIBUTING.md) — the full authoring reference: the four-step add process, the frontmatter table (including the `user-invocable` / `disable-model-invocation` matrix), the description-writing guide, a copy-paste `SKILL.md` template, and the validation checklist.
- [README.md](README.md) — one-screen overview of the project.

Link to those rather than restating them here, so a fact never has two copies to drift apart.

## Layout

```
skills/<skill-name>/
├── SKILL.md        # required; frontmatter name MUST equal <skill-name>
├── references/     # optional docs the skill loads only when needed
├── scripts/        # optional executable helpers
└── assets/         # optional templates/boilerplate the skill emits
```

A new skill goes in its own `skills/<skill-name>/` folder; there is no top-level tooling to run. When adding one, mirror [skills/study-set-builder/](skills/study-set-builder/) — the worked example for every convention below.

## SKILL.md shape

The body follows a predictable arc, visible in [study-set-builder's SKILL.md](skills/study-set-builder/SKILL.md): YAML frontmatter (`name` + `description`) → a short **When to use** list → the domain facts that matter → a numbered **Workflow** → writing tips → **Limits**. Reuse that skeleton instead of inventing one; the copy-paste template is in [CONTRIBUTING.md](CONTRIBUTING.md).

## Conventions that fail silently

These break discovery or loading with no error message, so get them right:

- **`name` equals the folder name** — lowercase, hyphens, 1–64 chars. A mismatch means the skill never loads.
- **`description` is the only trigger** — say what the skill does *and* when to use it ("Use when …"), in the words a user would actually type. A phrase absent from the description is a skill the agent can't find.
- **Keep `SKILL.md` under ~500 lines** — move depth into `references/` and link with `./` relative paths, kept one level deep.
- **Each skill is self-contained** — it carries every procedure it needs and never reaches into another skill's files.

## Scripts

Skills that need a helper keep it in `scripts/` and call it from the workflow as `python3 scripts/<name>.py …`.

- **Python 3, standard library only** — `argparse`, `csv`, `json`, `sys`. No third-party dependencies and nothing to install; keep it that way.
- **House style** — `from __future__ import annotations`, a module docstring, `_private` helpers, and `main()` behind an `if __name__ == "__main__"` guard. See [build_study_set.py](skills/study-set-builder/scripts/build_study_set.py).
- **Validators gate the work** — a checking script exits non-zero on any problem (so it can fail a build) and offers `--json` for a machine-readable report. See [validate_study_set.py](skills/study-set-builder/scripts/validate_study_set.py).
- Feed structured input as JSON through `--input` or stdin rather than ad-hoc flags.

## References and assets

- `references/` holds the deep look-up detail that would otherwise bloat `SKILL.md`; cite it with `./references/…`, and give any reference over ~300 lines its own table of contents. Example: [goodnotes-format.md](skills/study-set-builder/references/goodnotes-format.md).
- `assets/` holds sample output or boilerplate the skill emits, e.g. [example.csv](skills/study-set-builder/assets/example.csv).

## Validating your work

There is no CI — the validation checklist in [CONTRIBUTING.md](CONTRIBUTING.md) is the gate. Before finishing a skill change, walk that checklist, confirm every `./` link resolves, and run any bundled validator over its own output (e.g. `python3 scripts/validate_study_set.py study-set.csv`).
