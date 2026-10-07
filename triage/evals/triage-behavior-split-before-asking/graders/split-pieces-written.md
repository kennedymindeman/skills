---
type: regex
target: files
flags: m
# At least two new top-level inbox notes.
pattern: '^inbox/[^/\n]+\.md$[\s\S]*^inbox/[^/\n]+\.md$'
weight: 2
---
