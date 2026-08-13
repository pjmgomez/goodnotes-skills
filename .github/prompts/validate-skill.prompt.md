---
mode: agent
description: "Check a skill folder before opening a pull request — run tools/validate_skill.py for the mechanical rules, then the judgment checks a script can't make."
argument-hint: 'the skill name'
---

# Validate a skill

Validate the skill named in the prompt argument (default: every folder under `skills/`).
CI runs the mechanical validator on every pull request touching `skills/` or `tools/`, so this
is the pre-PR gate: run that same script locally first, then make the judgment calls CI cannot.
The checklist itself lives in [CONTRIBUTING.md](../../CONTRIBUTING.md).

## 1. Mechanical rules — run the script

From the repository root:

```
python3 tools/validate_skill.py skills/<skill-name>
```

It covers `name` vs folder name, the description length, unknown frontmatter keys, the
500-line budget, `./` links resolving one level deep, self-containment, and stray secrets.
Report its output verbatim. If it exits non-zero, fix the problems and re-run before going on.

## 2. Judgment rules — check these yourself

The script cannot judge any of these. Read `SKILL.md` and decide:

- **Trigger coverage.** Write down at least five phrasings a user would plausibly type to
  reach this skill. Check each one against the `description` and name the ones it would miss.
  This is the single most common reason a skill never fires.
- **Description shape.** Does it say both *what* the skill does and *when* to use it, in a
  user's words rather than the author's?
- **Body arc.** When to use → the domain facts that matter → a numbered Workflow → tips →
  Limits. Is the workflow actually actionable, with the commands spelled out?
- **Limits stated.** Does it say what the skill can't do?
- **Self-containment.** Does it assume another skill's files or a tool that isn't bundled?
- **Provenance.** Do the `references/` files say where their facts came from?
- **Assets are real.** Would the bundled example pass this skill's own validator?
- **Safety.** No secrets, no credentials, and no step that could steer an agent into a
  destructive command ([SECURITY.md](../../SECURITY.md)).
- **Catalog row.** Is the skill listed in the table in [README.md](../../README.md)?

## 3. Report

Print a PASS/FAIL table with one row per check and a one-line reason for every FAIL. Then
emit a **"How was this verified?"** block ready to paste into
[the pull request template](../PULL_REQUEST_TEMPLATE.md): the phrasings you tried, and the
validator output.
