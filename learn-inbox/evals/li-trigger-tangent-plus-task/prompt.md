---
max_turns: 15
timeout_seconds: 240
allowed_tools: [Read, Glob, Grep, Skill, Bash, Write, Edit]
---

Side note: the free-threaded Python build keeps coming up in release notes I skim, and I should really learn how CPython runs without the GIL at some point. Anyway, the actual job: rename parse_rows to parse_records in etl.py, call site included.
