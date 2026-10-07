---
type: regex
target: trace
# A copy would also satisfy the file_exists grader; require the source to be moved or removed. Trace-based, so it misses glob or loop moves.
pattern: '(?:\\n|(?<![\w-]))(?:mv|rm|unlink)\s(?:[^"\\\n&;|]|\\")*2026-09-10-0732-few-things\.md'
---
