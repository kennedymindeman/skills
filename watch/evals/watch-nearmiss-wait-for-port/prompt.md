---
max_turns: 8
timeout_seconds: 180
allowed_tools: [Read, Glob, Grep, Skill]
---

Write me a bash function wait_for_port HOST PORT TIMEOUT that polls with nc until the port accepts connections or the timeout passes, returning nonzero on timeout. I'll drop it into our CI entrypoint. Just the code in your reply.
