---
name: dump
description: Captures a thought verbatim to ~/inbox without derailing the current task. Use on /dump, "brain dump", "capture this", "park this", "note for later", or when a mid-task message becomes an unstructured mix of ideas that belongs to no project.
---

A thought arriving mid-task is cheap to keep and expensive to process, and processing is what loses it: the moment capture asks a question it has become a conversation, and the session it interrupted is already derailed. So there is one move here - the thought goes to disk in the user's own words, and the task resumes in the same turn. Everything a dump might deserve (routing, tagging, next steps) belongs to triage, later, deliberately.

## Write the file

One markdown file per dump, in `~/inbox/`:

```
~/inbox/2026-08-13-2341-srs-grader-latency.md
```

The stamp is `date +%Y-%m-%d-%H%M`; the slug is the first three to five words of the dump, lowercased and hyphenated with punctuation dropped. Never ask about the name - check only whether that filename is taken, and suffix `-2` (then `-3`, `-4`, ...) if it is.

Frontmatter carries two keys and no others. Both are already in hand, and neither is a judgment about the content:

```markdown
---
captured: 2026-08-13T23:41
source: mid-session tangent while debugging the learn-web SRS page
---
<the dump, verbatim>
```

`source` is one line of session context - what was going on when it arrived, not what the dump is about. The body is the dump verbatim: the user's words, their order, their typos, no cleanup, no headings imposed on it.

One message is one file even when it mixes five unrelated topics. Splitting it is already a categorization, and triage clusters better with the whole message in front of it.

Otherwise leave the inbox alone: don't edit or reorder files already there, and don't commit. Dumps sit uncommitted in the inbox repo; triage commits them when it processes them.

## Ask nothing, add nothing

Between reading the dump and acknowledging it, all of this is forbidden: clarifying questions, categories, tags, rewriting or summarizing, proposed next steps, an opinion on the idea, and reading the inbox to see whether the thought duplicates something already there - the only permitted look at the directory is the mechanical filename-collision check. Any of them turns a two-second capture into the conversation the dump was meant to defer.

Then one line back, naming the file, and straight on with what the session was doing:

> Captured to inbox: `2026-08-13-2341-srs-grader-latency.md`. Back to the grader timeout - 

When a message mixes a tangent with a real instruction about the current task, capture the tangent and carry out the instruction. Capture never stands in for work the user actually asked for.

## Capture unprompted

Capturing on the user's behalf is allowed and expected: when a mid-task message veers into a tangent without asking for anything, write the file and steer back rather than following it. Verbatim capture is non-destructive and reversible - an unwanted file costs one line at triage, while the tangent costs the session.

Don't offer first. "Want me to capture that?" is precisely the question this skill exists to avoid; capture, then say so.

## Leave triage for triage

The inbox is emptied later by the `triage` skill's deliberate pass, which owns every routing decision, so no dump is ever sent straight to its apparent destination on the way in: a guess about where a half-formed thought belongs is worth less than the thirty seconds it saves, and being wrong quietly is how an inbox stops being trusted.
