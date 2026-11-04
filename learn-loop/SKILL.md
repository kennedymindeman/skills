---
name: learn-loop
description: Checks what the user already knows before teaching and offers to save learning gaps, SRS cards, and reference notes. Use before a substantive explanation (teaching a concept over several paragraphs), when an explanation shows a gap or a concept new to the user, or when the user asks what a word means while reading.
---

# Learn loop

Status updates and code reviews are not substantive explanations; skip this skill for them.

## Before explaining

Only where `~/.local/share/learn/learn.db` exists, run:

```sh
sqlite3 -readonly ~/.local/share/learn/learn.db "SELECT name, state FROM concepts"
```

Elsewhere skip this step silently.

- Concepts marked known can be skipped, but name every skip ("since you know X, ...").
- Treat learnable and unprobed concepts as not known.
- If the topic isn't in the list, say nothing about it and answer in the normal answer-first style.

## After explaining

Offer the matching saves as options in one question box when the explanation:

- shows a gap that isn't in the list: the gap to `~/inbox` (exact topic, why, and source);
- covers something probably new to the user (unprobed, learnable, or missing from the list) and likely to recur: an SRS card (prompt plus answer, drafted in the reply) to `~/inbox/learning/` until the learn app accepts cards;
- is worth keeping as reference: a `~/wiki` page.

Save only what the user picks, and say where it landed. A gap that comes up mid-debug is not automatically study material.

## Word lookups

When the user asks what a word means while reading, draft a vocab card: only the word on the front, the definition plus the source sentence on the back. Ask before saving it.
