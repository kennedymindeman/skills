---
name: learn-inbox
description: Captures a topic, or the work an agent just finished, to the learn app's learning inbox without enrolling in anything. Use on "add that to my learning inbox", "I should learn X", "I want to learn to do this myself", "next time I'll do it", "teach me this later", "capture this for learn", `learn inbox capture`, the retired ~/learning/queue; when a topic surfaces mid-conversation and how to learn it is undecided; and after finishing a task the user flagged as one to learn, or one they keep delegating (git surgery, launchd, Caddy, DNS, uv packaging), firing once the work is done, never in the middle of it; and on "digest this chat into learn", one item per concept the conversation taught.
---

Wanting to learn something and choosing how to learn it are two decisions, and the second one is expensive: a mission is a teaching engagement, an SRS card is a lifetime of reviews. The learning inbox exists so the first decision can be recorded on its own - one intent, filed, committing the user to nothing. So capture is a single call that writes a row and returns to the task, and every question about what to do with the topic is left for the review page, later.

## File the item

An inbox item is a topic plus the motivation behind it and the source material to ground it later. From the laptop, one command:

```
learn inbox capture "<topic>" --why "<motivation>" --source "<context>"
```

The database lives on the mini, so that command hands the payload over ssh. Run `hostname` when it matters: on the mini itself, run the mini-side half directly in the repo, with the same payload as JSON on stdin.

```
cd ~/projects/learn && echo '{"topic": "...", "motivation": "...", "source_material": "..."}' | uv run learn _inbox-capture
```

Both write the same row; only the first form prints a confirmation. In the JSON form, line breaks inside a field go in as `\n` escapes (written `\\n` inside the single-quoted `echo`) - a raw newline in a JSON string is a parse error, and the payload is rejected whole. `--why` and `--source` are optional, but an item with neither is a topic with no reason and nothing to start from - fill them from the conversation that produced the topic: why it came up, and the link, file, or transcript it came from. That material is already in hand, so filling them costs nothing. Asking for them does not: an interview about a topic the user mentioned in passing is the conversation capture is meant to defer.

Then one line back naming what was filed, and on with what the session was doing.

To digest a whole conversation into learn, one item per concept, read digest.md.

## Hand off work the user wants to do themselves

Some items come from a task the agent just did and the user wants in their own hands next time - they said so, or it is one of the jobs they keep delegating. Filing it is the same call, with one difference: the source material is the work itself, so the app teaches from what actually happened instead of researching the topic from scratch.

Finish the job first. The hand-off is the last thing in the turn, after the work is done and reported; a task suspended to file an inbox item is the work the user actually asked for, delayed.

Then fill the same three fields, aimed at the capability rather than the topic:

- **topic** - the thing they want to be able to do, in their hands: "rebase a stack of branches after a squash-merge", not "git rebase".
- **`--why`** - why they want to do it themselves: what they were blocked on, how often it comes up, what delegating it costs them.
- **`--source`** - the artifact below.

The artifact is a self-contained record of the run, around 2 KB, in four parts:

```
commands: the calls that mattered, in order, with the flags that made them work
changed: path - what changed there and why (the intent, not the diff)
why it worked: one paragraph of the reasoning the commands don't show - the situation,
  the approach picked over the alternative, the gotcha that decided it
done when: one checkable sentence, phrased as something they do and can verify
```

The cap does the editing: keep what a reader could not reconstruct - the reasoning, the gotcha, the order - and leave out the transcript, the full diff, and output a rerun would print again. The `done when:` line is the one to labour over: learn's mission machinery reads it as a practicum criterion, so it has to name an outcome that can be checked rather than a feeling of understanding.

## Capture commits to nothing

Capturing never enrolls the user in anything. The item sits in the inbox as a suggestion until they act on it, and nothing else is set in motion on the way in - no SRS cards drafted from the topic or the artifact, no mission started, no wiki page written, no digest requested. Starting a mission from an item, or declining it, is what consumes it, and both are the user's call on the review page.

That neutrality is what makes unprompted capture safe. When a topic surfaces mid-conversation and how to learn it is undecided, file it and say so rather than asking whether to; an unwanted item costs one line to decline, while the ask costs the thread. Capture never stands in for work the user actually asked for - when a message mixes a learning tangent with a real instruction, file the tangent and carry out the instruction.

## Use the inbox's words

`~/projects/learn/CONTEXT.md` is the learn app's glossary and the reference for this vocabulary; read it before writing anything the user reads about the inbox. The terms that come up at capture time:

- **Learning inbox** - the app-owned list of captured intents. Not a queue: `~/learning/queue/` is retired, and the word went with it.
- **Inbox item** - one captured intent. Not a card candidate; a captured topic may never become a card.
- **Consumed** - an item's exit, by a mission started from it or an explicit decline.
- **Digest** - background enrichment that maps an item into the concept graph and leaves it in the inbox.
- **Mission** - the teaching engagement an item can become. Not a course or a workspace.
