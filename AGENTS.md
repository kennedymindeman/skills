# writingSkills
Before writing or editing any skill in this repo, load the `mattpocock-skills:writing-for-agents` skill (plugin-namespaced) — it owns the method (pointers, disclosure, leading words, pruning) and its `SKILL-MECHANICS.md` owns the model-vs-user invocation choice. This file adds only skill-authoring facts and repo conventions that skill doesn't carry.

# description
Write what-plus-when in third person: one short clause naming what the skill does, then "Use when …" trigger clauses carrying the concrete phrases, symptoms, and command names that should fire it. Never summarize the skill's step sequence in the description — agents follow the summary instead of reading the body (documented failure: a description saying "code review between tasks" produced one review where the body's flowchart required two; obra/superpowers). Hard cap 1024 characters; aim under 500. Describe the problem, not tool-specific symptoms.

# naming
Lowercase letters, numbers, hyphens; 64 characters max; "claude" and "anthropic" are reserved. Verb-first or gerund where natural (`creating-skills`), a concrete noun otherwise (`frontier`); never `helper`/`utils`/`tools`. Keep one pattern across the collection.

# body
Target 50–200 lines, readable in 90 seconds; the official ceiling is 500 lines (~5k tokens loaded on trigger). Split heavy reference (100+ lines) into a sibling file exactly one level deep from SKILL.md, with a table of contents past 100 lines; keep principles and short code patterns inline. No time-sensitive content, and one term per concept throughout.

# testing
Baseline a new skill before shipping it: in a fresh session, pose a task the skill should catch, and watch what happens without the skill — that gap is what the skill must change. Then confirm the skill actually fires on the trigger phrases in its description. There is no official evaluator; this manual check is the floor.

# repoConventions
Skills are real directories at the repo root and are installed into each harness after merge. Harness registration is machine state, never part of a PR. Use the `skills` installer for cross-agent skills. Update README's Skills section in the same change that adds or retires a skill. This repo is public: effort planning (wayfinder maps, decision tickets) lives in the private `kennedymindeman/dotfiles` GitHub Issues under the `skills` label, and personal data stays in `~/wiki`, `~/inbox`, and `~/journal`, referenced by path only. Fork a third-party skill into this repo only when it needs local modification; otherwise install it from upstream through the harness's plugin or skill installer.
