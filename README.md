# skills

Agent skills for Claude Code and GitHub Copilot: owned behavior and modified forks of third-party skills. Install third-party skills from their upstream repository instead of vendoring them here; fork one into this repo only when it needs local modifications.

Some skills assume a personal setup (`~/inbox`, `~/wiki`, the learn app, a laptop/mini ssh pair). The background-agent policies below work anywhere.

## Installation

Install the background-agent policies that the `builder` and `researcher` agents in [dotfiles-shared](https://github.com/kennedymindeman/dotfiles-shared) preload:

```sh
npx skills add kennedymindeman/skills -g -a claude-code -s researcher-rules builder-rules -y
npx skills add kennedymindeman/skills -g -a github-copilot -s researcher-rules builder-rules -y
```

Claude Code gets Matt Pocock's skills through the official `mattpocock-skills` plugin. Install the skills needed by Copilot directly from upstream:

```sh
npx skills add mattpocock/skills -g -a github-copilot -s research -y
```

## Skills

- **researcher-rules** — keep background research and review read-only,
  neutral, source-grounded, and explicit about uncertainty.
- **builder-rules** — implement one fixed brief against its explicit
  success criterion without widening scope or growing the backlog.
- **dump** — capture a thought verbatim to `~/inbox/` without asking anything or
  leaving the current task; **triage** empties the inbox later.
- **triage** — empty `~/inbox/`: cluster the dumps, route each one to the
  learning queue, a GitHub issue, the wiki, do-now, someday, or drop, with the
  user approving every destination, then archive and commit the pass.
- **frontier** — run a repo's issue frontier via subagents: audit the board,
  dispatch one caged builder per ticket, review, merge, and keep the tracker
  honest.
- **fetch-media** — read YouTube transcripts/frames and Reddit threads that WebFetch/curl can't.
- **distill-video** — turn a YouTube link into a thesis plus timestamped evidence and a transcript-backed Q&A, instead of watching the whole thing.
- **paste-screenshot** — fetch a Cmd+V-pasted screenshot through the clipaste tunnel when the session runs over ssh.
- **import-schedule** — turn a schedule screenshot into Google Calendar events, writing nothing until the parsed list is confirmed.
- **read-document** — extract text from PDF/docx/pptx/xlsx before reading; visual reads only for scans/layout.
- **watch** — arm a background watch (Bash until-loop or Monitor) instead of polling for an external condition.
- **browser-session** — Playwright automation under per-site storageState bot logins.
- **possessions** — review problems with owned expensive things via their wiki pages and open questions.
- **learn-inbox** — capture a topic, hand off work an agent just did, or digest a whole conversation (one item per concept) into the learn app's inbox without enrolling in anything.
- **fetch-amazon** — read Amazon product pages and search results (browser-UA fetch + parser); canonical `/dp/ASIN` links, buybox price, specs.
- **education-ui** — design/restyle UI for learning or reading-heavy tools: calm, legible, professional, non-persuasive; every rule tied to a cited finding (review and vetting in [learn/docs/research](https://github.com/kennedymindeman/learn/tree/main/docs/research)).
- **blind-redesign** — fresh designs for a screen from builders who never see the current UI, compared with the current design under shuffled letters.

## Retired

- **teach** — fork of Matt Pocock's `/teach`. Post-ship,
  the teach/SRS boundary was reversed and the two converged into one learning
  app ([learn#114](https://github.com/kennedymindeman/learn/issues/114)). The
  skill directory, its symlink, and its spec are gone
  ([learn#117](https://github.com/kennedymindeman/learn/issues/117)); the
  renderer lives on in the
  [learn](https://github.com/kennedymindeman/learn) repo.
- **technical-writing** — docs style guide imported from Cursor's pstack
  plugin. Never invoked; `unslop` and the global plain-language and PR-writing
  rules already cover its sentence rules.
