---
max_turns: 8
timeout_seconds: 180
allowed_tools: [Read, Glob, Grep, Skill]
---

In my aiohttp handler I call time.sleep(5) to wait for a rate limit, and every other request stalls while it sleeps. Why does that happen, and what should I use instead?
