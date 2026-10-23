---
name: best-of-n
description: Best-of-N for agent work - several isolated attempts at one hard task, one kept. Use when asked to fan out, try several approaches, race agents, or take the best of N, or when a task with an objective check (a failing test, a reproducible bug, a benchmark) has already beaten one attempt or its stakes justify paying for several. Load it before outlining or dispatching the attempts.
---

More attempts raise the odds that one of them is right; picking it is the hard part. So **selection** carries this skill: tests filter, then a blind reviewer picks by running the candidates, never by reading their style. Each attempt follows a different **plan**, because N copies of one brief tend to fail the same way. Routine tickets go through one builder; best-of-n costs about N times the tokens.

You are the orchestrator. Builders and the reviewer are subagents; you hold the briefs, the label key, and the final call.

## 1. Pin the task and the check

Write down, once:

- **Task** - the change, in one line, plus the ticket if there is one.
- **Acceptance check** - one command that exits 0 on success, such as a test file, a repro script, or a benchmark with a threshold. A check that already passes selects nothing.
- **Base** - the commit every attempt starts from, with the check's files committed in it, pushed, and its full SHA written down. Confirm the check fails at the base. `isolation: worktree` starts each builder from the remote's default branch, not from your checkout, so each builder moves itself onto the base (step 2).
- **Slug** - `issue-<N>` with a ticket, otherwise a short name. Branches are `agent/issue-<N>-try-<K>`, or `best-of/<slug>-<K>` without a ticket.

For a non-code task (a design, research, a plan), the acceptance check is a written rubric the reviewer scores against.

## 2. Write N briefs, one plan each

N is 3 by default and at most 5. Every brief shares the task, the acceptance check, and the base commit word for word, and commits to a **different named plan**: a different algorithm, layer, library, or point of attack. Name the plans to yourself first; when two would land as the same diff, replace one.

Each brief is a builder brief built on the `frontier` skill's cage, including its command discipline (one command per Bash call: the worktree isolation guard refuses compound commands), plus these lines:

```
Plan: <one paragraph naming the approach. Commit to it; if it proves unworkable, report status: blocked with why rather than switching plans>.
Branch: you start in an isolated worktree on a harness branch. Before any edit, run each as its own call: `git branch -m <branch>`, then `git reset --hard <base SHA>`, then `git rev-parse HEAD`. Stop and report if HEAD is not <base SHA>. Commit your work on <branch> and stop. Do not push or open a PR.
Scope: your worktree only. Leave every other branch, worktree, and `.claude/worktrees/` entry unread.
Commit messages: describe the change; leave the plan name out of them.
Done when: `<acceptance check>` exits 0 in your worktree. Quote its output, and report your worktree path and branch name.
```

The rename keeps the harness from leaving a stray `worktree-agent-<id>` branch behind.

A brief never mentions the other attempts, their plans, or their branches.

## 3. Dispatch the builders

`cd` to the target repo first: `isolation: worktree` makes its worktree from the Bash working directory. The repo must sit inside the session's allowed working directories (the launch directory or an added one); otherwise Claude Code resets the cwd after the `cd`, and every worktree comes from the wrong repo. Run `pwd` to confirm the `cd` held. Then send every builder in one message, one Agent call each:

```
Agent({
  description: "best-of <slug> try <K>",
  subagent_type: "builder",
  isolation: "worktree",
  run_in_background: true,
  prompt: "<brief K>"
})
```

Keep working while they run. Each completion notification carries the agent's worktree path, its report, and its token usage; record all three per attempt. Its `worktreeBranch` may still name the harness branch, so record the branch name the builder reports.

## 4. Filter by the check

For each attempt that reports a commit, run the acceptance check yourself in its worktree, plus the repo's own test suite. The builder's quoted output is a claim; your run is the filter. Drop every candidate that fails or reported `blocked`.

- No candidate passes: skip to step 7 and report each attempt's plan and failure output. Stop there.
- One passes: it is the winner. Skip to step 6.
- Two or more pass: go to step 5.

## 5. Anonymize, shuffle, and pick

The reviewer must not know which plan produced which candidate, and labels must not track try numbers or branch names. Run `mkdir -p ~/scratch/best-of-keys`, then shuffle the passing branches onto letters, redirecting the output to the key file `~/scratch/best-of-keys/<slug>.txt`. The key lives outside every directory the reviewer is pointed at.

```
python3 -c 'import random,sys; b=sys.argv[1:]; random.shuffle(b); [print(chr(65+i), x) for i, x in enumerate(b)]' <passing branches>
```

For each line, export the candidate as a fresh repo with two commits, `base` and `candidate`, and no branches, remotes, or reflog from the source repo. A worktree or clone would carry the branch names. Run each as its own call, with `D=~/worktrees/<repo>-best-of-<slug>/<letter>`:

```
mkdir -p $D
git -C <repo> archive <base SHA> | tar -x -C $D
git -C $D init -q
git -C $D add -A
git -C $D commit -qm base
git -C <repo> diff --binary <base SHA> <branch> | git -C $D apply
git -C $D add -A
git -C $D commit -qm candidate
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

The reviewer brief holds the task line, the acceptance criteria, and the candidate paths by letter. It omits plan names, branch names, try numbers, and builder reports. It asks for this:

```
Candidates A, B, C each implement the task above and each pass `<acceptance check>`. Compare them pairwise (A vs B, A vs C, B vs C). Ground every call in execution: run the tests, and write inputs that tell the candidates apart, such as edge cases, malformed input, scale, or concurrency, into `/tmp/best-of-<slug>-review/`, then run each candidate on them. Read `git diff HEAD~1` in each candidate directory for its change. Prefer the candidate that is correct on more of your inputs, then the one with the smaller and simpler change.

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

After the report, clean up, one command per call:

```
git worktree remove --force <losing worktree path>
git -C <repo> branch -D <losing branch>
rm -rf ~/worktrees/<repo>-best-of-<slug>
rm -f ~/scratch/best-of-keys/<slug>.txt
rm -rf /tmp/best-of-<slug>-review
```

Also delete any `worktree-agent-*` branch an attempt left behind because it never ran the rename (`git -C <repo> branch --list 'worktree-agent-*'`). The winner's worktree and branch stay until its PR lands. Then remove them the same way.
