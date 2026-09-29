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

Before arming a Monitor, read `~/wiki/claude-code-waiting-for-triggers.md`. Per-line flushing, matching every terminal state rather than only success, and the right poll interval are what separate a watch that fires from one that sits silent or gets auto-stopped as a firehose. The page also carries the worked recipes for these machines - a file landing via scp, P1S print state over MQTT, `gh pr checks` diffed poll to poll - and the pitfall log behind these rules.

## Say what is armed

Announce the watch on screen in the turn that arms it: the condition being watched, the tool holding it, and what happens when it fires.

> Armed a Monitor on `~/Downloads/*.3mf` (persistent); it notifies once the file lands, then I'll read it. Meanwhile, back to the slicer profile - 

The user is then free to leave the session alone, which is the whole point of arming rather than polling. Continue with other work in the same turn.

## Re-arm after a clear

A watch lives inside the session that armed it: `/clear`, a new session, or a crash takes it down with no notification. When a session resumes work that had a watch on it, re-arm the watch before doing anything that assumes it is still live, and say so.
