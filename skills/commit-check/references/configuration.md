# Commit Check — Configuration Reference

commit-check resolves settings from four sources, highest priority first:

1. **CLI arguments** — override per run (e.g. `--subject-max-length=72`).
2. **Environment variables** — `CCHK_*` (e.g. `CCHK_SUBJECT_MAX_LENGTH=72`).
3. **Configuration file** — `cchk.toml` or `commit-check.toml`.
4. **Built-in defaults** — used when nothing else sets a value.

## Config file discovery

With no `--config`, commit-check searches for the first of:

1. `cchk.toml`
2. `commit-check.toml`
3. `.github/cchk.toml`
4. `.github/commit-check.toml`

Pass `-c PATH` / `--config PATH` to use an explicit file. Put the file in the repo root
or `.github/`.

> IDE support: the TOML schema is published on [SchemaStore](https://www.schemastore.org/),
> so editors (VS Code with *Even Better TOML*, PyCharm, IntelliJ) give autocompletion and
> validation for `cchk.toml` with no manual setup.

## Full `cchk.toml` with defaults

Values below are the **built-in defaults**. Include only the keys you want to change.

```toml
# Learn more: https://commit-check.com

[commit]
# https://www.conventionalcommits.org
conventional_commits = true        # CC001: enforce Conventional Commits
message_pattern = ""               # custom regex; overrides conventional_commits when set
subject_capitalized = false        # CC002: subject must start with a capital letter
subject_imperative = false         # CC003: subject must use imperative mood
subject_max_length = 80            # CC004: max subject length
subject_min_length = 5             # CC005: min subject length
allow_commit_types = ["feat", "fix", "docs", "style", "refactor", "test", "chore", "perf", "build", "ci"]
allow_merge_commits = true         # CC006: allow merge commits
allow_revert_commits = true        # CC007: allow revert commits
allow_empty_commits = true         # CC008: allow empty commit messages
allow_fixup_commits = true         # CC009: allow fixup! commits
allow_wip_commits = true           # CC010: allow WIP commits
require_body = false               # CC011: require a commit body
require_signed_off_by = false      # CC012: require a Signed-off-by trailer (DCO)
ignore_authors = []                # authors/co-authors whose commits are skipped
ai_attribution = "ignore"          # CC013: "ignore" or "forbid" AI tool signatures
author_email_pattern = "^.+@.+$"   # CC102: regex for --author-email
author_name_pattern = ""           # CC101: regex for --author-name (empty = built-in)

[branch]
# https://conventionalbranch.org
conventional_branch = true         # CC201: enforce Conventional Branch
allow_branch_types = ["feature", "bugfix", "hotfix", "release", "chore", "feat", "fix", "build", "ci", "docs", "perf", "refactor", "test", "style", "ai", "claude", "codex", "copilot", "cursor", "dependabot", "renovate"]
allow_branch_names = []            # exact branch names always allowed (e.g. "main", "develop")
require_rebase_target = ""         # CC202: branch that HEAD must be rebased onto (e.g. "main")
ignore_authors = []                # authors whose branch checks are skipped

[push]
allow_force_push = true            # CC301: --no-force-push flips this to false
```

> Note: a real repo often tightens these — for example turning `subject_imperative` on,
> narrowing `allow_commit_types`, or setting `allow_wip_commits = false`. Always follow
> the repository's own file rather than assuming defaults.

## Option → CLI flag → environment variable

Most options have a matching CLI flag and `CCHK_*` variable; `message_pattern` is the
exception — it has no CLI flag and must come from the file or `CCHK_MESSAGE_PATTERN`.
CLI wins over env, env wins over the file.

### `[commit]`

| TOML key | CLI flag | Environment variable |
| --- | --- | --- |
| `conventional_commits` | `--conventional-commits` | `CCHK_CONVENTIONAL_COMMITS` |
| `message_pattern` | *(file/env only)* | `CCHK_MESSAGE_PATTERN` |
| `subject_capitalized` | `--subject-capitalized` | `CCHK_SUBJECT_CAPITALIZED` |
| `subject_imperative` | `--subject-imperative` | `CCHK_SUBJECT_IMPERATIVE` |
| `subject_max_length` | `--subject-max-length` | `CCHK_SUBJECT_MAX_LENGTH` |
| `subject_min_length` | `--subject-min-length` | `CCHK_SUBJECT_MIN_LENGTH` |
| `allow_commit_types` | `--allow-commit-types` | `CCHK_ALLOW_COMMIT_TYPES` |
| `allow_merge_commits` | `--allow-merge-commits` | `CCHK_ALLOW_MERGE_COMMITS` |
| `allow_revert_commits` | `--allow-revert-commits` | `CCHK_ALLOW_REVERT_COMMITS` |
| `allow_empty_commits` | `--allow-empty-commits` | `CCHK_ALLOW_EMPTY_COMMITS` |
| `allow_fixup_commits` | `--allow-fixup-commits` | `CCHK_ALLOW_FIXUP_COMMITS` |
| `allow_wip_commits` | `--allow-wip-commits` | `CCHK_ALLOW_WIP_COMMITS` |
| `require_body` | `--require-body` | `CCHK_REQUIRE_BODY` |
| `require_signed_off_by` | `--require-signed-off-by` | `CCHK_REQUIRE_SIGNED_OFF_BY` |
| `ignore_authors` | `--ignore-authors` | `CCHK_IGNORE_AUTHORS` |
| `ai_attribution` | `--ai-attribution` | `CCHK_AI_ATTRIBUTION` |
| `author_email_pattern` | `--author-email-pattern` | `CCHK_AUTHOR_EMAIL_PATTERN` |
| `author_name_pattern` | `--author-name-pattern` | `CCHK_AUTHOR_NAME_PATTERN` |

### `[branch]`

| TOML key | CLI flag | Environment variable |
| --- | --- | --- |
| `conventional_branch` | `--conventional-branch` | `CCHK_CONVENTIONAL_BRANCH` |
| `allow_branch_types` | `--allow-branch-types` | `CCHK_ALLOW_BRANCH_TYPES` |
| `allow_branch_names` | `--allow-branch-names` | `CCHK_ALLOW_BRANCH_NAMES` |
| `require_rebase_target` | `--require-rebase-target` | `CCHK_REQUIRE_REBASE_TARGET` |
| `ignore_authors` | `--branch-ignore-authors` | `CCHK_BRANCH_IGNORE_AUTHORS` |

### `[push]`

| TOML key | CLI flag | Environment variable |
| --- | --- | --- |
| `allow_force_push` | `--no-force-push` (sets `false`) | `CCHK_ALLOW_FORCE_PUSH` |

List-valued flags/vars are comma-separated, e.g. `--allow-commit-types feat,fix,docs` or
`CCHK_ALLOW_COMMIT_TYPES="feat,fix,docs"`. Booleans accept `true`/`false`.

## Organization-level config: `inherit_from`

Share a base policy across repos and override locally. Local keys always win.

```toml
# .github/cchk.toml
inherit_from = "github:my-org/.github:cchk.toml"

[commit]
subject_max_length = 72   # local override of the inherited base
```

Accepted `inherit_from` forms:

- GitHub shorthand: `github:owner/repo:path/to/cchk.toml`
- GitHub shorthand with ref: `github:owner/repo@main:path/to/cchk.toml`
- Local path (relative or absolute): `../shared/cchk.toml`
- HTTPS URL: `https://example.com/cchk.toml`

The `github:` form fetches from `raw.githubusercontent.com`. Plain-HTTP URLs are rejected.

## Complete rule catalog

Rule IDs are stable. ID ranges: `CC0xx` commit message, `CC1xx` author, `CC2xx` branch,
`CC3xx` push. Each rule's docs live at `https://commit-check.com/rules/#<lowercase-id>`.

| Rule ID | Check | Enforces |
| --- | --- | --- |
| CC001 | `message` | Conventional Commits (or `message_pattern`) |
| CC002 | `subject_capitalized` | Subject starts with a capital letter |
| CC003 | `subject_imperative` | Subject uses imperative mood |
| CC004 | `subject_max_length` | Subject at most `subject_max_length` chars |
| CC005 | `subject_min_length` | Subject at least `subject_min_length` chars |
| CC006 | `allow_merge_commits` | Rejects merge commits when `false` |
| CC007 | `allow_revert_commits` | Rejects revert commits when `false` |
| CC008 | `allow_empty_commits` | Rejects empty messages when `false` |
| CC009 | `allow_fixup_commits` | Rejects `fixup!` commits when `false` |
| CC010 | `allow_wip_commits` | Rejects WIP commits when `false` |
| CC011 | `require_body` | Requires a commit body when `true` |
| CC012 | `require_signed_off_by` | Requires a `Signed-off-by` trailer (DCO) |
| CC013 | `ai_attribution` | Rejects AI tool signatures when `"forbid"` |
| CC101 | `author_name` | Committer name matches `author_name_pattern` |
| CC102 | `author_email` | Committer email matches `author_email_pattern` |
| CC201 | `branch` | Conventional Branch naming |
| CC202 | `merge_base` | HEAD is rebased onto `require_rebase_target` |
| CC301 | `no_force_push` | No force push (checked in a `pre-push` hook) |

`ignore_authors` is internal bookkeeping and has no rule ID; matching authors cause the
relevant checks to report `skip`.

## AI attribution policy

`ai_attribution = "forbid"` (or `--ai-attribution=forbid`) rejects commits carrying known
AI-tool signatures (for example AI co-author trailers). The default `"ignore"` allows
them. Note this only inspects the commit-message text for those signatures: it discourages
AI attribution, but a commit whose attribution is removed or never added passes, so it
cannot prove a commit was not AI-authored. To exempt bot/automation authors from *all*
checks instead, add them to `ignore_authors`, e.g.
`ignore_authors = ["dependabot[bot]", "renovate[bot]", "copilot[bot]"]`.
