#!/usr/bin/env python3
"""Validate a skill folder against this repository's SKILL.md conventions.

Checks the rules that fail silently when broken: a frontmatter `name` that must equal the
folder name, a `description` an agent can match on, a SKILL.md small enough to load cheaply,
`./` links that resolve and stay one level deep, and self-containment. Exits non-zero if
anything fails, so it can gate a build. Pass --json for a machine-readable report.

With no arguments it checks every folder under skills/, so run it from the repository root.
Judgment calls it cannot make -- is the description phrased the way a user would type it? --
are covered by the checklist in CONTRIBUTING.md.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

SKILLS_DIR = "skills"
MAX_SKILL_LINES = 500
MAX_REFERENCE_LINES = 300
MAX_DESCRIPTION_CHARS = 1024

ALLOWED_KEYS = {"name", "description", "argument-hint", "user-invocable", "disable-model-invocation"}
BOOLEAN_KEYS = {"user-invocable", "disable-model-invocation"}

NAME_PATTERN = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
FIELD_PATTERN = re.compile(r"^([A-Za-z0-9_-]+):[ \t]*(.*)$")
LINK_PATTERN = re.compile(r"\]\(([^)]*)\)")
REFERENCE_PATTERN = re.compile(r"^[ \t]{0,3}\[([^\]]+)\]:[ \t]*(\S+)", re.MULTILINE)
TAG_PATTERN = re.compile(r"<[A-Za-z/][^>]*>")
CONTENTS_PATTERN = re.compile(r"^#{1,6}\s+.*contents", re.IGNORECASE | re.MULTILINE)
# Unquoted scalars YAML reads as null, a boolean or a number rather than as text.
_NON_STRING_PATTERN = re.compile(r"^(~|null|true|false|yes|no|on|off|-?\d+(\.\d+)?)$", re.IGNORECASE)
SECRET_SUFFIXES = (".pem", ".key")


def _read(path):
    try:
        with open(path, encoding="utf-8") as handle:
            return handle.read(), None
    except FileNotFoundError:
        return None, f"missing file: {os.path.basename(path)}"
    except UnicodeDecodeError:
        return None, f"file is not valid UTF-8: {os.path.basename(path)}"
    except OSError as error:
        # A malformed skill can make the path a directory or unreadable; report it instead of crashing.
        return None, f"cannot read {os.path.basename(path)}: {error.strerror or error}"


def _scalar(value):
    # Returns (text, quoted, problem): the quoting has to survive, or a quoted boolean reads as a boolean.
    if value and value[0] in "\"'":
        quote = value[0]
        if len(value) < 2 or value[-1] != quote:
            return value, True, "value opens with a quote that is never closed"
        inner = value[1:-1]
        return (inner.replace("''", "'") if quote == "'" else inner), True, None
    return value, False, None


def _parse_frontmatter(text):
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, set(), ["SKILL.md does not open with a --- frontmatter fence"]
    end = next((i for i, line in enumerate(lines[1:], start=1) if line.strip() == "---"), None)
    if end is None:
        return {}, set(), ["SKILL.md frontmatter is never closed with ---"]

    fields, quoted, problems = {}, set(), []
    for number, line in enumerate(lines[1:end], start=2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        match = FIELD_PATTERN.match(line)
        # Report anything this parser can't read rather than skipping it, so a malformed key never passes silently.
        if not match:
            problems.append(f'frontmatter line {number} is not a single-line "key: value": {line.strip()}')
            continue
        key = match.group(1)
        if key in fields:
            problems.append(f"frontmatter line {number} repeats the key: {key}")
        value, is_quoted, problem = _scalar(match.group(2).strip())
        if problem:
            problems.append(f"frontmatter line {number} {problem}: {line.strip()}")
        fields[key] = value
        if is_quoted:
            quoted.add(key)
        else:
            quoted.discard(key)
    return fields, quoted, problems


def _check_frontmatter(skill_name, fields, quoted):
    problems = []
    name = fields.get("name")
    if name and "name" not in quoted and _NON_STRING_PATTERN.match(name):
        # YAML reads these unquoted scalars as null/boolean/number, not as the text they look like.
        problems.append(f'name "{name}" is not a string — quote it')
    elif not name:
        problems.append("frontmatter is missing name")
    else:
        if name != skill_name:
            problems.append(
                f'name "{name}" does not match the folder name "{skill_name}" — the skill will never load'
            )
        if not NAME_PATTERN.match(name) or len(name) > 64:
            problems.append(f'name "{name}" must be 1-64 chars of lowercase letters, digits and single hyphens')

    description = fields.get("description")
    if description and "description" not in quoted and _NON_STRING_PATTERN.match(description):
        problems.append(f'description "{description}" is not a string — quote it')
    elif not description:
        problems.append("frontmatter is missing a non-empty description — an agent has nothing to match on")
    elif len(description) > MAX_DESCRIPTION_CHARS:
        problems.append(f"description is {len(description)} chars, the limit is {MAX_DESCRIPTION_CHARS}")
    elif TAG_PATTERN.search(description):
        # Angle brackets are stripped as markup when the description is rendered, silently mangling the trigger text.
        problems.append(
            f'description contains "{TAG_PATTERN.search(description).group(0)}", which is stripped as markup — '
            "write the placeholder without angle brackets"
        )

    for key in sorted(set(fields) - ALLOWED_KEYS):
        problems.append(f"unknown frontmatter key: {key}")
    for key in sorted(BOOLEAN_KEYS & set(fields)):
        if fields[key] not in ("true", "false") or key in quoted:
            # A quoted "true" is the string, not the boolean the schema expects.
            problems.append(f'{key} must be an unquoted true or false, got "{fields[key]}"')
    return problems


def _link_targets(text):
    for raw in LINK_PATTERN.findall(text):
        parts = raw.split()
        yield parts[0] if parts else ""
    # Reference-style definitions ("[id]: ./references/x.md") are links too, and just as breakable.
    for _label, target in REFERENCE_PATTERN.findall(text):
        yield target.strip("<>")


def _check_links(skill_dir, path, text):
    problems = []
    where = os.path.relpath(path, skill_dir)
    root = os.path.realpath(skill_dir)
    for target in _link_targets(text):
        if not target or target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        resolved = os.path.normpath(os.path.join(os.path.dirname(path), target.split("#")[0]))
        # Compare the real paths: a symlink inside the skill can still point outside it.
        if os.path.relpath(os.path.realpath(resolved), root).startswith(".."):
            problems.append(f"{where} links outside the skill folder ({target}) — skills must be self-contained")
        elif not os.path.exists(resolved):
            problems.append(f"{where} links to a missing file: {target}")
    return problems


def _bundled_files(skill_dir):
    for root, _dirs, names in os.walk(skill_dir):
        for name in names:
            yield os.path.join(root, name)


def validate(path):
    stats = {"skill_md_lines": 0, "bundled_files": 0}
    skill_dir = os.path.normpath(path)
    if not os.path.isdir(skill_dir):
        return [f"not a directory: {path}"], stats

    text, problem = _read(os.path.join(skill_dir, "SKILL.md"))
    if text is None:
        return [problem], stats

    fields, quoted, problems = _parse_frontmatter(text)
    problems += _check_frontmatter(os.path.basename(skill_dir), fields, quoted)

    stats["skill_md_lines"] = len(text.splitlines())
    if stats["skill_md_lines"] > MAX_SKILL_LINES:
        problems.append(
            f"SKILL.md is {stats['skill_md_lines']} lines, over the {MAX_SKILL_LINES}-line budget — "
            "move depth into references/"
        )

    for file_path in sorted(_bundled_files(skill_dir)):
        relative = os.path.relpath(file_path, skill_dir)
        name = os.path.basename(relative)
        if relative != "SKILL.md":
            stats["bundled_files"] += 1
        if relative.count(os.sep) > 1:
            problems.append(f"bundled file is more than one level deep: {relative}")
        if name.startswith(".env") or name.endswith(SECRET_SUFFIXES):
            problems.append(f"possible secret committed in the skill: {relative}")
        if not name.endswith(".md"):
            continue

        content, problem = _read(file_path)
        if content is None:
            problems.append(problem)
            continue
        problems += _check_links(skill_dir, file_path, content)
        if relative.startswith("references" + os.sep) and len(content.splitlines()) > MAX_REFERENCE_LINES:
            if not CONTENTS_PATTERN.search(content):
                problems.append(f'{relative} is over {MAX_REFERENCE_LINES} lines and has no "Contents" heading')

    return problems, stats


def _default_targets():
    if not os.path.isdir(SKILLS_DIR):
        return []
    return sorted(
        os.path.join(SKILLS_DIR, name)
        for name in os.listdir(SKILLS_DIR)
        if os.path.isdir(os.path.join(SKILLS_DIR, name))
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("skill", nargs="*", help=f"skill folders to check (default: every folder under {SKILLS_DIR}/)")
    parser.add_argument("--json", action="store_true", help="emit a JSON report")
    args = parser.parse_args()

    targets = args.skill or _default_targets()
    if not targets:
        sys.exit(f"error: no skill folders found in {SKILLS_DIR}/ — run this from the repository root")

    reports = []
    for target in targets:
        problems, stats = validate(target)
        reports.append({"skill": target, "valid": not problems, "problems": problems, **stats})

    ok = all(report["valid"] for report in reports)
    if args.json:
        print(json.dumps({"valid": ok, "checked": len(reports), "skills": reports}, indent=2))
    else:
        for report in reports:
            if report["valid"]:
                print(
                    f"PASS: {report['skill']} — SKILL.md {report['skill_md_lines']} lines, "
                    f"{report['bundled_files']} bundled files, links resolve."
                )
            else:
                print(f"FAIL: {report['skill']}")
                for problem in report["problems"]:
                    print(f"  - {problem}")

    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
