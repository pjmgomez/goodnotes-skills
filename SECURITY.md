# Security Policy

## Supported versions

This repository has no versioned releases — skills are consumed from `main`, and fixes land there.
Please report against the latest commit on `main`.

## Reporting a vulnerability

Please report security vulnerabilities **privately** — do not open a public issue.

- Preferred: use GitHub's private vulnerability reporting ("Report a vulnerability" under the
  repository's **Security** tab), if it is enabled.
- Otherwise, email the maintainers at patrick@patrickgomez.me.

Please include as much of the following as you can:

- A description of the issue and its impact.
- Steps to reproduce, or a proof of concept.
- The skill and file involved, and the commit you saw it on.
- Any known mitigations.

## What counts as a vulnerability here

Skills in this repository are Markdown instructions plus small helper scripts that an agent may run
on a contributor's machine. Reports we especially want:

- A bundled script that reads or writes outside the inputs and outputs it documents.
- Instructions in a `SKILL.md` that could steer an agent into running destructive commands or
  exposing credentials.
- Secrets or credentials committed anywhere in the repository.

## What to expect

- We will acknowledge your report within a few business days.
- We will keep you updated as we investigate and prepare a fix.
- We will credit you when the fix lands, unless you would prefer to remain anonymous.
