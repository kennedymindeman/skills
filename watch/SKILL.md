---
name: watch
description: Arms a background watch for an external condition so the session keeps working while it resolves. Use when waiting on a file to land, a print to finish, CI or PR checks to pass, or any wait longer than a few seconds - and whenever the alternative is a foreground sleep, polling by hand, or asking the user to report back when the thing is done.
---

A wait is not work. The turn spent holding still on `sleep 240` is a turn the session could have spent on the next task, and it ends with the user interrupting to get the turn back. So an external condition is never waited on in the foreground - it is **armed** as a background watch that fires when the condition holds, and the session moves on to other work in the same turn.

## Arm it

Two harness tools do the waiting; pick by how long the wait may run and how many notifications you want.

**One-shot under ten minutes - `Bash` with `run_in_background: true`** and an `until` loop that exits once the condition holds:

```sh
until ls ~/projects/3d-print/a20/*.3mf >/dev/null 2>&1; do sleep 5; done
```

That yields one completion notification. Background Bash is capped by its `timeout` (max 600000 ms = ten minutes), so a wait that may outlast that belongs to Monitor.

**Longer, or repeating - the `Monitor` tool.** It is deferred: load it with `ToolSearch("select:Monitor")`. Monitor runs a script in the background and turns every stdout line into a notification; the watch ends when the script exits. `persistent: true` removes the timeout. For a one-shot wait past the ten-minute cap, hand it a command that exits on the first match, still with `persistent: true` - same single notification, no cap. Stop one early with `TaskStop` (also deferred).

Without `persistent: true` a Monitor times out at 3600000 ms (one hour). The rules that separate a watch that fires from one that sits silent or gets auto-stopped:

- Every pipe stage flushes per line (`grep --line-buffered`, `awk '{print; fflush()}'`). A buffered stage, or `| head -N`, holds the line that should have fired.
- Match every terminal state - failed, cancelled, paused - and not only success. Silence looks identical to "still running".
- Emit only lines you would act on. A firehose gets the monitor auto-stopped.
- Poll remote APIs every 30 s or slower, local checks every 0.5-5 s, and wrap flaky calls in `|| true` so one error doesn't end the watch.
- A file arriving by `scp` or download may still be writing when it first appears: wait a few seconds after the match before reading it.
- For CI, diff `gh pr checks <n> --json name,bucket` against the previous poll and exit once nothing is pending.
- A notification is an event, not the user's reply, even when it lands while a question is pending.
- Give the Monitor a specific `description`; it is shown on every notification.

`~/wiki/claude-code-waiting-for-triggers.md` holds the machine-specific recipes (printer state, camera checks) and the pitfall log behind these rules.

## Say what is armed

Announce the watch on screen in the turn that arms it: the condition being watched, the tool holding it, and what happens when it fires.

> Armed a Monitor on `~/Downloads/*.3mf` (persistent); it notifies once the file lands, then I'll read it. Meanwhile, back to the slicer profile - 

The user is then free to leave the session alone, which is the whole point of arming rather than polling. Continue with other work in the same turn.

## Re-arm after a clear

A watch lives inside the session that armed it: `/clear`, a new session, or a crash takes it down with no notification. When a session resumes work that had a watch on it, re-arm the watch before doing anything that assumes it is still live, and say so.
