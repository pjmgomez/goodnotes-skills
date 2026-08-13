# Goodnotes Study Set import format

Reference for building files that Goodnotes imports as a Study Set. Sourced from
Goodnotes Support, "Getting Started with Study Sets and Smart Learn".

## Platform and supported formats

- Study Sets and Smart Learn are **iOS/iPadOS only**. The file you build is imported on
  an iPhone or iPad.
- The importer accepts **.TXT, .CSV, and .TSV**. This skill emits **.CSV** and **.TSV**
  because their layout is documented; `.TXT` is accepted by Goodnotes but its expected
  structure isn't specified, so avoid generating it.

## The two-column layout

You can build a set outside Goodnotes in any spreadsheet tool (Excel, Google Sheets) and
export it, or write the file directly:

- **Column A holds the question, column B holds the answer.**
- **A card is a row.** The question in a row pairs with the answer in the *same* row —
  `A1` ↔ `B1`, `A2` ↔ `B2`, and so on.
- One question/answer pair per row.

## The no-header rule (why it matters)

Do **not** put a title or header in the top row. Goodnotes has no notion of a header row —
it converts every row into a flashcard, so a `Question,Answer` header becomes a stray card
that reads "Question" on the front and "Answer" on the back. This is the most common import
mistake, so the build script omits headers and the validator flags them.

## Escaping: CSV vs TSV

A flashcard's text often contains punctuation that collides with the delimiter.

- **CSV** — a field containing a comma, a double quote, or a line break must be wrapped in
  double quotes, and any double quote inside it is doubled (`"` → `""`). This is the RFC 4180
  convention that spreadsheets and Goodnotes expect. `build_study_set.py` applies it via
  Python's `csv` module, so multi-line answers survive intact.
- **TSV** — tab-separated values have no reliable quoting convention. The build script
  therefore replaces any embedded tab or line break in a field with a space so every row
  stays exactly two columns. Choose TSV when answers are dense with commas and you'd rather
  not look at quoted fields; choose CSV when you need to preserve line breaks inside a card.

Either way the file is written as **UTF-8**, so accented characters and non-Latin scripts
(useful for language study) import correctly.

## Importing into Goodnotes

1. Build and export the file as `.csv` or `.tsv`.
2. Import it into Goodnotes the same way as any file (Library → New/Import, or share the
   file to Goodnotes).
3. Goodnotes mass-converts the rows into a Study Set. Open it and study with **Smart Learn**
   (spaced repetition) or **Practice Mode** (review the whole set).

## Writing cards that work with Smart Learn

Smart Learn schedules reviews with spaced repetition and tests you with active recall.
Cards that respect how that works are learned faster:

- **One fact per card.** A card that asks for five things is really five cards; split it so
  the algorithm can track each fact's difficulty separately.
- **One unambiguous answer.** If a question could be answered several ways, tighten it.
  Avoid yes/no prompts — they let you guess without recalling anything.
- **Front-load the cue.** Put the distinctive word or concept at the start of the question.
- **Keep answers short.** A phrase or a single sentence recalls better than a paragraph;
  move extra context to its own card.
- **Prefer your own words.** Rephrasing source text into a genuine question beats copying a
  sentence and blanking a word.

## What can't be imported this way

- **Images and freeform ink** can be added to cards inside Goodnotes, but a CSV/TSV import is
  **text only** — it can't carry pictures or handwriting.
- **Formatting** (bold, colour, layout) isn't part of the import; cards come in as plain text.
