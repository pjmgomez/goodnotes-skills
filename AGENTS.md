# goodnotes-skills — agent guide

A library of reusable **Agent Skills** in the [SKILL.md format](https://code.visualstudio.com/docs/copilot/customization/agent-skills). Markdown-only: no build, no test runner, no dependencies. Each skill is a self-contained folder that an agent discovers by its `description` and loads on demand.

## Where to look

- **This file** — quick, always-on orientation for working in the repo.
- [CONTRIBUTING.md](CONTRIBUTING.md) — the full authoring reference: the add process, the frontmatter table (including the `user-invocable` / `disable-model-invocation` matrix), the description-writing guide, a copy-paste `SKILL.md` template, and the two-tier validation.
- [README.md](README.md) — one-screen overview of the project, and the catalog table every skill needs a row in.
- [SECURITY.md](SECURITY.md) — the threat model a skill is written against.

Link to those rather than restating them here, so a fact never has two copies to drift apart.

The repo also ships its own customizations: `/new-skill` scaffolds a skill folder, `/validate-skill` runs the pre-PR gate, and [.github/instructions/](.github/instructions/) carries the authoring and Python rules automatically when you edit a matching file.

## Layout

```
skills/<skill-name>/
├── SKILL.md        # required; frontmatter name MUST equal <skill-name>
├── references/     # optional docs the skill loads only when needed
├── scripts/        # optional executable helpers
└── assets/         # optional templates/boilerplate the skill emits
tools/
└── validate_skill.py   # repo-level checker; run from the repository root
```

A new skill goes in its own `skills/<skill-name>/` folder. When adding one, mirror [skills/study-set-builder/](skills/study-set-builder/) — the worked example for every convention below — and add its row to the catalog table in [README.md](README.md), which nothing enforces.

There is deliberately no top-level `src/`, `test/`, or `docs/`. A generic repo-structure audit will report those as missing; that is expected here, not a gap to fill. `tools/` holds repo-level validation only — the skills themselves stay Markdown plus stdlib Python.

## SKILL.md shape

The body follows a predictable arc, visible in [study-set-builder's SKILL.md](skills/study-set-builder/SKILL.md): YAML frontmatter (`name` + `description`) → a short **When to use** list → the domain facts that matter → a numbered **Workflow** → writing tips → **Limits**. Reuse that skeleton instead of inventing one; the copy-paste template is in [CONTRIBUTING.md](CONTRIBUTING.md).

## Conventions that fail silently

These break discovery or loading with no error message, so get them right:

- **`name` equals the folder name** — lowercase, hyphens, 1–64 chars. A mismatch means the skill never loads.
- **`description` is the only trigger** — say what the skill does *and* when to use it ("Use when …"), in the words a user would actually type. A phrase absent from the description is a skill the agent can't find.
- **Keep `SKILL.md` under ~500 lines** — move depth into `references/` and link with `./` relative paths, kept one level deep.
- **Each skill is self-contained** — it carries every procedure it needs and never reaches into another skill's files.
- **Never steer an agent somewhere dangerous** — a bundled script reads and writes only the paths its docs name, and no `SKILL.md` instruction may lead to a destructive command or expose credentials. See [SECURITY.md](SECURITY.md).

## Scripts

Skills that need a helper keep it in `scripts/` and call it from the workflow as `python3 scripts/<name>.py …`.

- **Python 3, standard library only** — `argparse`, `csv`, `json`, `os`, `re`, `sys`. No third-party dependencies and nothing to install; keep it that way.
- **House style** — `from __future__ import annotations`, a module docstring reused as the argparse description, `_private` helpers, and `main()` behind an `if __name__ == "__main__"` guard. See [build_study_set.py](skills/study-set-builder/scripts/build_study_set.py), or the full rules in [skill-scripts.instructions.md](.github/instructions/skill-scripts.instructions.md).
- **Validators gate the work** — a checking script exits non-zero on any problem (so it can fail a build) and offers `--json` for a machine-readable report. See [validate_study_set.py](skills/study-set-builder/scripts/validate_study_set.py).
- Feed structured input as JSON through `--input` or stdin rather than ad-hoc flags.

## References and assets

- `references/` holds the deep look-up detail that would otherwise bloat `SKILL.md`; cite it with `./references/…`, and give any reference over ~300 lines its own table of contents. Example: [goodnotes-format.md](skills/study-set-builder/references/goodnotes-format.md).
- `assets/` holds sample output or boilerplate the skill emits, e.g. [example.csv](skills/study-set-builder/assets/example.csv).

## Validating your work

Validation is two-tier.

1. **Mechanical** — run `python3 tools/validate_skill.py skills/<skill-name>` from the repository root (no argument checks every skill). It covers the name/folder match, description limits, unknown frontmatter keys, the line budget, `./` links resolving one level deep, self-containment, and stray secrets. [CI runs it](.github/workflows/validate-skills.yml) on every pull request touching `skills/` or `tools/`, so run it locally first.
2. **Judgment** — nothing automates this tier. Walk the checklist in [CONTRIBUTING.md](CONTRIBUTING.md), or use `/validate-skill <name>`: does the `description` cover the phrasings a user would actually type, are the Limits honest, is the bundled example real.

Also run any skill's own validator over its own output, e.g. `python3 scripts/validate_study_set.py study-set.csv`.

## Git

- **Conventional Commits** — `feat: …`, `fix: …`, `docs: …`, `chore: …`.
- **Branches** are `<prefix>/<kebab-topic>`, e.g. `copilot/commit-check`.
- **One skill, or one focused change, per pull request.** The PR body records the trigger phrases you actually tried and the validator output — see [the template](.github/PULL_REQUEST_TEMPLATE.md).
