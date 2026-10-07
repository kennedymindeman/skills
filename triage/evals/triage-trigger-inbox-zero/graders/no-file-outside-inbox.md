---
type: regex
target: files
flags: m
match: not_contains
# Routing before approval would create files outside inbox/ or in someday/.
pattern: '^(?!inbox/).+|^inbox/someday/'
---
