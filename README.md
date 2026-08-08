# goodnotes-skills

A collection of [Agent Skills](https://agentskills.io) — self-contained folders of
instructions and references that an AI agent loads on demand to perform specialized
tasks well.

Each skill lives in its own directory with a `SKILL.md` (YAML frontmatter + Markdown
instructions) and optional `references/` files that are read only when needed.

## Skills

| Skill | Description |
| --- | --- |
| [`commit-check`](./commit-check/) | Author, validate, and fix Git commit messages, branch names, author identity, sign-off trailers, and AI-attribution/force-push policy with the [commit-check](https://github.com/commit-check/commit-check) tool. Covers Conventional Commits/Branch, the `cchk.toml` policy, pre-commit hooks, and the GitHub Action. |

## Using a skill

- **Claude Code / agents:** copy a skill directory (e.g. `commit-check/`) into your
  `.claude/skills/` folder, or point your agent at this repository.
- **Manually:** open the skill's `SKILL.md` and follow the instructions; the
  `references/` files provide deeper detail on demand.