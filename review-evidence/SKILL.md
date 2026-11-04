---
name: review-evidence
description: Records the evidence a review needs for a change. Use when preparing a PR or review for changed interactions, layout, backend work, a PreToolUse or PostToolUse hook, a UI change in an app, or a change to how a list moves (collapse, reorder, insert, scroll anchoring).
---

# Review evidence

Every piece of evidence names the tested commit, any uncommitted changes, and whether the run used synthetic or live data.

## By kind of change

- **Changed interactions.** Record a short passing flow: the steps, a final screenshot, the tested commit, synthetic or live data.
- **Layout changes.** Compare screenshots at the same viewport.
- **Backend work.** Keep the relevant test output.
- **A hook that runs on every tool call (PreToolUse/PostToolUse).** Before merging, replay the last week of real tool calls from the `~/.claude/projects` transcripts through it. Report how many calls it would block and the top reasons. Keep the replay script next to the hook's tests.
- **UI changes in an app.** In the simulator, screenshot every state of each changed control (empty, focused, typed, cleared and retyped, stepped, done, carried, relaunched). Lay the shots side by side before shipping. When a state is wrong, also record a short video of the steps that cause it.
- **List motion** (collapse, reorder, insert, scroll anchoring). Record a screen video of the real flow on each device size and judge it from the video. Screenshots and logged offsets can't show a jump.

## Keeping it

Keep videos and traces in the approved artifact location and link them from the review. Keep source history in Git. When the code behind recorded behavior changes, record that behavior again.
