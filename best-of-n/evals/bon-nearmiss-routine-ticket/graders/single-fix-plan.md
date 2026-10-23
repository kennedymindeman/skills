---
type: llm
---

The final message is a numbered plan for fixing one failing rounding test.

PASS if the plan describes a single fix path (for example reproduce the failure, change the rounding, for instance with `decimal` and ROUND_HALF_UP, then rerun the test and the suite).
FAIL if the plan launches several parallel agents or attempts on competing approaches and picks among them.
