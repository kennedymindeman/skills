---
name: subagent-rules
description: Rules preloaded by subagents that do not receive CLAUDE.md. Not for direct use.
---

Run Python through uv (`uv run file.py`, `uv run --with <pkg> python ...`, `uv pip`), never bare `python`, `python3`, or `pip`. A project with its own Python tooling keeps it; a one-off `uv run` in a project without uv gets `--no-project`.

Write multi-line text (scripts, commit messages, issue and PR bodies) to a file with the Write tool and pass the file (`git commit -F`, `gh ... --body-file`), not a heredoc, `printf`, or `echo`.

When debugging, produce evidence for the diagnosis (a failing test, instrumentation, a log excerpt) before changing code.

Run remote operations, cleanup, branch changes, and destructive commands as standalone Bash calls, without pipes, `;`, or `&&`, and outside any parallel batch of reads.

When the user or a permission check denies an action, report the denial and move on. Retrying it, splitting it, rewrapping it, or writing the same content to another path all count as routing around it.

You cannot reach the user. Put every question, decision, and step that needs the user in your report, recommendation first.

Before returning, remove what you created: scratch directories, temp files, downloads, and caches filled only for the task. List anything left behind and why.

Write the report in plain words, one idea per sentence. When your own rules skill or agent body sets a report format, follow it; otherwise put the result first, then the output of each check you ran, then background.
