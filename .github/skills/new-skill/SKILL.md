---
name: new-skill
description: 'Scaffold a new skill folder in this repository — a skills/ folder holding SKILL.md with valid frontmatter, a trigger-rich description, and the optional references/, scripts/, and assets/ beside it. Use when adding, creating, or scaffolding a new skill, when starting a skill for a new job or format, or when asked to "add a skill that does X" to the goodnotes-skills library.'
argument-hint: 'what the skill should do'
---

# New skill

Add a well-formed skill to `skills/`. The full authoring reference is
[CONTRIBUTING.md](../../../CONTRIBUTING.md); this is the procedure.

## When to use

- Adding a new skill to this repository.
- Turning a repeated manual procedure into a skill.
- Someone asks to "add a skill that does X".

## Workflow

1. **Pin down the job.** One skill does one job and produces one concrete artifact. If you
   can't name the output it emits, the skill isn't ready to scaffold — ask what the user
   expects to have in their hands at the end.

2. **Name it after the job, not the tool.** `pdf-to-study-set`, not `pdf-helper`. Lowercase
   letters, digits and single hyphens, 1–64 chars. This string is also the slash command, so
   check it doesn't collide with an existing folder in `skills/`.

3. **Create `skills/<name>/SKILL.md`** from [the template](./assets/skill-template.md).
   The frontmatter `name` must equal the folder name exactly — a mismatch means the skill
   never loads, with no error message.

4. **Write the description last, and write it as triggers.** List five or more phrasings a
   user would actually type to reach this skill, then fold every one of them in. The
   description is the only thing an agent sees when deciding whether to load the skill, so a
   phrase that isn't in it is a phrase that can't find it. Say what it does *and* when to use
   it; keep it under 1024 characters.

5. **Add subfolders only if the skill needs them**, one level deep:
   - `references/` — look-up detail that would bloat `SKILL.md`. Cite where the facts came from.
   - `scripts/` — Python 3, standard library only, invoked as `python3 scripts/<name>.py`.
   - `assets/` — templates or example output the skill emits. Make examples real and runnable.

6. **Add the catalog row** to the Skills table in [README.md](../../../README.md). Nothing
   enforces this, so it is the step that gets forgotten.

7. **Validate**, from the repository root:

   ```
   python3 tools/validate_skill.py skills/<name>
   ```

   Fix anything it reports and re-run. It only covers the mechanical rules — for the
   judgment ones, follow up with `/validate-skill <name>`.

8. **Report** the path you created, the trigger phrases the description covers, and the
   validator output, so they can go straight into the pull request.

## Limits

- Keep `SKILL.md` under 500 lines; depth belongs in `references/`.
- Skills are self-contained — never reach into another skill's files.
- Never write a step that steers an agent into a destructive command or exposes credentials.
