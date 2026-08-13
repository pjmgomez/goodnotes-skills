# Contributing to goodnotes-skills

This repository is a library of reusable **Agent Skills** written in the [SKILL.md format](https://code.visualstudio.com/docs/copilot/customization/agent-skills). It is Markdown-only — no build step, package manager, or test runner. Contributing a skill means adding one well-formed folder under `skills/`.

For the always-on summary agents use, see [AGENTS.md](AGENTS.md). This guide is the full reference.

## Add a skill in five steps

1. Create `skills/<skill-name>/SKILL.md` (see the [template](#skillmd-template) below), or run `/new-skill`.
2. Write the frontmatter — `name` **must** equal `<skill-name>`.
3. Write a trigger-rich `description` (see [Writing the description](#writing-the-description)).
4. Add the skill's row to the catalog table in [README.md](README.md).
5. Run the [validation](#validation) below before you open a PR.

## Folder layout

Each skill is a self-contained folder. Only `SKILL.md` is required; add the optional subfolders only when the skill needs them.

```
skills/<skill-name>/
├── SKILL.md        # required — the skill itself
├── references/     # docs the skill points to and loads on demand
├── scripts/        # executable helpers the skill runs
└── assets/         # templates/boilerplate the skill emits into output
```

Reference bundled files from `SKILL.md` with `./` relative paths, one level deep — e.g. `[the rules](./references/rules.md)`.

Repo-level tooling lives in `tools/`, outside any skill.

### Naming

- `<skill-name>` and the frontmatter `name` are identical.
- Lowercase alphanumeric and hyphens only, 1–64 characters (e.g. `study-set-import`, `smart-learn-quiz`).
- Name by the job the skill does, not the tool it uses — `pdf-to-study-set`, not `pdf-helper`.

## Frontmatter reference

```yaml
---
name: skill-name                 # required; must equal the folder name
description: 'What it does and when to use it.'   # required; <=1024 chars
argument-hint: '<topic>'         # optional; hint shown for slash invocation
user-invocable: true             # optional; default true — show as /slash command
disable-model-invocation: false  # optional; default false — allow auto-loading
---
```

`user-invocable` and `disable-model-invocation` decide how a skill is reached:

| `user-invocable` | `disable-model-invocation` | `/` slash command | Auto-loaded by model |
|---|---|---|---|
| `true` (default) | `false` (default) | Yes | Yes |
| `false` | `false` | No | Yes |
| `true` | `true` | Yes | No |
| `false` | `true` | No | No |

Leave both at their defaults unless you have a reason — most skills should be both slash-invocable and auto-loadable.

## Writing the description

The `description` is the only thing an agent sees when deciding whether to load a skill. If a user's phrasing isn't in it, the skill won't fire. Make it do two jobs:

1. **What** the skill does.
2. **When** to use it — concrete trigger phrases, in the words a user would type. Lead with "Use when …".

**Weak:** `A helpful skill for study sets.`

**Strong:** `Convert lecture notes and PDFs into Goodnotes-style study sets. Use when the user mentions study sets, flashcards, spaced repetition, or wants to turn notes into reviewable cards.`

Keep it under 1024 characters. Prefer distinct triggers over synonyms of the same case.

## Keep SKILL.md lean

An agent loads the whole `SKILL.md` body when the skill fires, so protect it:

- Keep it under ~500 lines. If it grows past that, move depth into `references/` and point to it.
- Put step-by-step procedure in the body; put look-up detail (rules, schemas, long examples) in `references/`.
- Give any reference file over ~300 lines its own table of contents.

## SKILL.md template

```markdown
---
name: study-set-import
description: 'Turn notes and PDFs into Goodnotes-style study sets. Use when the user mentions study sets, flashcards, spaced repetition, or converting notes into review cards.'
---

# Study Set Import

## When to use
- The user wants notes or a PDF turned into a study set.
- The user mentions flashcards or spaced repetition.

## Steps
1. Identify the source material and confirm the target study-set format.
2. Extract question/answer pairs.
3. Emit the study set using [the card template](./assets/card-template.md).

## Notes
- Detail that would bloat this file lives in [references/](./references/).
```

## Validation

Validation is two-tier. Run through this before opening a PR.

### Checked by the validator

From the repository root — no argument checks every skill:

```
python3 tools/validate_skill.py skills/<skill-name>
```

CI runs the same command on every pull request that touches `skills/` or `tools/`, so run it locally
first. It exits non-zero on any of these, and takes `--json` for a machine-readable report:

- The folder is `skills/<skill-name>/` and contains `SKILL.md`.
- Frontmatter `name` exactly equals `<skill-name>`, lowercase, hyphens only, 1–64 chars.
- Frontmatter parses, and carries no keys outside the table above.
- `description` is present and <=1024 chars, with no `<angle-bracket>` placeholders — they are stripped as markup.
- `SKILL.md` is under 500 lines; references over 300 lines have a table of contents.
- Every `./`-relative link resolves, and bundled files sit one level deep.
- No link escapes the skill folder, and no secrets are bundled.

### Checked by you

The judgment calls a script can't make, and that CI will never catch. `/validate-skill <skill-name>` walks these with you.

- [ ] The `description` names the phrasings a user would actually type — write down five and check each one.
- [ ] The body follows the arc: When to use → domain facts → numbered Workflow → tips → Limits.
- [ ] The Limits are honest about what the skill can't do.
- [ ] The bundled example is real, and would pass the skill's own validator.
- [ ] Nothing in the skill could steer an agent into a destructive command ([SECURITY.md](SECURITY.md)).
- [ ] The skill has its row in the [README.md](README.md) catalog table.

## Pull requests

- One skill (or one focused change) per PR.
- In the description, note what the skill does and the trigger phrases you expect to invoke it.
- Include the validator output, and confirm the judgment checks pass.
