---
type: regex
target: trace
# A copy would also satisfy the file_exists grader; require the source to be moved or removed. Trace-based, so it misses glob or loop moves.
pattern: '(?:\\n|(?<![\w-]))(?:mv|rm|unlink)\s(?:[^"\\\n&;|]|\\")*2026-09-02-0815-parking-permit\.md'
---
