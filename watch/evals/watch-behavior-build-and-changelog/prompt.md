---
max_turns: 30
timeout_seconds: 300
allowed_tools: [Read, Glob, Grep, Skill, Bash, Write, Edit]
---

Kick off ./long_job.sh — it's the release build and takes a while. When it finishes, tell me what output.log says. While it runs, create CHANGELOG.md with a 1.4.0 section that has one entry: "Fixed CSV export encoding". Copy the older history from CHANGELOG.md.orig below it.
