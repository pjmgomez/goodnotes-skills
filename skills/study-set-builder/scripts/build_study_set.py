#!/usr/bin/env python3
"""Build a Goodnotes-importable Study Set file (.csv/.tsv) from question/answer pairs.

Goodnotes imports flashcards from a two-column file: column A = question, column B =
answer, one pair per row, and NO header row (a header becomes a stray flashcard). This
script writes that file with correct escaping and UTF-8 encoding so the import is clean.

Input is a JSON array (from --input or stdin). Each item is either
{"question": "...", "answer": "..."} (aliases: q/a, front/back, term/definition) or a
two-element [question, answer] list.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys


def _load_pairs(raw):
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        sys.exit(f"error: input is not valid JSON: {exc}")
    if not isinstance(data, list):
        sys.exit("error: expected a JSON array of question/answer pairs")

    pairs = []
    for i, item in enumerate(data):
        if isinstance(item, dict):
            question = item.get("question", item.get("q", item.get("front", item.get("term"))))
            answer = item.get("answer", item.get("a", item.get("back", item.get("definition"))))
        elif isinstance(item, (list, tuple)) and len(item) == 2:
            question, answer = item[0], item[1]
        else:
            sys.exit(f"error: item {i} is not a [question, answer] pair or object")

        if question is None or answer is None:
            sys.exit(f"error: item {i} is missing a question or answer")
        question, answer = str(question).strip(), str(answer).strip()
        if not question or not answer:
            sys.exit(f"error: item {i} has an empty question or answer")
        pairs.append((question, answer))

    if not pairs:
        sys.exit("error: no question/answer pairs found")
    return pairs


def _delimiter_for(path, override):
    if override == "tab":
        return "\t"
    if override == "comma":
        return ","
    return "\t" if path.lower().endswith(".tsv") else ","


def _sanitize_for_tsv(value):
    # TSV has no reliable quoting convention, so collapse embedded tabs/newlines to spaces.
    return " ".join(value.replace("\t", " ").split("\n")).replace("\r", " ")


def _write_csv(path, pairs, delimiter):
    with open(path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter=delimiter, quoting=csv.QUOTE_MINIMAL, lineterminator="\r\n")
        for question, answer in pairs:
            writer.writerow([question, answer])


def _write_tsv(path, pairs):
    with open(path, "w", encoding="utf-8", newline="") as handle:
        for question, answer in pairs:
            handle.write(_sanitize_for_tsv(question) + "\t" + _sanitize_for_tsv(answer) + "\r\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--input", help="JSON file of pairs; reads stdin if omitted")
    parser.add_argument("--output", required=True, help="destination .csv or .tsv")
    parser.add_argument(
        "--delimiter",
        choices=["comma", "tab"],
        help="override the delimiter (default: infer from the output extension)",
    )
    args = parser.parse_args()

    raw = open(args.input, encoding="utf-8").read() if args.input else sys.stdin.read()
    pairs = _load_pairs(raw)
    delimiter = _delimiter_for(args.output, args.delimiter)

    if delimiter == "\t":
        _write_tsv(args.output, pairs)
        kind = "TSV"
    else:
        _write_csv(args.output, pairs, delimiter)
        kind = "CSV"

    print(f"Wrote {len(pairs)} cards to {args.output} ({kind}, no header, UTF-8).")


if __name__ == "__main__":
    main()
