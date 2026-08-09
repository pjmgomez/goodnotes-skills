---
name: study-set-builder
description: 'Turn notes, PDFs, documents, or a topic into a Goodnotes-importable Study Set file (.CSV/.TSV) of question/answer flashcards. Use when the user wants to make, build, generate, or export flashcards or a study set for Goodnotes; mentions Study Sets, Smart Learn, spaced repetition, or Practice Mode; wants to convert lecture notes, a textbook, or a PDF into reviewable cards; asks to "make N flashcards about X" for studying on an iPad or iPhone; or has a CSV/TSV of question-answer pairs that Goodnotes will not import cleanly and needs it reformatted (column A = question, column B = answer, no header row).'
---

# Study Set Builder

Turn source material into a **Goodnotes Study Set** — a two-column file of
question/answer flashcards that Goodnotes imports and drills with Smart Learn.

## When to use

- The user wants to make, build, generate, or export flashcards or a study set for Goodnotes.
- They mention Study Sets, Smart Learn, spaced repetition, or Practice Mode.
- They want to turn lecture notes, a textbook, or a PDF into reviewable cards.
- They have a CSV/TSV of question–answer pairs that Goodnotes won't import cleanly and needs fixing.

## The format that matters

Goodnotes builds a Study Set from a plain two-column file:

- **Column A = question, column B = answer.** Each row is one card; the question in a
  row pairs with the answer in the same row.
- **No header row.** A first row like `Question,Answer` is imported as a real flashcard,
  so it must not be there. This is the single most common import mistake.
- Save as **.CSV** (default) or **.TSV**. Both import; prefer TSV when answers are full of commas.

Full rules, import steps, and card-writing tips: [references/goodnotes-format.md](./references/goodnotes-format.md).

## Workflow

1. **Confirm the target.** Default to `.csv`. Ask where to save if it isn't obvious
   (e.g. `study-set.csv` in the workspace). Note that importing is iOS/iPadOS only.

2. **Get the question/answer pairs.** How depends on the source:
   - **Notes / pasted text** — pull out the testable facts; one idea per card.
   - **PDF / document** — read it, then extract the key definitions, facts, and relationships.
   - **A topic** ("make 20 cards on the Krebs cycle") — generate that many cards covering
     the topic; if no count is given, aim for 15–25.
   - **Existing CSV/TSV** — parse it and **drop any header row**, split each line back to
     exactly two columns, fix ragged rows, and remove duplicates and blanks.

3. **Write the file with the script**, don't hand-format it. Correct escaping of commas,
   quotes, and newlines inside a card is fiddly and easy to get subtly wrong, and the
   script also guarantees there is no header row.

   Put the pairs in a JSON array — each item `{"question": "...", "answer": "..."}` — and run:

   ```
   python3 scripts/build_study_set.py --input pairs.json --output study-set.csv
   ```

   Use a `.tsv` output path for tab-separated; pass `--delimiter comma|tab` to override the
   extension. The script reads JSON from stdin if `--input` is omitted.

4. **Validate before handing off:**

   ```
   python3 scripts/validate_study_set.py study-set.csv
   ```

   It fails loudly on a stray header, empty cells, or rows that aren't exactly two columns.
   Fix anything it reports and re-run.

5. **Tell the user the file path and how to import it:** import the file into Goodnotes the
   same way as any file and it auto-converts into a Study Set ready for Smart Learn.

## Writing cards that work with Smart Learn

Smart Learn uses spaced repetition and active recall, which reward focused cards:

- One fact per card — split "list the causes and effects" into separate cards.
- Ask for a single, unambiguous answer; avoid yes/no prompts.
- Keep answers tight — a phrase or a sentence, not a paragraph.

More detail is in [references/goodnotes-format.md](./references/goodnotes-format.md).

## Limits

- Study Sets and Smart Learn import is **iOS/iPadOS only** in Goodnotes.
- Imported cards are **text only** — a CSV/TSV can't carry images or freeform ink.
- Goodnotes also accepts `.TXT`, but its layout isn't documented, so this skill emits `.CSV`/`.TSV`.
