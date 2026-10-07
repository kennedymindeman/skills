---
max_turns: 20
timeout_seconds: 300
allowed_tools: [Read, Glob, Grep, Skill, Bash, Write, Edit]
---

The notes app moved to the port in site/app.env, but site/Caddyfile still proxies notes.example.test to the old one. Fix the Caddyfile; leave the wiki block alone. I keep handing Caddy changes to you, and next time I want to do this myself.
