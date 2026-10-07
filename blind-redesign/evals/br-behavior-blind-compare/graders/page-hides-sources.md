---
type: regex
target: {source: file, path: compare/index.html}
match: not_contains
flags: i
pattern: 'shots/|current|existing|\bv[12]\b|variant|redesign'
weight: 2
---
