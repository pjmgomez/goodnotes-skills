---
applyTo: "skills/**/*.md"
description: "Conventions for authoring a skill in skills/ — frontmatter rules, description triggers, file budget, and self-containment."
---

# Authoring a skill

Full reference: [CONTRIBUTING.md](../../CONTRIBUTING.md). These are the rules that fail silently.

## Frontmatter

- `name` **must** equal the folder name — lowercase, hyphens, 1–64 chars. A mismatch means the skill never loads.
- `description` is the only thing an agent matches on. Say **what** it does *and* **when** to use it, in the words a user would actually type. A phrase absent from the description is a skill nobody can find.
- Quote any description containing a colon, and keep angle brackets out of it — `<name>` is stripped as markup, silently mangling the trigger text. Allowed keys are only `name`, `description`, `argument-hint`, `user-invocable`, `disable-model-invocation`.

## Body

Follow the arc in [study-set-builder](../../skills/study-set-builder/SKILL.md): **When to use** → the domain facts that matter → a numbered **Workflow** → writing tips → **Limits**.

- Keep `SKILL.md` under 500 lines. Push look-up detail into `references/` and link it with `./`.
- Bundled files sit one level deep — `./references/x.md`, never `./references/sub/x.md`.
- A skill is self-contained: never link to `../` or another skill's files.
- A reference file states where its facts came from, and gets a `## Contents` heading past ~300 lines.
- Never write a step that steers an agent into a destructive command or exposes credentials — see [SECURITY.md](../../SECURITY.md).

## Before you finish

- Adding a skill also means adding its row to the catalog table in [README.md](../../README.md).
- Run `python3 tools/validate_skill.py skills/<skill-name>` from the repository root.
