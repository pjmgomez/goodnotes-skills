---
name: commit-check
description: Author, validate, and fix Git commit messages, branch names, author identity, DCO sign-off trailers, and AI-attribution or force-push policy using commit-check (the `commit-check`/`cchk` CLI and its Python API). Use whenever writing or amending a commit message, naming a branch, enforcing Conventional Commits or Conventional Branch, generating or editing a `cchk.toml` policy, wiring commit-check into pre-commit hooks or a GitHub Actions/CI pipeline, or fixing a commit that Commit-Check rejected (for example CC001, CC003, CC201, or CC301 errors) — even when the user asks for "commit message linting" or "commit policy" without naming the tool.
---

# Commit Check

## Overview

[Commit Check](https://github.com/commit-check/commit-check) is a lightweight policy
engine for Git commit metadata. One versioned TOML policy (`cchk.toml`) enforces the
same rules everywhere: the CLI, pre-commit hooks, CI, GitHub Actions, and AI agents.

It validates:

- **Commit messages** — [Conventional Commits](https://www.conventionalcommits.org), subject length, imperative mood, body, sign-off, WIP/fixup/merge/revert policy, AI attribution.
- **Branch names** — [Conventional Branch](https://conventionalbranch.org) and rebase-target freshness.
- **Author identity** — committer name and email patterns.
- **Push safety** — reject force pushes in a `pre-push` hook.

The CLI is invoked as `commit-check` or the shorter alias `cchk`. Exit code `0` means
pass (or skip), `1` means fail — so it drops straight into hooks and CI.

Use this skill for two things above all: **writing metadata that passes** (so commits
and branches are compliant the first time) and **diagnosing failures** (mapping a rule
ID back to a concrete fix).

## Installation and quick check

```bash
pip install commit-check          # installs `commit-check` and the `cchk` alias

commit-check --message --branch   # zero-config: Conventional Commits + Conventional Branch
```

With no config file, commit-check applies sensible built-in defaults (Conventional
Commits and Conventional Branch on; subject max length 80, min 5). To run without
installing, `pipx run commit-check ...` or `uvx commit-check ...` also work.

## Writing a compliant commit message

This is the most common task. Produce a [Conventional Commits](https://www.conventionalcommits.org)
message so the `message` (CC001) check passes.

**Format:**

```
<type>(<optional scope>)<optional !>: <description>

<optional body>

<optional footer(s)>
```

- **type** — one of the allowed types. Built-in default set: `feat`, `fix`, `docs`,
  `style`, `refactor`, `test`, `chore`, `perf`, `build`, `ci`. A repo may narrow or
  extend this via `allow_commit_types`; check the project's `cchk.toml` first.
- **description** — short summary. Defaults require **5–80 characters**. Keep it
  concise. Do not end with a period.
- **`!`** or a `BREAKING CHANGE:` footer marks a breaking change.
- **imperative mood** (CC003) and **capitalized subject** (CC002) are available but
  **off by default** — only satisfy them if the repo's config turns them on. When
  imperative mood is required, start with a base-form verb ("add", not "added"/"adds").

**Examples:**

Input: Added user authentication with JWT tokens
Output: `feat(auth): add JWT-based authentication`

Input: Fixed a crash when the config file is missing
Output: `fix: handle missing config file gracefully`

Input: Update the README with installation steps
Output: `docs: add installation steps to README`

Input: Remove the deprecated v1 REST endpoints (breaking)
Output:
```
feat(api)!: remove deprecated v1 endpoints

BREAKING CHANGE: the /v1/* routes are gone; use /v2/*.
```

If a repo requires DCO sign-off (`require_signed_off_by`, CC012), append a trailer with
`git commit --signoff` or add the line manually: `Signed-off-by: Name <email@example.com>`.

## Writing a compliant branch name

Produce a [Conventional Branch](https://conventionalbranch.org) name so the `branch`
(CC201) check passes.

**Format:** `<type>/<description>` with a lowercase, kebab-case description.

Built-in default types include `feature`, `bugfix`, `hotfix`, `release`, `chore` plus
the Conventional Commit types and AI/bot prefixes (`ai`, `claude`, `codex`, `copilot`,
`cursor`, `dependabot`, `renovate`).

Examples: `feature/add-streaming`, `bugfix/fix-null-pointer`, `chore/bump-deps`.

Avoid names like `BadBranch` or `my_feature` (no type prefix / not kebab-case).

## Validating with the CLI

Select **which** checks run with these flags; each maps to a rule family:

| Flag | Short | Checks |
| --- | --- | --- |
| `--message` | `-m` | commit message rules (CC001–CC013) |
| `--branch` | `-b` | branch name + rebase target (CC201, CC202) |
| `--author-name` | `-n` | committer name (CC101) |
| `--author-email` | `-e` | committer email (CC102) |
| `--no-force-push` | | reject force push (CC301); reads `pre-push` stdin, else compares against upstream |
| `--dry-run` | `-d` | run but always exit `0` |

Provide the **commit message** by piping to stdin or passing a file path (pre-commit
passes the `.git/COMMIT_EDITMSG` path positionally). Branch and author checks read from
the current Git repository.

```bash
# Validate a message (stdin) — exit 0
echo "feat: add streaming support" | commit-check --message

# Validate a message file (how pre-commit calls it)
commit-check "$PWD/.git/COMMIT_EDITMSG"

# Validate the current branch name
commit-check --branch
```

### Machine-readable output for automation

Pass `--format json` to any invocation to get structured results (exit code
unchanged). Prefer this when consuming results programmatically or feeding an LLM:

```bash
echo "wip bad commit" | commit-check -m --format json
```

```json
{
  "status": "fail",
  "checks": [
    {
      "rule_id": "CC001",
      "check": "message",
      "status": "fail",
      "value": "wip bad commit",
      "error": "The commit message should follow Conventional Commits. See https://www.conventionalcommits.org",
      "suggest": "Use <type>(<scope>): <description>, where <type> is one of: feat, fix, docs, style, refactor, test, chore, perf, build, ci",
      "docs_url": "https://commit-check.com/rules/#cc001"
    }
  ]
}
```

`status` is `pass`, `fail`, or `skip`. **`skip` is not `pass`**: it means the rule never
ran (for example the author matched `ignore_authors`, or there was nothing to check). A
fully skipped run still exits `0`.

For quieter human output: `--no-banner` drops the ASCII-art failure banner; `--compact`
prints one `[FAIL] <rule_id> <check>: <value>` line per failure (and implies `--no-banner`).

### Override policy per run

Any `cchk.toml` option has a matching CLI flag (and a `CCHK_*` environment variable),
useful for one-off checks without editing config:

```bash
commit-check -m --subject-imperative=true --subject-max-length=72
```

See `references/configuration.md` for the complete flag/env/option matrix.

## Reading and fixing failures

Each failing check reports a stable **rule ID**, an `error` (what is wrong) and a
`suggest` (how to fix). Fix the value and re-run. Most-used IDs:

| Rule | Check | Fix |
| --- | --- | --- |
| CC001 | message (Conventional Commits) | Rewrite as `<type>(<scope>): <description>` using an allowed type. |
| CC003 | subject_imperative | Use a base-form verb: `add`, not `added`/`adds`/`adding`. |
| CC004 | subject_max_length | Shorten the subject (default ≤ 80 chars). |
| CC005 | subject_min_length | Lengthen the subject (default ≥ 5 chars). |
| CC010 | allow_wip_commits | Remove `WIP`/`wip` and finish the change. |
| CC012 | require_signed_off_by | Add `Signed-off-by:` via `git commit --signoff`. |
| CC013 | ai_attribution | Remove AI/co-author trailers when the repo sets `ai_attribution = "forbid"`. |
| CC101 / CC102 | author_name / author_email | `git config user.name '...'` / `git config user.email '...@...'`. |
| CC201 | branch (Conventional Branch) | Rename to `<type>/<kebab-description>`, or add to `allow_branch_names`. |
| CC202 | merge_base | Rebase the branch onto its `require_rebase_target`. |
| CC301 | no_force_push | Push without `--force`/`--force-with-lease`. |

The full catalog (CC001–CC301) is in `references/configuration.md`.

To fix an **already-created** commit: amend with a corrected message
(`git commit --amend`) for the latest commit, or use an interactive rebase for older
ones. To fix a branch name, create a correctly named branch and move the work onto it.

## Python API (no subprocess)

`commit_check.api` validates without spawning a process — ideal for agents and tools.
All functions return the same dict schema as the JSON output:

```python
from commit_check.api import validate_message, validate_branch, validate_author, validate_all

validate_message("feat: add streaming support")["status"]          # "pass"
validate_branch("feature/add-streaming")["status"]                 # "pass"

# Restrict allowed types with a partial config override
validate_message("docs: update readme",
                 config={"commit": {"allow_commit_types": ["feat", "fix"]}})["status"]  # "fail"

# Run several checks at once
result = validate_all(
    message="feat: implement new feature",
    branch="feature/new-feature",
    author_name="Ada Lovelace",
    author_email="ada@example.com",
)
if result["status"] == "fail":
    for check in result["checks"]:
        if check["status"] == "fail":
            print(check["check"], check["error"], "->", check["suggest"])
```

Functions: `validate_message(message, *, config=None)`,
`validate_branch(branch=None, *, config=None)`,
`validate_author(name=None, email=None, *, config=None)`,
`validate_push(push_refs, *, config=None)`,
`validate_all(message=None, branch=None, author_name=None, author_email=None, *, config=None)`.
`config` is a partial dict shaped like `cchk.toml`; omitted keys fall back to defaults.

## Configuration

commit-check reads config, in priority order: **CLI args > `CCHK_*` env vars > TOML file
> built-in defaults**. It auto-discovers the first of `cchk.toml`, `commit-check.toml`,
`.github/cchk.toml`, `.github/commit-check.toml`, or takes an explicit `--config PATH`.
Organizations can share a base policy with `inherit_from`.

**Before writing or changing a policy, read `references/configuration.md`** — it lists
every `[commit]`, `[branch]`, and `[push]` option with its default, the matching CLI
flag and `CCHK_*` variable, `inherit_from` forms, and the complete rule catalog.

## Integrations

**When setting up pre-commit hooks, a GitHub Action, or CI, read
`references/integrations.md`.** It has the ready-to-use `.pre-commit-config.yaml` hook
IDs (`check-message`, `check-branch`, `check-author-name`, `check-author-email`,
`check-no-force-push`), the `commit-check/commit-check-action` workflow (inputs,
`fetch-depth: 0`, PR comments, job summary), and plain-CI recipes. Pin to the latest
release (currently commit-check `v2.13.4`, the action `v2.13.1`).

## Guidelines

- **Match the project's own policy.** Inspect any existing `cchk.toml` (or `.github/`
  copy) and follow its `allow_commit_types`, length limits, and toggles rather than the
  defaults, which vary from a repo's chosen policy.
- **Consume `--format json`** (or the Python API) when acting on results
  programmatically; parse `status` and per-check `error`/`suggest` to self-correct.
- **`skip` ≠ `pass`.** A skipped run validated nothing; don't report it as compliant.
- **Bypass bots via `ignore_authors`**, not by weakening rules for everyone.
- **Piping `git push` output into commit-check is not force-push prevention.** Use the
  `check-no-force-push` `pre-push` hook; the push metadata only exists there.
