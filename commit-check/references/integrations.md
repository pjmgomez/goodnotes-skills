# Commit Check — Integrations

Wire commit-check into the points where commits, branches, and pushes happen. Pin to
the latest release: commit-check `v2.13.4`, `commit-check-action` `v2.13.1`.

## pre-commit hooks

Add commit-check to [`.pre-commit-config.yaml`](https://pre-commit.com). Available hook
IDs and the Git stage each runs at:

| Hook ID | Stage | Purpose |
| --- | --- | --- |
| `check-message` | `commit-msg` | Validate the commit message |
| `check-branch` | `pre-commit` | Validate the branch name |
| `check-author-name` | `pre-commit` | Validate the committer name |
| `check-author-email` | `pre-commit` | Validate the committer email |
| `check-no-force-push` | `pre-push` | Reject force pushes |

```yaml
repos:
  - repo: https://github.com/commit-check/commit-check
    rev: v2.13.4
    hooks:
      - id: check-message
      - id: check-branch
      - id: check-author-name
      - id: check-author-email
      - id: check-no-force-push
```

Because these hooks span three stages, install all of them:

```bash
pre-commit install --hook-type commit-msg --hook-type pre-commit --hook-type pre-push
```

Pass extra arguments through `args` (they map to the CLI flags in
`references/configuration.md`):

```yaml
      - id: check-message
        args: [--subject-imperative=false, --subject-max-length=100]
      - id: check-author-email
        args: [--no-banner, --author-email, --author-email-pattern=^.+@example\.com$]
```

## GitHub Actions

Use the composite [`commit-check/commit-check-action`](https://github.com/commit-check/commit-check-action).
Create `.github/workflows/commit-check.yml`:

```yaml
name: Commit Check

on:
  pull_request:
    branches: 'main'

jobs:
  commit-check:
    runs-on: ubuntu-latest
    permissions:            # required for pr-comments
      contents: read
      pull-requests: write
    steps:
      - uses: actions/checkout@v7
        with:
          fetch-depth: 0    # required for branch / merge-base checks
      - uses: commit-check/commit-check-action@v2.13.1
        with:
          message: true
          branch: true
          author-name: false
          author-email: false
          job-summary: true
          pr-comments: true
```

`fetch-depth: 0` is important — branch and rebase-target checks need full history.
Pin to a released tag (`@v2.13.1`) for reproducibility, or track the major tag (`@v2`)
for the latest v2.

### Action inputs

| Input | Default | Description |
| --- | --- | --- |
| `message` | `true` | Check commit message (Conventional Commits) |
| `branch` | `true` | Check branch name (Conventional Branch) |
| `author-name` | `false` | Check committer name |
| `author-email` | `false` | Check committer email |
| `dry-run` | `false` | Run without failing (exit `0`) |
| `job-summary` | `true` | Write results to the workflow job summary |
| `pr-comments` | `false` | Post results as PR comments (needs `pull-requests: write`) |
| `pr-title` | `false` | Check the PR **title** (great for Squash & Merge) |

The action still reads a `cchk.toml` / `commit-check.toml` in the repo for the detailed
rule settings; these inputs only toggle **which** scopes run.

### Consuming the JSON output

The action exposes a `result` output (structured JSON) for downstream steps:

```yaml
      - uses: commit-check/commit-check-action@v2.13.1
        id: check
        with:
          message: true
          branch: true
      - run: echo '${{ steps.check.outputs.result }}' | jq .status
```

> Notes: `pr-comments` is skipped for pull requests from forks (see the action's
> `docs/fork-pr-comments.md`). `pr-title` only applies to `pull_request` /
> `pull_request_target` events and is ignored on `push`.

## Plain CI (any provider)

Without the dedicated Action, install and run the CLI directly. Non-zero exit fails the
job:

```bash
pip install commit-check

commit-check --branch --author-name --author-email

# Validate the latest commit message
git log -1 --pretty=%B | commit-check --message
```

For custom reporting, add `--format json` and parse the output (for example with `jq`).

## Local Git hooks (no pre-commit framework)

commit-check works from a raw hook too. A minimal `.git/hooks/commit-msg`:

```bash
#!/usr/bin/env bash
commit-check --message "$1"
```

For force-push protection, call `commit-check --no-force-push` from a `pre-push` hook —
it reads the ref updates Git provides on the hook's stdin. Running it standalone instead
compares `HEAD` against the current branch's configured upstream.

> Piping `git push` output into commit-check does **not** prevent a force push: the push
> has already started and standard `git push` output lacks the pre-push ref metadata the
> `no_force_push` check relies on. Use the `pre-push` hook.

## Badge

Advertise enforcement in your README:

```markdown
[![commit-check](https://img.shields.io/badge/commit--check-enabled-brightgreen?logo=Git&logoColor=white&color=%232c9ccd)](https://github.com/commit-check/commit-check)
```
