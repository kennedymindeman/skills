---
name: triage
description: Empties ~/inbox by routing each captured thought to its destination, one approved decision at a time. Use on /triage or when asked to process, clear, or zero the inbox.
---

Capture is cheap because it defers every decision; triage is the session where those decisions are paid. One promise keeps the habit alive and is yours to hold in either mode: nothing is lost. Routing a thought to the wrong place quietly is how an inbox stops being trusted, and an untrusted inbox stops being used.

This skill runs two ways. **Interactive mode** is the default: the user asks, and nothing moves without their approval - the whole of this document below the routing table describes it. **Autonomous mode** is the scheduled background job described in its own section at the end; it earns trust by logging every decision and leaving the archive and git history intact, not by asking. Neither mode runs as an unrequested favour at the end of some other task.

## Read everything before asking anything

Read every file in `~/inbox/` - the body, not the filename - and what is already sitting in `~/inbox/someday/`, which is re-offered every pass. Then cluster, before a single question goes out:

- Duplicates and near-duplicates of one thought become **one** question and one routing; the extra files are archived alongside it.
- A single file may hold several unrelated items. `dump` writes one file per message on purpose, mixed topics and all, because splitting is a categorization and categorization is this session's job. **Split it before asking anything**: one new inbox file per item, the original's frontmatter copied and the item's text verbatim, then archive the original. Each piece is routed from there like any other file - routing is per file, so items that will end up in different places need to be different files first.
- Items that only make sense together - a task and the constraint on it - go to one destination as one artifact.

An inbox holding no dumps is a two-line report: nothing to triage, and here is what is still in `someday/`.

## Route in batches, recommended first

Every routing is a question to the user through **AskUserQuestion**. This is the user's standing house style rather than a rule of this skill, so it holds even when the answer looks obvious:

- One question per item, **at most four items per call**, and hold the rest until that batch comes back. A long list of open items is more overwhelming than one question with concrete answers.
- **Recommended destination first, marked "(Recommended)"**, then the genuinely distinct alternatives - don't compress six real options down to two.
- Phrase options in the user's words for the item, not vocabulary you coined while reading it, and carry the item's gist in the question so the user doesn't have to reopen the file.
- Expect "Other" as a common answer, not a failure of the option set. When the destination is genuinely unpredictable, ask open-ended instead of guessing four wrong options.
- Report first, then ask. Routing questions never arrive buried at the end of a status summary.

## Routing table

| Destination | What executing it means |
| --- | --- |
| Learning interest | One item per topic in the learn app's learning inbox, captured the way the `learn-inbox` skill does it (`learn inbox capture "<topic>" --why ... --source ...`; on the mini, the JSON-stdin form), carrying the dump's motivation and source context. |
| Project task or idea | A GitHub issue in the relevant repo, via `gh issue create`. When the repo isn't obvious, which repo is part of the question. |
| Durable machine or infra fact | The host's page in `~/wiki`, plus an append to `~/wiki/log.md`. |
| Do now | Done inside this session - the two-minute rule. Anything longer is a project task. |
| Someday/maybe | Moved to `~/inbox/someday/`, re-offered at the next pass. |
| Drop | Nothing downstream. |

What lands downstream stays neutral: the learning inbox holds the interest, not lessons or SRS cards; the wiki holds the fact, not your reading of it. Each of those systems decides for itself what to do with what it is handed.

## Execute, archive, commit

Execute only what the user accepted, then move every processed file - drops included - into `~/inbox/archive/`:

```
mv ~/inbox/2026-08-13-2341-srs-grader-latency.md ~/inbox/archive/
```

Plain `mv`, not `git mv` - a fresh dump is untracked until this pass commits it, and `git mv` refuses to move what git doesn't know about yet.

Drop is a destination like any other: no downstream artifact, and the file still archives. The archive and the inbox's git history are the whole promise that capture is safe, and keeping a dead file costs nothing. Deferred items move to `someday/` the same way. Then commit the inbox once, for the pass rather than per file:

```
git -C ~/inbox add -A && git -C ~/inbox commit -m "Triage: 9 routed, 2 someday"
```

`dump` leaves what it writes uncommitted, so expect untracked files at the start of the pass - this commit is what records the dumps as well as what empties them. `add -A` takes every inbox file, so an item still sitting in the inbox root because its question went unanswered is committed too, and stops being untracked work the next pass could lose.

## End at inbox zero

`~/inbox/` finishes the pass holding nothing but `README.md`, `archive/`, and `someday/`. Close with one paragraph: how many items went where, what was done in-session, and what is now waiting in `someday/`. An item whose question the user left unanswered is the one permitted exception - it stays in the inbox root, committed with the pass, named in the summary, and is the first thing the next pass asks about.

## Autonomous mode

The scheduled runner `auto-triage.sh` invokes this mode headless on Fable, hourly, only when the inbox root holds a dump. It reuses everything above - read bodies not filenames, split multi-item files, cluster duplicates - with two differences: no question is ever asked, and every decision is written to `~/inbox/auto-triage.log` instead. The runner passes one argument, `dry-run` or `execute`.

Where interactive mode would call **AskUserQuestion**, decide yourself and take the recommended destination. The approval gate is replaced by three rules that keep a wrong guess cheap:

- **Confident routes go through.** A clear learning interest, an obvious project task, a plain infra fact - route it.
- **Genuinely ambiguous items stay put.** When interactive mode would ask open-ended because the destination is unpredictable, do not guess. Leave the file in the inbox root, unrouted, and log it as deferred. It is the first thing the next interactive pass sees, exactly like an unanswered question. Deferring is bounded: after the fifth defer the runner moves the file to `someday/` and logs it as `PARKED`, so an item no autonomous pass can decide leaves the hourly defer loop and waits in `someday/` for a person instead. The count restarts from that `PARKED` line, so a file moved back to the inbox root by hand keeps its full budget.
- **Never drop autonomously.** "Drop" is a human decision. An item you would drop goes to `someday/` instead, so nothing leaves without a person having seen it.

Each log line is one item: `ISO-timestamp  source-basename  ->  destination  (one-line reason)` - the bare filename, never a path, because the runner's park bound counts defers by matching that basename. For a split, log each piece. For a deferred item, the destination is `DEFER` and the reason says why.

**dry-run:** do the full read/split/cluster/decide pass and append every decision to `auto-triage.log`. Execute nothing, create nothing, archive nothing, commit nothing. The split files you would have written are described in the log, not written to disk. This is the mode to run for the first days, so the routing can be audited against the log before it acts.

**execute:** carry out the decisions using the routing table and the *Execute, archive, commit* section above - create the artifacts, move processed files to `archive/`, move deferred items' peers to `someday/`, and commit the inbox once with a message naming the counts. Then append a final summary line to `auto-triage.log`. Deferred items stay in the inbox root, committed with the pass.

The runner calls Claude with `--model claude-fable-5` and no fallback model. If Fable is out of usage the run fails without downgrading, and the wrapper records the skip in `auto-triage-runs.log` and starts a six-hour cooldown - the hourly runs in between exit immediately instead of burning another failed call. Each run is also capped by a wall-clock timeout, so a hung call ends that run rather than the hour.
