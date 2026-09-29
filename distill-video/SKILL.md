---
name: distill-video
description: Turns a video link into a one- or two-sentence thesis, timestamped evidence, and a Q&A run off the transcript. Use when asked to explain, summarize, or pull the argument out of a YouTube link; when the user says they don't want to watch the whole thing; when a video spends an hour restating one claim; and when a follow-up question about a video needs an answer citing where in the video it was said.
---

A talking-head video is a **restatement machine**: one claim, made at 0:40, re-made in different words at 4:10, 12:55, and 31:20, with the actual support buried in two of those passes. Watching it end to end pays full price for the repetition. The transcript collapses it - the claim stated once, each distinct piece of support linked to the second it lands, and every follow-up answered from the text instead of a rewatch.

So the output is never a running summary of the video in order. It is a **thesis** plus the evidence that carries it, and then a back-and-forth.

## Get the transcript

`fetch-media` owns the recipe and the pitfalls. Use it; do not fetch the watch page.

The video ID is the `v=` parameter, the `youtu.be/` path segment, or the `/shorts/` segment. Keep it in hand: every link you emit is built from it.

## Build the timestamp index

The transcript comes back as a Python list of per-video lists; each inner list is the `{'start', 'duration', 'text'}` cues, a few seconds long each and cut mid-sentence. That shape is the index:

- A quotable passage is several consecutive cues joined; its timestamp is the `start` of its **first** cue.
- A link is `https://youtu.be/<ID>?t=<SECONDS>`, seconds as an integer. Floor it and back off two or three seconds so the quote starts after the link, not before it.
- On a long video, pipe the transcript to a file and grep it rather than holding the whole thing in context.

Read the whole transcript once before writing anything. The thesis is usually stated near the start and again near the end, and the strongest support is rarely near either.

## State the thesis

One or two sentences, in the speaker's terms, naming what they claim and what they claim it against. Link it to where they state it most plainly - which is often not the first time they say it.

When the video has no thesis - a news roundup, a stream of unconnected demos - say that in one line and give the evidence section as a list of items instead. Manufacturing an argument that isn't there is the failure mode.

## List the evidence

Each distinct piece of support gets one bullet: what it establishes, in your words, then the link.

```markdown
- Cold starts dominate the latency budget: he traces one request end to end and 380ms of the 500ms is process boot ([12:04](https://youtu.be/0oXOOlqVu5M?t=721)).
```

Quote verbatim when the wording is the point - a number, a concession, a claim the speaker will be held to. Paraphrase otherwise.

Order by weight, strongest first, not by when it appears. A benchmark, a demo, a document, or a conceded counterexample outranks an assertion repeated with more conviction.

## Collapse repetition

Restatements are the bulk of most videos, and they get grouped rather than listed:

- Group every passage making the **same claim** into one bullet, however far apart they sit.
- Cite two timestamps at most: the **first** occurrence, where the claim is introduced, and the **strongest**, where it is actually argued with a fact, a demo, or a number. Drop the rest silently.
- A restatement that adds a new fact is not a restatement - it is its own bullet.
- When the repetition is itself the finding, say so with a count instead of bullets: "argues this six times between 8:00 and 41:00, with no new support after [14:12](https://youtu.be/0oXOOlqVu5M?t=850)."

The bar: no two bullets in the list assert the same thing.

## Answer follow-ups

The transcript stays available for the back-and-forth - that is the point of the skill, and the user will keep asking. Each answer carries a timestamped quote so it can be checked against the video:

> "we never got it under three hundred milliseconds" - [23:41](https://youtu.be/0oXOOlqVu5M?t=1419)

Grep the transcript for the question's terms and their synonyms before answering. When the transcript does not cover it, say so in one plain line - "he doesn't say", "not in the video" - and then either answer from your own knowledge, marked as coming from outside the video, or name what would answer it. An inferred answer sitting unmarked next to timestamped quotes is what breaks trust in every other line.

Two follow-ups are off the transcript entirely:

- **What was on screen** - a diagram, a benchmark table, a snippet the speaker talks around without reading out. `fetch-media` storyboards find the moment, then a full-resolution slice reads it.
- **What the comments say** - outside this skill; no skill carries a YouTube-comments recipe.

## Delegating

A subagent sent at a video watches it, or paraphrases the transcript into a running summary. Put the shape in the brief - thesis, weighted evidence with `youtu.be/ID?t=SECONDS` links, repetition collapsed - plus the `fetch-media` pointer for the transcript command.
