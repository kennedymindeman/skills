---
name: read-document
description: Gets the text out of PDF, docx, pptx, and xlsx files, and judges when a page still needs a visual read. Use when a task hands over a .pdf, .docx, .pptx, or .xlsx path - a paper, deck, contract, statement, spreadsheet - when a document has to be quoted verbatim, or when briefing a subagent that will read one.
---

A page read as an image spends a screenful of tokens, comes back paraphrased, and can't be quoted exactly. The same page extracted as text costs a fraction of that and comes back verbatim. So every document is **extracted** first, and a **visual read** is spent only where extraction has nothing to give - a scan with no text layer, or a question the words can't answer.

`~/wiki/document-text-extraction.md` is the durable page for this; new format recipes land there.

## Extract

Each command takes the path as an argument rather than inlining it, so spaces and quotes in filenames survive. Page and sheet markers go in the output; they are how a visual read later gets narrowed to a page range.

PDF:

```bash
uv run --quiet --with pypdf python -c "
import sys
from pypdf import PdfReader
for i, p in enumerate(PdfReader(sys.argv[1]).pages, 1):
    print(f'--- page {i} ---')
    print(p.extract_text())
" report.pdf
```

`pdftotext -layout report.pdf -` is faster where it is installed, and `-layout` holds columns and tables apart instead of interleaving them. `pypdf` needs no install beyond `uv`, so it is the safe default in a brief.

docx - paragraphs and tables are separate collections, and text that only lives in a table is missed by reading paragraphs alone:

```bash
uv run --quiet --with python-docx python -c "
import sys, docx
d = docx.Document(sys.argv[1])
for p in d.paragraphs:
    print(p.text)
for t in d.tables:
    for r in t.rows:
        print('\t'.join(c.text for c in r.cells))
" contract.docx
```

pptx - text lives on shapes, so walk the shapes of each slide:

```bash
uv run --quiet --with python-pptx python -c "
import sys
from pptx import Presentation
for i, s in enumerate(Presentation(sys.argv[1]).slides, 1):
    print(f'--- slide {i} ---')
    for sh in s.shapes:
        if sh.has_text_frame:
            print(sh.text_frame.text)
" deck.pptx
```

xlsx - `data_only=True` returns the last computed values; without it, formula cells come back as `=SUM(A1:A9)` strings:

```bash
uv run --quiet --with openpyxl python -c "
import sys, openpyxl
wb = openpyxl.load_workbook(sys.argv[1], data_only=True)
for ws in wb:
    print(f'--- {ws.title} ---')
    for row in ws.iter_rows(values_only=True):
        print('\t'.join('' if c is None else str(c) for c in row))
" figures.xlsx
```

For a long document, pipe the extraction to a file and grep it rather than printing the whole thing into context.

## Spend the visual read

Two cases earn one, and both are visible in the extraction you already ran:

- **Empty or garbled output** - a scan, an image-only export, or a PDF whose text layer is broken. There is no text to get; read the pages.
- **The question is about layout** - a figure, chart, diagram, signature, form, or how a table is arranged on the page. The words are already extracted and the arrangement is what's missing.

Either way, read the pages the extraction pointed at, not the document - `Read` with `pages: "12-14"`. On a scan with no extraction to point at, work in chunks and stop at the answer.

Everything else - long, dense, badly formatted, a hundred pages - is still an extraction. Length is a reason to grep the text, not to look at it.

## Delegating

A subagent inherits none of this: dispatch a document review without saying so and it will page through the file visually. Put the instruction in the brief, with the format's command and the path to `~/wiki/document-text-extraction.md`, the same way you would hand it any other tool it needs.
