---
max_turns: 4
timeout_seconds: 120
allowed_tools: [Read, Glob, Grep, Skill]
runs: 3
---
Ticket #42: `tests/test_invoice.py::test_rounds_half_up` fails because `invoice.total()` rounds 2.675 down to 2.67 instead of up to 2.68. Done when that test passes and the rest of the suite stays green. Don't start yet, just outline the steps you'd take to fix it as a numbered list.
