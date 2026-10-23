---
max_turns: 6
timeout_seconds: 180
allowed_tools: [Read, Glob, Grep, Skill]
runs: 2
---
The date parser in our Python service still fails `tests/test_parse_dates.py::test_ambiguous_formats` after one agent's fix attempt. Fan out a few agents on it, try several approaches, and keep the best result. Don't start anything yet, just outline the steps you'd take as a numbered list.
