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
- `gh issue list --label needs-info` and `--label ready-for-human` - tickets a prior run parked. In an interactive session these go to the owner first, as AskUserQuestion batches of 4, before any dispatch; a headless run lists them under "Blocked on me" and moves on. A parked ticket needs an unanswered question: a comment containing `Question for owner:` (any case; a backtick immediately before the phrase exempts it) newer than the latest decision comment - one starting `Decision (` followed by the owner's name - or, only while no such comment exists, a `## Question` section in the body. One without is mislabelled: extract the one live question from the ticket and write it as that comment with 2-4 options, recommended first. A `needs-info` ticket with no live question may instead return to `ready-for-agent`; a `ready-for-human` ticket never does, since it still waits on the owner.
- `gh issue list --label in-queue` - tickets already in a queue branch or run PR from an earlier run; they are not takeable. If their run PR has merged since, finish its landing as "Land the ticket and the board together" describes; while it is open, they wait on the owner. With neither a live `run/*` branch nor a run PR, the queue has stranded and gets reported first.
- `git branch -a --list 'run/*'` - a stale queue from a prior day. An unreviewed `run/<date>` gets reviewed and its run PR opened before anything new is dispatched.

The audit is done when every ticket you intend to work is accounted for against every view above. Then **claim** each one - assign it, and write the coordinator's name into its one status comment - before spawning anything; concurrent sessions have double-booked tickets and shipped duplicate PRs of the same work. If an earlier run left a status comment (the one naming a coordinator), edit that; otherwise post it with `gh issue comment` and take the ID from the number after `#issuecomment-` in the URL it prints. Keep the ID: every status update edits that comment in place with `gh api -X PATCH repos/<owner>/<repo>/issues/comments/<id> -F body=@<file>`, with the body written by the Write tool, so the ticket carries one status comment, not a trail of run noise. `Question for owner:` comments stay separate new comments - the parked-ticket check reads the newest comment holding that phrase.

Every `agent/*` and `run/*` branch the audit turns up - local or remote - leaves it with a verdict, or last month's abandoned builds are still there next quarter:

- **Merged into `origin/main`** (`git branch -a --merged origin/main | grep -E 'agent/|run/'`, which catches the `run/<date>` of a run PR the owner merged) - delete it both sides, stripping the `origin/` prefix from the name: `git push origin --delete <branch>`, `git branch -D <branch>`, then `git worktree prune`.
- **Unmerged, ticket closed** - leave the branch alone and report it by name under "Blocked on me" with its ticket and last commit date (`git log -1 --format=%cs <branch>`); the owner decides whether it dies.
- **Unmerged, ticket open** - that branch is the ticket's starting point, so the brief bases on it rather than commissioning a fresh build of work that already exists.

Whenever that list is non-empty it goes in the run summary; the session-end sweep is this pass's counterpart for the branches the run itself created.

## Triage before you dispatch

`needs-triage` is not takeable, and skipping it silently is how a backlog of tickets sits for weeks while the nights run idle. So the run makes a triage pass over them first. The pass itself only relabels - a ticket it stamps `ready-for-agent` is takeable immediately, and one it leaves at any other label is not built this run.

1. `gh issue list --label needs-triage --state open --limit 100` - without `--limit` the default 30 silently drops the oldest tickets, which is the backlog. An open ticket carrying no state label counts as `needs-triage` too, whatever category labels it has; that command can't return those, so follow it with `gh issue list --state open --limit 300 --json number,labels` and keep the tickets whose labels include none of the six state labels (`needs-triage`, `ready-for-agent`, `needs-info`, `ready-for-human`, `in-queue`, `proposed`). `proposed` marks a ticket an outside reporter filed that waits on the owner's approval; only the owner promotes it. Skip anything already assigned or claimed in a comment - a concurrent run holds it.
2. Read each one. If it names a goal and a definition of done and has no open blocker: `gh issue edit <N> --remove-label needs-triage --add-label ready-for-agent`.
3. Anything short of that: post one comment starting `Question for owner:` carrying 2-4 concrete options, recommended first, then `gh issue edit <N> --remove-label needs-triage --add-label needs-info`. One question, not a list.
4. Work only the owner can do - sudo, a console, live data, taste - gets the same one `Question for owner:` comment, its options naming what the owner would do, then `gh issue edit <N> --remove-label needs-triage --add-label ready-for-human`. One state label per ticket, always, so the remove is never optional.
5. Comment on nothing you merely skipped.

The questions this pass raises route out the same run: an interactive session parks each on its ticket, keeps dispatching the rest, and puts them to the owner as AskUserQuestion batches of 4 once no other work is left, and a headless run lists the newly parked tickets under "Blocked on me" alongside the ones the audit found.

## Check before you dispatch

Per ticket, in the orchestrator's own shell:

1. `cd` to the target repo. An `isolation: worktree` dispatch snapshots the Bash cwd, not the repo named in the prompt - agents have been handed a worktree of an entirely different project this way.
2. Check the current branch against `origin/main` and pin the base in the brief explicitly. A repo parked on a deploy branch poisons every PR opened from it.
3. Grep for the files the ticket names. A ticket written against retired code costs one grep to kill and a whole dispatch to discover.
4. Partition the round by file surface - one writer per checkout, one checkout per file cluster. Tickets that touch the same files go to a single agent as a bundle.

A ready ticket these checks decline - retired code, too big for one dispatch - is stopped, not silently skipped: write its `stopped: declined - <reason>` comment and park it as "Stop a ticket that isn't moving" describes.

## Cage every brief

The brief is the cage: it fixes what the agent may touch, where it starts, and how it reports back. Every ticket goes out with every section of this filled in.

```markdown
REPO GUARD: run `git remote -v` first - it must show <owner/repo>. Any other repo: stop and report.

Brief: <the change, in one line>. Spec and acceptance criteria: `gh issue view <N> --comments`.

Reading order:
1. <the spec or design doc>
2. <the convention or house-style file the change must follow>
3. <the closest existing implementation> - the pattern to copy.

Base: branch `agent/issue-<N>-<slug>` from <origin/main | the run's queue tip <sha>>. On a resumed ticket: continue on its existing unmerged `agent/issue-<N>[-slug]` branch <name> - do not cut a new one - and open a fresh PR only if none is open.

MUST NOT:
- <the branch, file, or directory that looks live but is abandoned> - IGNORE it.
- Touch <live systems: prod data, deploys, dotfiles, the tracker beyond this issue>.
- Merge the PR or close the issue.
- Delete or skip a failing test - report it instead; only the orchestrator retires one.

Stop and park - do not guess - the moment any of these is true. A stopped dispatch costs one dispatch; a guess costs a wrong PR plus its review and its fix.
1. The ticket does not decide an outcome you can state as 2-4 options whose consequences differ for the owner (what they see, what data is kept, what it costs).
2. The next action is not undoable by `git revert` + push - live data, a deploy, a secret, a force-push, any edit under `~/.claude`, the live `~/dotfiles` checkout, or any other live checkout (a service's running checkout); edits in your own worktree never count, even on a dotfiles ticket.
3. The same auth path failed twice, or the permission classifier blocked a command. Name the credential's location (env var, 1Password item); never ask for the value and never route around the block.
4. Two sentences you can quote - from this ticket, AGENTS.md/CLAUDE.md, the wiki, or another ticket - cannot both be true.

Mechanism choices with an established convention (file layout, library, schema, storage engine) are yours unless they change what the owner sees: decide, and record it under "ambiguous-and-how-I-resolved-it".

Parking means one comment on the ticket: a first line `trigger: <1-4> - <which condition above>`, then a line starting `Question for owner:` with the question, then 2-4 options with a one-sentence consequence each, recommended first. Everything after that phrase is read as the question, so nothing follows the options. New evidence later goes in a new comment that repeats the question; never edit the old one.

Command discipline - auto mode's classifier refuses compound and destructive lines, and a refused cleanup leaves a worktree stranded:
1. One command per Bash call. No `&&`, `;`, or pipes on any line that changes git state or removes files.
2. `git -C <absolute path>` instead of `cd`.
3. Absolute paths everywhere.
4. Retire a worktree in two separate calls: `git worktree remove --force /abs/path/to/worktree` first, then `git -C /abs/path/to/repo branch -D <name>`. Without `--force` the remove refuses a checkout holding untracked files - the normal state after a build - and `-d` refuses the unmerged branch this is meant to clean up.

Verify in this session before you claim: run the verifying command, quote its output in the PR body under `## Validation` (or `not run: <reason>`). Saying done, fixed, or passing without that output is not done.

Success criterion: <the goal-delta, checkable by someone who reads only the diff>.

Report back: `status: done|blocked|partial` / what changed / `validation:` command + output / PR link / `questions:` / `trigger:` the stop condition above that fired (1-4), or `none` / found-not-acted-on / ambiguous-and-how-I-resolved-it.
```

For UI or prototype tickets, restate the standing interaction rules in the brief - write deliverables to disk, and put any choice for the owner in the report, since a builder has no AskUserQuestion. Subagents inherit none of these rules. The brief also names one user flow - "log water, see the total update" - and the success criterion is that flow driven end to end in the running app, evidenced in `.pr-assets/issue-<N>/flow.md` as `builder-rules` describes and linked from the PR body. A screenshot shows a render, not a working flow. Before landing, the orchestrator removes `.pr-assets/` with one commit on the queue tip so it never reaches main.

## Dispatch by role

- **Build** → `builder`, `isolation: worktree`, ending at an open PR based on the run's queue branch (on `origin/main` only for a single-branch run, where that PR becomes the run PR once its review passes: the orchestrator adds the review verdict and a `Closes #<N>` line to its body, labels the ticket `in-queue` with `gh issue edit <N> --remove-label ready-for-agent --add-label in-queue`, and from there follows the same run PR steps below).
- **Review and verify** → `reviewer`, blind. The reviewer re-runs the PR's `## Validation` commands and reads any `flow.md` and its screenshot; a PR missing that section fails review. Every PR gets one before its issue closes, and reviews run interleaved with the builds rather than saved for the end - an end-of-queue review has starved on usage credits with confirmed bugs left unfixed. Send its findings back out as surgical fix dispatches. When the diff adds dead-code-whitelist entries (e.g. `vulture_whitelist.py`), the brief has the reviewer verify each added name is actually reached at runtime - the builder is the one party who can't audit its own whitelisting.

Integration is a **merge queue**. At the first multi-branch round, cut `run/<date>` from `origin/main`; as each branch's review passes, run the queue-entry checklist below. Later builders branch from the queue tip, not `origin/main`. A blind review of the full queue diff precedes the landing. The run ends by opening one **run PR**, `gh pr create --base main --head run/<date>`, whose body carries the review's verdict, any unresolved findings summarized, and one `Closes #<N>` line per ticket that landed whole. Main belongs to the owner: the run lists the run PR's URL and `gh pr merge <PR> --merge --delete-branch -R <owner>/<repo>` under "Blocked on me" and leaves the merge, git-level or `gh`, to them. Reserve the budget for that review - stop dispatching new builds once elapsed wall clock passes 80% of the runner's per-repo window (`nightly-frontier`'s `REPO_TIMEOUT`, a 90-minute alarm), or at the first usage-limit warning, whichever comes first. When conflicts outgrow the orchestrator's context, hand the queue to one **integrator** agent that absorbs them in its own context and stays alive across rounds via SendMessage.

## Stop a ticket that isn't moving

Two breakers per ticket, both tunable:

- **Fix cap** - after K=3 review→fix rounds the ticket stops.
- **No progress** - a round that returns no diff, or the same error string as the round before, gets one retry with that error quoted in the brief; still nothing, and the ticket stops.

Stopping means: leave the PR open with the unresolved findings, release the claim (`gh issue edit <N> --remove-assignee @me`, then note the released lease in the status comment with the PATCH above, not a new comment), and park the ticket. The parked label is what keeps it on the owner's list and out of the runner's picks until they answer. Every stop gets one standalone comment whose first line is `stopped: <breaker> - <what was tried>`, where the breaker is `fix-cap`, `no-progress`, or the builder's `trigger:`; a ready ticket the orchestrator declines to dispatch at the check step (retired code, too big) writes `stopped: declined - <reason>`; with `trigger: none`, a builder `blocked` or `partial` writes `stopped: blocked - <the builder's one-line reason>`, and a builder `done` with non-empty `questions:` writes `stopped: questions - <its first question>`. Both copy builder text, so reword any copy containing `question for owner:` until that phrase appears only on the real question line. What follows the `stopped:` line depends on how many `stopped:` comments the ticket has, `stopped: declined` included, counted over its whole history and never reset by a decision comment. From the third onward, always follow it with `Question for owner:` and the stall question - finish from the branch, cut scope, re-spec, or close, recommended first - even when the builder already asked; a still-unanswered builder question becomes one of its options, so a decision on the stall question settles both. Before the third, if the builder already left an unanswered question, the `stopped:` line is the whole comment; otherwise follow it with `Question for owner:`, the findings as the question - for a `stopped: blocked`, how to proceed on that reason; for a `stopped: questions`, the builder's question - and 2-4 options with a one-sentence consequence each, recommended first - the shape triage step 3 leaves; with no sharper question, ask the stall question. Then label by the builder's `trigger:`: 3 (an auth failure, a classifier block) is owner-only work and gets `ready-for-human`; everything else gets `needs-info` - 2 included, since an irreversible action is a yes/no the agent carries out once approved, and fix-cap and no-progress trips too: `gh issue edit <N> --remove-label ready-for-agent --add-label <label>`. Only `status: done` carrying validation output is landable; `blocked` and `partial` stop the same way, as do reported questions. Log every trip as one line in the run summary - `stopped #N: fix-cap 3/3`, `stopped #N: no-progress` - and list the parked tickets under "Blocked on me".

When the owner sends a parked ticket back to `ready-for-agent`, the next run claims it and first reads the newest decision comment. On close, it closes the PR and the issue with the decision's reason. On cut scope, it edits the issue's done-criteria to match the decision, then builds. Otherwise it resumes. A resumed ticket continues on its unmerged `agent/issue-<N>[-slug]` branch rather than cutting a new one. Its PR may be gone - GitHub closes a PR into `run/<date>` when the queue branch is deleted - so the builder opens a fresh PR only if none is open.

## Land the ticket and the board together

Before a branch enters the queue, when `diff-coverage-gate` and `test-tamper-check` are on PATH, run both in a clean checkout of the branch with `run/<date>` as the argument, so each ticket is judged alone against the queue. A gate failure keeps the branch out of the queue and goes back as a fix dispatch; each hunk the tamper check flags goes to the reviewer to clear. Before opening the run PR, run both again on the queue tip with no argument.

Every duplication incident on record traces to work landing while the tracker held still, and a wind-down pass over the board arrives after the next session has already picked up the ghost. So a branch enters the queue in one turn, all three steps or none:

1. Merge the branch into `run/<date>` with plain `git merge` and push (queue entries use git-level merges, not `gh pr merge`).
2. Delete the branch both sides - the same `git push origin --delete <branch>` / `git branch -D <branch>` pair as the audit above.
3. `gh issue edit <N> --remove-label ready-for-agent --add-label in-queue`, plus an edit to the claim's status comment (the PATCH above, not a new comment) carrying the queue tip SHA it merged at. Create the label once per repo if it is missing.

When the run PR opens, PATCH each of its issues' status comments to `In run PR <url>, waiting on the owner's merge`; `in-queue` stays on. Once the owner merges it, the `Closes` lines close the whole tickets, and the next run's audit finishes each issue: PATCH the status comment to `Landed on main at <sha> via run/<date>` with the PR link in the body, then `gh issue edit <N> --remove-label in-queue` and, if GitHub left it open, `gh issue close <N>` - or, if the ticket landed partial, the same comment saying what actually shipped, `in-queue` removed all the same, and the issue left open. A partial ticket that keeps `in-queue` reads to the next audit as a stranded queue. Finished work is never parked as `ready-for-human`; that label means work only the owner can do.

## Keep the run visible

Open each turn with a running-agents line: which agents are live and on what, and what each background watcher fires when it triggers. An unattended run otherwise goes dark, and "is it still going?" should be answered on screen before it is asked.

## Sweep before the clear

Ending the session, enumerate **by name** every `agent/*` branch and worktree that is unmerged, with the ticket each belongs to - finished-but-unmerged work has come close to being lost twice. The run is clear-ready when that list is empty - every reviewed branch queue-merged and deleted, the run PR open and listed under "Blocked on me" - or written where the next session will find it.
