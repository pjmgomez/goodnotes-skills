#!/usr/bin/env python3
"""Validate a Goodnotes Study Set import file (.csv/.tsv).

Checks the rules Goodnotes needs: a UTF-8 file that parses cleanly, exactly two columns
per row, no empty cells, and — most importantly — no header row (a header like
"Question,Answer" would be imported as a real flashcard). Exits non-zero if anything fails,
so it can gate a build. Pass --json for a machine-readable report.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys

# First-row cells matching these on both sides almost certainly mean a stray header.
HEADER_WORDS = {
    "question", "answer", "q", "a", "front", "back",
    "term", "definition", "prompt", "response", "word", "meaning",
}


def _delimiter_for(path, override):
    if override == "tab":
        return "\t"
    if override == "comma":
        return ","
    return "\t" if path.lower().endswith(".tsv") else ","


def validate(path, delimiter):
    quoting = csv.QUOTE_NONE if delimiter == "\t" else csv.QUOTE_MINIMAL
    try:
        with open(path, encoding="utf-8", newline="") as handle:
            rows = list(csv.reader(handle, delimiter=delimiter, quoting=quoting))
    except FileNotFoundError:
        return [f"file not found: {path}"], 0
    except UnicodeDecodeError:
        return [f"file is not valid UTF-8: {path}"], 0

    rows = [row for row in rows if row and any(cell.strip() for cell in row)]
    if not rows:
        return ["file has no card rows"], 0

    problems = []
    first = rows[0]
    if (
        len(first) == 2
        and first[0].strip().lower() in HEADER_WORDS
        and first[1].strip().lower() in HEADER_WORDS
    ):
        problems.append(
            f'row 1 looks like a header ("{first[0]}", "{first[1]}") — Goodnotes would '
            "import it as a flashcard; remove it"
        )

    for i, row in enumerate(rows, start=1):
        if len(row) != 2:
            problems.append(f"row {i} has {len(row)} columns, expected 2")
            continue
        if not row[0].strip():
            problems.append(f"row {i} has an empty question")
        if not row[1].strip():
            problems.append(f"row {i} has an empty answer")

    return problems, len(rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("file", help="the .csv or .tsv to validate")
    parser.add_argument(
        "--delimiter",
        choices=["comma", "tab"],
        help="override the delimiter (default: infer from the file extension)",
    )
    parser.add_argument("--json", action="store_true", help="emit a JSON report")
    args = parser.parse_args()

    delimiter = _delimiter_for(args.file, args.delimiter)
    problems, count = validate(args.file, delimiter)
    ok = not problems

    if args.json:
        print(json.dumps({"file": args.file, "valid": ok, "card_count": count, "problems": problems}, indent=2))
    elif ok:
        print(f"PASS: {args.file} — {count} cards, 2 columns, no header, UTF-8.")
    else:
        print(f"FAIL: {args.file}")
        for problem in problems:
            print(f"  - {problem}")

    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
