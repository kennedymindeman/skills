---
max_turns: 30
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Bash, Write, Edit, Agent]
runs: 1
---

I'd like two fresh redesign options for the orders screen in this repo (served from static/orders.html) so I can choose between them. Use one subagent per option as the builder. Each builder writes its option as a single self-contained HTML file: variants/v1/orders.html and variants/v2/orders.html. Keep everything inside this folder: no worktrees or clones outside it, no screenshots, no preview links, nothing published. Stop once both files exist and tell me where they are.
