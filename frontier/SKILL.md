---
name: frontier
description: Runs a repo's issue frontier as a queue of subagents. Use when working a ticket queue or running the frontier unattended.
---

Subagent execution is reliably fine; the waste lives one level up, in the orchestration - boards that lag the code, worktrees pointed at the wrong repo, briefs re-derived from scratch each session. So the run is yours to hold on three fronts: the board tells the truth, the git mechanics are pinned before anything spawns, and every dispatch goes out **caged**.

## Audit the board

Before the first dispatch, reconcile the tracker against the repo - an implemented-but-still-open ticket reads as takeable work, and a fresh session once started rebuilding 19 of them:

- `git branch -a --list 'agent/*'` - work another session already built.
- `git worktree list` - checkouts still held, and by which repo.
- `gh pr list` - open PRs and the issue each one closes.
- Issue assignees and recent comments - a concurrent session may already hold the ticket.
- `gh issue list --label needs-info` and `--label ready-for-human` - tickets a prior run parked. In an interactive session these go to the owner first, as AskUserQuestion batches of 4, before any dispatch; a headless run lists them under "Needs you" and moves on.
- `gh issue list --label in-queue` - tickets already merged into a queue branch by an earlier run; they are not takeable, and if no `run/*` branch is live the queue has stranded and gets landed or reported first.
- `git branch -a --list 'run/*'` - a stale queue from a prior day. An unreviewed `run/<date>` gets reviewed and landed before anything new is dispatched.

The audit is done when every ticket you intend to work is accounted for against every view above. Then **claim** each one - assign it, comment on it - before spawning anything; concurrent sessions have double-booked tickets and shipped duplicate PRs of the same work.

Every `agent/*` and `run/*` branch the audit turns up - local or remote - leaves it with a verdict, or last month's abandoned builds are still there next quarter:

- **Merged into `origin/main`** (`git branch -a --merged origin/main | grep agent/`) - delete it both sides, stripping the `origin/` prefix from the name: `git push origin --delete <branch>`, `git branch -D <branch>`, then `git worktree prune`.
- **Unmerged, ticket closed** - leave the branch alone and report it by name under "Needs you" with its ticket and last commit date (`git log -1 --format=%cs <branch>`); the owner decides whether it dies.
- **Unmerged, ticket open** - that branch is the ticket's starting point, so the brief bases on it rather than commissioning a fresh build of work that already exists.

Whenever that list is non-empty it goes in the run summary; the session-end sweep is this pass's counterpart for the branches the run itself created.

## Triage before you dispatch

`needs-triage` is not takeable, and skipping it silently is how a backlog of tickets sits for weeks while the nights run idle. So the run makes a triage pass over them first. The pass itself only relabels - a ticket it stamps `ready-for-agent` is takeable immediately, and one it leaves at any other label is not built this run.

1. `gh issue list --label needs-triage --state open --limit 100` - without `--limit` the default 30 silently drops the oldest tickets, which is the backlog. An open ticket carrying no state label counts as `needs-triage` too, whatever category labels it has; that command can't return those, so follow it with `gh issue list --state open --limit 300 --json number,labels` and keep the tickets whose labels include none of the five state labels (`needs-triage`, `ready-for-agent`, `needs-info`, `ready-for-human`, `in-queue`). Skip anything already assigned or claimed in a comment - a concurrent run holds it.
2. Read each one. If it names a goal and a definition of done and has no open blocker: `gh issue edit <N> --remove-label needs-triage --add-label ready-for-agent`.
3. Anything short of that: post one comment starting `Question for owner:` carrying 2-4 concrete options, then `gh issue edit <N> --remove-label needs-triage --add-label needs-info`. One question, not a list.
4. Work only the owner can do - sudo, a console, live data, taste - gets `gh issue edit <N> --remove-label needs-triage --add-label ready-for-human`. One state label per ticket, always, so the remove is never optional.
5. Comment on nothing you merely skipped.

The questions this pass raises route out the same run: an interactive session puts them to the owner as AskUserQuestion batches of 4 before the first dispatch, and a headless run lists the newly parked tickets under "Needs you" alongside the ones the audit found.

## Check before you dispatch

Per ticket, in the orchestrator's own shell:

1. `cd` to the target repo. An `isolation: worktree` dispatch snapshots the Bash cwd, not the repo named in the prompt - agents have been handed a worktree of an entirely different project this way.
2. Check the current branch against `origin/main` and pin the base in the brief explicitly. A repo parked on a deploy branch poisons every PR opened from it.
3. Grep for the files the ticket names. A ticket written against retired code costs one grep to kill and a whole dispatch to discover.
4. Partition the round by file surface - one writer per checkout, one checkout per file cluster. Tickets that touch the same files go to a single agent as a bundle.

## Cage every brief

The brief is the cage: it fixes what the agent may touch, where it starts, and how it reports back. Every ticket goes out with every section of this filled in.

```markdown
REPO GUARD: run `git remote -v` first - it must show <owner/repo>. Any other repo: stop and report.

Brief: <the change, in one line>. Spec and acceptance criteria: `gh issue view <N> --comments`.

Reading order:
1. <the spec or design doc>
2. <the convention or house-style file the change must follow>
3. <the closest existing implementation> - the pattern to copy.

Base: branch `agent/issue-<N>-<slug>` from <origin/main | the run's queue tip <sha>>.

MUST NOT:
- <the branch, file, or directory that looks live but is abandoned> - IGNORE it.
- Touch <live systems: prod data, deploys, dotfiles, the tracker beyond this issue>.
- Merge the PR or close the issue.
- Delete or skip a failing test - report it instead; only the orchestrator retires one.

Stop and report if <the product decision this ticket can run into> is ambiguous - a stopped dispatch costs one dispatch, a guess costs a wrong PR plus its review and its fix. Blockers and open questions go as a comment on the ticket too, so they outlive the run.

Command discipline - auto mode's classifier refuses compound and destructive lines, and a refused cleanup leaves a worktree stranded:
1. One command per Bash call. No `&&`, `;`, or pipes on any line that changes git state or removes files.
2. `git -C <absolute path>` instead of `cd`.
3. Absolute paths everywhere.
4. Retire a worktree in two separate calls: `git worktree remove --force /abs/path/to/worktree` first, then `git -C /abs/path/to/repo branch -D <name>`. Without `--force` the remove refuses a checkout holding untracked files - the normal state after a build - and `-d` refuses the unmerged branch this is meant to clean up.

Verify in this session before you claim: run the verifying command, quote its output in the PR body under `## Validation` (or `not run: <reason>`). Saying done, fixed, or passing without that output is not done.

Success criterion: <the goal-delta, checkable by someone who reads only the diff>.

Report back: `status: done|blocked|partial` / what changed / `validation:` command + output / PR link / `questions:` / found-not-acted-on / ambiguous-and-how-I-resolved-it.
```

For UI or prototype tickets, restate the standing interaction rules in the brief - write deliverables to disk, use AskUserQuestion for choices. Subagents inherit none of them. The brief also names one user flow - "log water, see the total update" - and the success criterion is that flow driven end to end in the running app, evidenced in `.pr-assets/issue-<N>/flow.md` as `fixed-brief-executor` describes and linked from the PR body. A screenshot shows a render, not a working flow. Before landing, the orchestrator removes `.pr-assets/` with one commit on the queue tip so it never reaches main.

## Dispatch by role

- **Build** → `builder`, `isolation: worktree`, ending at an open PR based on the run's queue branch (on `origin/main` only for a single-branch run).
- **Review and verify** → `reviewer`, blind. The reviewer re-runs the PR's `## Validation` commands and reads any `flow.md` and its screenshot; a PR missing that section fails review. Every PR gets one before its issue closes, and reviews run interleaved with the builds rather than saved for the end - an end-of-queue review has starved on usage credits with confirmed bugs left unfixed. Send its findings back out as surgical fix dispatches. When the diff adds dead-code-whitelist entries (e.g. `vulture_whitelist.py`), the brief has the reviewer verify each added name is actually reached at runtime - the builder is the one party who can't audit its own whitelisting.

Integration is a **merge queue**. At the first multi-branch round, cut `run/<date>` from `origin/main`; as each branch's review passes, run the queue-entry checklist below. Later builders branch from the queue tip, not `origin/main`. A blind review of the full queue diff decides the landing. Clean: merge the queue into main with plain `git merge`, push, delete `run/<date>`, and report the landed queue in the run summary - the git-level merge after a passing review is the sanctioned landing path, no PR to the owner. Unresolved findings: the queue goes to the owner as the compare URL (`https://github.com/<owner>/<repo>/compare/main...run/<date>`) plus the merge command, and the findings summarized. Reserve the budget for that review - stop dispatching new builds once elapsed wall clock passes 80% of the runner's per-repo window (`nightly-frontier`'s `REPO_TIMEOUT`, a 90-minute alarm), or at the first usage-limit warning, whichever comes first. When conflicts outgrow the orchestrator's context, hand the queue to one **integrator** agent that absorbs them in its own context and stays alive across rounds via SendMessage.

## Stop a ticket that isn't moving

Two breakers per ticket, both tunable:

- **Fix cap** - after K=3 review→fix rounds the ticket stops.
- **No progress** - a round that returns no diff, or the same error string as the round before, gets one retry with that error quoted in the brief; still nothing, and the ticket stops.

Stopping means: leave the PR open with the unresolved findings, comment those findings on the issue as one `Question for owner:` comment - the same shape triage step 3 leaves, so every `needs-info` ticket scans the same, then `gh issue edit <N> --remove-label ready-for-agent --add-label needs-info`, and move on. Only `status: done` carrying validation output is landable; `blocked` and `partial` stop the same way, as do reported questions. Log every trip as one line in the run summary - `stopped #N: fix-cap 3/3`, `stopped #N: no-progress` - and list the `needs-info` tickets under "Needs you".

## Land the ticket and the board together

Every duplication incident on record traces to work landing while the tracker held still, and a wind-down pass over the board arrives after the next session has already picked up the ghost. So a branch enters the queue in one turn, all three steps or none:

1. Merge the branch into `run/<date>` with plain `git merge` and push (`gh pr merge` stays blocked; git-level merges into non-main branches are the sanctioned path).
2. Delete the branch both sides - the same `git push origin --delete <branch>` / `git branch -D <branch>` pair as the audit above.
3. `gh issue edit <N> --remove-label ready-for-agent --add-label in-queue`, plus a comment on the issue carrying the queue tip SHA it merged at. Create the label once per repo if it is missing.

When the queue lands on main, the run closes each of its issues itself: `gh issue comment <N> --body "Landed on main at <sha> via run/<date>"` with the PR link in the body, then `gh issue edit <N> --remove-label in-queue` and `gh issue close <N>` - or, if the ticket landed partial, the same comment saying what actually shipped, `in-queue` removed all the same, and the issue left open. A partial ticket that keeps `in-queue` reads to the next audit as a stranded queue. Finished work is never parked as `ready-for-human`; that label means work only the owner can do.

## Keep the run visible

Open each turn with a running-agents line: which agents are live and on what, and what each background watcher fires when it triggers. An unattended run otherwise goes dark, and "is it still going?" should be answered on screen before it is asked.

## Sweep before the clear

Ending the session, enumerate **by name** every `agent/*` branch and worktree that is unmerged, with the ticket each belongs to - finished-but-unmerged work has come close to being lost twice. The run is clear-ready when that list is empty - every reviewed branch queue-merged and deleted, the landed queue reported - or written where the next session will find it.
