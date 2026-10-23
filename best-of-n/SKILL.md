---
name: best-of-n
description: Best-of-N for agent work - several isolated attempts at one hard task, one kept. Use when asked to fan out, try several approaches, race agents, or take the best of N, or when a task with an objective check (a failing test, a reproducible bug, a benchmark) has already beaten one attempt or its stakes justify paying for several. Load it before outlining or dispatching the attempts.
---

More attempts raise the odds that one of them is right; picking it is the hard part. So **selection** carries this skill: tests filter, then a blind reviewer picks by running the candidates, never by reading their style. Each attempt follows a different **plan**, because N copies of one brief tend to fail the same way. Routine tickets go through one builder; best-of-n costs about N times the tokens.

You are the orchestrator. Builders and the reviewer are subagents; you hold the briefs, the label key, and the final call. Every command below is one Bash call; `<angle brackets>` are literal paths or names you substitute, since shell variables don't survive between calls.

## 1. Pin the task and the check

Write down, once:

- **Task** - the change, in one line, plus the ticket if there is one.
- **Acceptance check** - one command that exits 0 on success, such as a test file, a repro script, or a benchmark with a threshold. A check that already passes selects nothing.
- **Base** - the full SHA every attempt starts from, with the check's files committed in it. Confirm the check fails at the base. Commit a new failing test on a local branch (`best-of/<slug>-base`); it needs no push, since worktrees share the repo's objects, and a deliberately failing check never goes to the default branch.
- **Slug** - `issue-<N>` with a ticket, otherwise a short name. Branches are `agent/issue-<N>-try-<K>`, or `best-of/<slug>-<K>` without a ticket.
- **Letters directory** - `<letters>`, where step 5 puts the blind copies: inside one of the session's allowed working directories, outside the repo, such as `~/worktrees/<repo>-best-of-<slug>` when `~/worktrees` is allowed.

For a non-code task (a design, research, a plan), the acceptance check is a written rubric the reviewer scores against.

## 2. Write N briefs, one plan each

N is 3 by default and at most 5. Every brief shares the task, the acceptance check, and the base SHA word for word, and commits to a **different named plan**: a different algorithm, layer, library, or point of attack. Name the plans to yourself first; when two would land as the same diff, replace one.

Each brief is the `frontier` skill's cage, including its one-command-per-call discipline (the worktree isolation guard refuses compound commands). Three cage lines change: its `Base:` line gives way to the Branch line below, and the builder reports in its reply rather than opening a PR, so the PR link and Validation-in-PR lines drop. Add these lines:

```
Plan: <one paragraph naming the approach. Commit to it; if it proves unworkable, report status: blocked with why rather than switching plans>.
Branch: you start in an isolated worktree on a harness branch. Before any edit, run each as its own call: `git branch --show-current` (note the name), `git switch -C <branch> <base SHA>`, then `git branch -D <the noted name>` only if it starts with `worktree-agent-`, then `git rev-parse HEAD`. Stop and report if HEAD is not <base SHA>. Commit all your work on <branch>, leave the worktree clean, and stop. Do not push.
Scope: your worktree only. Leave every other branch, worktree, and `.claude/worktrees/` entry unread, and read the ticket only as it stood at dispatch.
Blockers: report them only in your reply. Post nothing on the ticket.
Commit messages: describe the change; leave the plan name out of them.
Done when: `<acceptance check>` exits 0 in your worktree. Quote its output, and report your worktree path and branch name.
```

A brief never mentions the other attempts, their plans, or their branches.

## 3. Dispatch the builders

`cd <repo>` first: `isolation: worktree` makes its worktree from the Bash working directory. The repo must sit inside the session's allowed working directories; otherwise Claude Code resets the cwd after the `cd` and every worktree comes from the wrong repo. Run `pwd` to confirm the `cd` held. Then send every builder in one message, one Agent call each:

```
Agent({
  description: "best-of <slug> try <K>",
  subagent_type: "builder",
  isolation: "worktree",
  run_in_background: true,
  prompt: "<brief K>"
})
```

Keep working while they run. Each completion notification carries the agent's worktree path, its report, and its token usage; record all three per attempt, plus the agent id. The notification's `worktreeBranch` may still name the harness branch, so record the branch name the builder reports.

## 4. Filter by the check

For each attempt that reports a commit, run `git -C <worktree> status --porcelain` and require empty output: the export and the PR use commits, so uncommitted work would pass here and vanish later. Then run the acceptance check yourself in that worktree, plus the repo's own test suite. The builder's quoted output is a claim; your run is the filter. Drop every candidate that fails, has a dirty tree, or reported `blocked`.

- No candidate passes: skip to step 7 and report each attempt's plan and failure output. Stop there.
- One passes: it is the winner. Skip to step 6.
- Two or more pass: go to step 5.

## 5. Anonymize, shuffle, and pick

The reviewer must not know which plan produced which candidate, and labels must not track try numbers or branch names. Run `mkdir -p ~/scratch/best-of-keys`, then shuffle the passing branches onto letters, redirecting the output to `~/scratch/best-of-keys/<slug>.txt`, which sits outside every directory the reviewer is pointed at:

```
python3 -c 'import random,sys; b=sys.argv[1:]; random.shuffle(b); [print(chr(65+i), x) for i, x in enumerate(b)]' <passing branches>
```

For each line, build `<letters>/<letter>` as a fresh repo with two commits, `base` and `candidate`, and no branches, remotes, or reflog from the source repo. A detached worktree with its `.git` file removed keeps paths that `git archive` would drop through `export-ignore`:

```
git -C <repo> worktree add --detach <letters>/<letter> <base SHA>
rm <letters>/<letter>/.git
git -C <repo> worktree prune
git -C <letters>/<letter> init -q
git -C <letters>/<letter> add -A
git -C <letters>/<letter> commit -qm base
git -C <repo> diff --binary <base SHA> <branch> | git -C <letters>/<letter> apply
git -C <letters>/<letter> add -A
git -C <letters>/<letter> commit -qm candidate
```

The reviewer inherits your Bash working directory, and the source repo or a candidate worktree would show it every try's branch. So `cd <letters>` and confirm with `pwd` before dispatching one reviewer:

```
Agent({
  description: "best-of <slug> blind pick",
  subagent_type: "reviewer",
  run_in_background: true,
  prompt: "<reviewer brief>"
})
```

The reviewer brief holds the task line, the acceptance criteria, and the candidate paths by letter. It omits plan names, branch names, try numbers, the repo path, and builder reports. It asks for this:

```
Candidates A, B, C each implement the task above and each pass `<acceptance check>`. Work only inside <letters>; every other checkout is out of scope. Compare them pairwise (A vs B, A vs C, B vs C). Ground every call in execution: run the tests, and write inputs that tell the candidates apart, such as edge cases, malformed input, scale, or concurrency, into <letters>/scratch, then run each candidate on them. Read `git diff HEAD~1` in each candidate directory for its change. Prefer the candidate that is correct on more of your inputs, then the one with the smaller and simpler change.

Report:
- winner: <letter>
- each pairwise call, with the commands you ran and what they showed
- ideas worth porting: each as "<letter>: <specific idea> - <why it helps the winner>", or "none"
```

Map the winning letter back through the key only after the report arrives.

## 6. Combine

The winner's branch is the base. Patches are never blended. Each idea worth porting that you accept becomes one follow-up `builder` on the winner's branch, run one at a time since they share a checkout. Dispatch it without `isolation`; its brief names the winner's worktree path and branch, the idea, the loser worktree it comes from, and the acceptance check that must still pass. Rerun the check yourself after each port.

A non-code task may instead end in one synthesis that takes the best parts of each candidate, written by you or one builder.

Then push the winner's branch, open its PR the usual way (repo PR rules, `frontier` merge queue under a run), and remove its isolation worktree with `git worktree remove --force <winner worktree path>`. The branch then follows the normal PR flow and its cleanup.

## 7. Report, then clean up

Report, in this order:

- each attempt: its plan, pass or fail (with the failing output's key line), and its token usage from the completion notification;
- the reviewer's pairwise calls and reasoning, letters mapped back to plans;
- which ideas were ported and which were declined, and why;
- the winner's PR URL, and the total tokens across all agents.

After the report, clean up, one command per call:

```
git -C <repo> worktree remove --force <losing worktree path>
git -C <repo> branch -D <losing branch>
rm -rf <letters>
rm -f ~/scratch/best-of-keys/<slug>.txt
```

Then run `git -C <repo> branch --list 'worktree-agent-*'`. Delete with `branch -D` only a `worktree-agent-<id>` whose id came from this run's notifications; any other branch there belongs to someone else.
