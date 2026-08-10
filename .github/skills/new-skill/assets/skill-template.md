<!-- Copy the block below into skills/<skill-name>/SKILL.md and replace every placeholder.
     The frontmatter `name` must equal the folder name. Keep the finished file under 500 lines. -->

---
name: skill-name
description: 'What the skill does, and the artifact it produces. Use when the user says <trigger>, <trigger>, or <trigger>; wants to <job>; or has <input> that needs <output>.'
---

# Skill Name

One or two lines on what this skill turns into what.

## When to use

- The user wants <job> done.
- They mention <trigger phrase>.
- They have <input> and need <output>.

## The format that matters

The domain facts an agent has to get right — the shape of the output, the rule that is
easiest to break, and why it matters. Push anything longer into
[references/<topic>.md](./references/<topic>.md).

## Workflow

1. **Confirm the target.** What is being produced, and where does it go.
2. **Gather the input.** How to handle each kind of source material.
3. **Produce the output.** Use `python3 scripts/<name>.py` rather than hand-formatting
   anything fiddly.
4. **Validate before handing off.** Run the bundled checker and fix what it reports.
5. **Tell the user the path** and what to do with the file next.

## Tips

- The judgment calls that separate a good result from a technically-correct one.

## Limits

- What this skill can't do, and the platform or format constraints behind it.
