---
type: regex
target: {source: file, path: learn-sandbox/inbox.jsonl}
pattern: '"topic":\s*"(?:[^"\\]|\\.)*(?:slow[- ]start|congestion)'
flags: i
weight: 2
---
