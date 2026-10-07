---
type: regex
target: {source: file, path: compare/index.html}
match: not_contains
flags: i
pattern: 'shots/|\bcurrent\b|\bexisting\b|\bv[12]\b|\bvariants?\b|\bredesign\b'
weight: 2
---
