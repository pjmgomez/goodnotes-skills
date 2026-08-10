# goodnotes-skills

A library of reusable **Agent Skills** — self-contained, Markdown-only skills in the [SKILL.md format](https://code.visualstudio.com/docs/copilot/customization/agent-skills) that AI coding agents load on demand.

## What it does

An AI coding agent is a generalist. A skill hands it the procedure for one specific job — the format to
emit, the steps to follow, the mistakes to avoid — and the agent loads it only when the work calls for
it, so it costs nothing the rest of the time.

Each skill here is a single folder under `skills/`: a `SKILL.md` holding the instructions, plus the
optional `references/`, `scripts/`, and `assets/` it draws on. There is no build step and nothing to
package — the skills are Markdown, and any helper scripts are Python 3 standard library.

## Skills

| Skill | What it does |
| --- | --- |
| [study-set-builder](skills/study-set-builder/SKILL.md) | Turns notes, a PDF, or just a topic into a Goodnotes-importable Study Set — a `.csv`/`.tsv` of question/answer flashcards for Smart Learn. |

## Getting started

### Prerequisites

- An AI coding agent that supports the [SKILL.md format](https://code.visualstudio.com/docs/copilot/customization/agent-skills), such as GitHub Copilot in VS Code.
- Python 3, for skills that bundle scripts. They use only the standard library, so there is nothing to install.

### Install a skill

Skills are copied, not packaged. Take the whole skill folder — `SKILL.md` together with any
`references/`, `scripts/`, and `assets/` beside it — and put it in one of two places.

**For a single project**, add it to that repository's `.github/skills/` directory:

```
your-project/
└── .github/
    └── skills/
        └── study-set-builder/
            ├── SKILL.md
            ├── assets/
            ├── references/
            └── scripts/
```

**For every project**, put the same folder in your agent's personal skills folder instead — for
example `~/.agents/skills/study-set-builder/`. The exact location is agent-specific, so check your
agent's documentation.

Either way there is no registration step: the agent discovers the skill from its `description`.

## Usage

Describe the job in your own words and the agent matches it to a skill:

> Turn my lecture notes into a Goodnotes study set.

Or invoke a skill by name:

```
/study-set-builder make 20 flashcards on the Krebs cycle
```

The agent then follows that skill's workflow. Here it writes a two-column file — question, answer, no
header row — that Goodnotes converts into a Study Set on import:

```csv
What does the Krebs cycle produce per turn?,"3 NADH, 1 FADH2, 1 GTP, and 2 CO2"
Where in the cell does the Krebs cycle occur?,The mitochondrial matrix
```

## Getting help

Open an issue — there are templates for a [bug report](.github/ISSUE_TEMPLATE/bug_report.md) and a
[feature request](.github/ISSUE_TEMPLATE/feature_request.md).

## Contributing

Contributions are welcome, and a new skill is just one well-formed folder under `skills/`.

- [CONTRIBUTING.md](CONTRIBUTING.md) — the add process, frontmatter reference, `SKILL.md` template, and validation.
- [AGENTS.md](AGENTS.md) — the always-on guide agents follow when working in this repo.

Before opening a pull request, check the skill from the repository root:

```
python3 tools/validate_skill.py skills/<skill-name>
```

## Security

Found a vulnerability? Please report it privately by following [SECURITY.md](SECURITY.md) rather than
opening a public issue.

## License

[Apache 2.0](LICENSE).