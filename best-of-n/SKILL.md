---
name: best-of-n
description: Best-of-N for agent work - several isolated attempts at one hard task, one kept. Use when asked to fan out, try several approaches, race agents, or take the best of N, or when a task with an objective check (a failing test, a reproducible bug, a benchmark) has already beaten one attempt or its stakes justify paying for several. Load it before outlining or dispatching the attempts.
---

More attempts raise the odds that one of them is right; picking it is the hard part. So **selection** carries this skill: tests filter, then a blind reviewer picks by running the candidates, never by reading their style. Each attempt follows a different **plan**, because N copies of one brief tend to fail the same way. Routine tickets go through one builder; best-of-n costs about N times the tokens.

You are the orchestrator. Builders and the reviewer are subagents; you hold the briefs, the label key, and the final call.

## 1. Pin the task and the check

Write down, once:

- **Task** - the change, in one line, plus the ticket if there is one.
- **Acceptance check** - one command that exits 0 on success, such as a test file, a repro script, or a benchmark with a threshold. Confirm it fails on `origin/main` now. A check that already passes selects nothing.
- **Slug** - `issue-<N>` with a ticket, otherwise a short name. Branches are `agent/issue-<N>-try-<K>`, or `best-of/<slug>-<K>` without a ticket.

For a non-code task (a design, research, a plan), the acceptance check is a written rubric the reviewer scores against.

## 2. Write N briefs, one plan each

N is 3 by default and at most 5. Every brief shares the task, the acceptance check, and the base commit word for word, and commits to a **different named plan**: a different algorithm, layer, library, or point of attack. Name the plans to yourself first; when two would land as the same diff, replace one.

Each brief is a builder brief (the `frontier` skill's cage works as a template) plus these lines:

```
Plan: <one paragraph naming the approach. Commit to it; if it proves unworkable, report status: blocked with why rather than switching plans>.
Branch: you start in an isolated worktree. Run `git switch -c <branch>` there, commit your work, and stop. Do not push or open a PR.
Commit messages: describe the change; leave the plan name out of them.
Done when: `<acceptance check>` exits 0 in your worktree. Quote its output.
```

A brief never mentions the other attempts, their plans, or their branches.

## 3. Dispatch the builders

`cd` to the target repo first: `isolation: worktree` makes its worktree from the Bash working directory. Then send every builder in one message, one Agent call each:

```
Agent({
  description: "best-of <slug> try <K>",
  subagent_type: "builder",
  isolation: "worktree",
  run_in_background: true,
  prompt: "<brief K>"
})
```

Keep working while they run. Each completion notification carries the agent's worktree path, its report, and its token usage; record all three per attempt.

## 4. Filter by the check

For each attempt that reports a commit, run the acceptance check yourself in its worktree, plus the repo's own test suite. The builder's quoted output is a claim; your run is the filter. Drop every candidate that fails or reported `blocked`.

- No candidate passes: skip to step 7 and report each attempt's plan and failure output. Stop there.
- One passes: it is the winner. Skip to step 6.
- Two or more pass: go to step 5.

## 5. Anonymize, shuffle, and pick

The reviewer must not know which plan produced which candidate, and labels must not track try numbers. Shuffle the passing branches onto letters and keep the key with you:

```
python3 -c 'import random,sys; b=sys.argv[1:]; random.shuffle(b); [print(chr(65+i), x) for i, x in enumerate(b)]' <passing branches>
```

Redirect that output to the key file, `~/worktrees/<repo>-best-of-<slug>/key.txt`, outside every candidate checkout. For each line, make a detached checkout under a neutral path:

```
git worktree add --detach ~/worktrees/<repo>-best-of-<slug>/<letter> <branch>
```

Dispatch one reviewer:

```
Agent({
  description: "best-of <slug> blind pick",
  subagent_type: "reviewer",
  run_in_background: true,
  prompt: "<reviewer brief>"
})
```

The reviewer brief holds the task line, the acceptance criteria, the base commit, and the candidate paths by letter. It omits plan names, branch names, try numbers, and builder reports. It asks for this:

```
Candidates A, B, C each implement the task above and each pass `<acceptance check>`. Compare them pairwise (A vs B, A vs C, B vs C). Ground every call in execution: run the tests, and write inputs that tell the candidates apart, such as edge cases, malformed input, scale, or concurrency, into a scratch directory under /tmp, then run each candidate on them. Read `git diff <base>` in each candidate directory; leave `git log` and `git branch` unread. Prefer the candidate that is correct on more of your inputs, then the one with the smaller and simpler change.

Report:
- winner: <letter>
- each pairwise call, with the commands you ran and what they showed
- ideas worth porting: each as "<letter>: <specific idea> - <why it helps the winner>", or "none"
```

Map the winning letter back through the key only after the report arrives.

## 6. Combine

The winner's branch is the base. Patches are never blended. Each idea worth porting that you accept becomes one follow-up `builder` on the winner's branch (no `isolation`; the brief names the winner's worktree path and branch), whose brief names the idea, the loser path it comes from, and the acceptance check that must still pass. Rerun the check yourself after each port.

A non-code task may instead end in one synthesis that takes the best parts of each candidate, written by you or one builder.

Open the PR from the winner's branch the usual way (repo PR rules, `frontier` merge queue under a run).

## 7. Report, then clean up

Report, in this order:

- each attempt: its plan, pass or fail (with the failing output's key line), and its token usage from the completion notification;
- the reviewer's pairwise calls and reasoning, letters mapped back to plans;
- which ideas were ported and which were declined, and why;
- the winner's branch or PR URL, and the total tokens across all agents.

After the report, remove every losing worktree and branch and the letter checkouts, one command per call:

```
git worktree remove --force <path>
git -C <repo> branch -D <losing branch>
```

The winner's branch stays until its PR lands.
