---
type: llm
weight: 2
---

The final message is a numbered plan for running several agents on one failing test and keeping the best result.

PASS if the plan does all of these: (1) each agent works in its own isolated checkout or branch and is given a different approach or plan, not the same brief repeated; (2) candidates are filtered by running the failing test or acceptance check, dropping the ones that fail; (3) when more than one passes, the choice is made by a reviewer who sees the candidates under neutral labels (letters or similar) without knowing which approach or agent produced each; and (4) one candidate is kept as the winner, with any idea from the others ported onto it afterwards rather than merging or blending the patches together.
FAIL if any of the four is missing.
