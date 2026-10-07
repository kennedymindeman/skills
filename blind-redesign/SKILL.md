---
name: blind-redesign
description: Blind redesign: builders who never see the current screen each design it fresh, then the user picks among them and the current design under shuffled letters. Use when asked for redesign options to choose from, a fresh take on a screen, or a blind design comparison.
---

A redesign built on top of the current UI inherits its layout, and a comparison where the user knows which one is their current screen is not a fair one. So both halves are **blind**: builders design from what the screen is for, never from what it looks like now, and the user picks from letters before they learn which letter is the current design.

You are the orchestrator. You may read the current UI to find its files; everything you hand a builder is scrubbed of it.

## 1. Write the brief

One brief per redesign, shared word for word by every builder. It holds three things:

- **User tasks** - what the user arrives wanting and what they leave having done, in their words. Pull them from the issue, the handler and API code, and their requests; the markup describes the old answer, not the question.
- **Data contract** - the endpoint, JSON shape, or model types the screen reads and the actions it posts, with field meanings. For a web screen, paste one real response from the fixture below.
- **Real content** - the fixture's actual names and numbers, so each design is judged on the content it will carry.

The brief is blind when it carries no current UI code, screenshots, CSS class or component names, colors, or section headings copied from the current screen. Reread it against that list before dispatching.

## 2. Pin one fixture

Every variant and the current design render the same seed data. Prefer the app's own test seed (a Playwright harness scenario, a pytest fixture, a preview provider); otherwise write a seed script with realistic content into the redesign's workspace. A copy of the live store stays out: it changes between captures and it holds private data that ends up on a preview URL.

## 3. Make one worktree per variant

Under `~/worktrees/<repo>-redesign-<slug>/`, from `origin/main`:

- `current` - untouched; it is captured, not edited.
- `v1`, `v2`, ... - one per builder, on branch `redesign/<slug>-vN`. In a scratch worktree, delete the screen's UI files and commit the result as a history-free root (`git checkout --orphan redesign/<slug>-vN`, `git add -A`, `git commit`). Then give the builder its own clone of only that branch, with no remote: `git clone --no-local --single-branch -b redesign/<slug>-vN <repo> vN`, then `git -C vN remote remove origin`. A worktree would share every branch, main included, so it could still read the old UI. The builder starts from an empty slot the existing route still points at; you fetch its commits back from `vN` when it is done.

What to delete, by app type:

| App type | Delete | Keep |
|---|---|---|
| Server-rendered web | the screen's templates, and the CSS/JS only it loads | routes, handlers, API |
| Static page a backend serves | the HTML file and its private assets | the route that serves it |
| Component web app (React, Vue, Svelte) | the screen's route component, its child components, their styles | API clients, stores, types |
| SwiftUI | the screen's `*View.swift` files and view-only modifiers | models, view models, networking |

Shared theme files and design-system components stay unless the redesign covers the whole look; then they go too.

## 4. Dispatch one builder per variant

Each builder is a fresh context (a `builder` subagent, or `claude -p` / `codex exec` run as background Bash from the variant worktree) whose brief is:

- the shared brief from step 1, verbatim;
- the paths it fills: the deleted files, recreated at the same paths so the existing route serves them;
- the fixture command and how to open the screen, so it can check its own work;
- one rule: design from the brief alone, and leave the running current app and every other checkout of the repo unread;
- done when the screen renders the fixture at 390x844 and 1440x900 with no console errors, and the work is committed on its branch.

Builders run in parallel; each owns only its clone.

## 5. Capture every source the same way

Capture `current` and every variant from its own worktree against the same fixture, into `~/worktrees/<repo>-redesign-<slug>/shots/<source>/`.

**Web:** start each worktree's server on the fixture, then take one shot per viewport with the Playwright CLI (from any checkout that has `@playwright/test`, or `npx playwright`):

```
npx playwright screenshot --viewport-size "390, 844" --full-page --wait-for-timeout 1500 <url> shots/<source>/390x844.png
npx playwright screenshot --viewport-size "1440, 900" --full-page --wait-for-timeout 1500 <url> shots/<source>/1440x900.png
```

The wait lets screens that fetch data after load finish rendering; open one shot and confirm the fixture content is on screen, and raise the wait if it is not. A screen behind a login loads its bot session with `--load-storage <file>`; the `browser-session` skill owns finding or capturing that file.

**iOS:** the mini has no Xcode, so builds and captures run on the laptop. Fetch each variant branch from its clone into the repo and push it, then over `ssh laptop` check it out, build for one simulator model (the same device name for every source), install, launch against the fixture, and capture:

```
ssh laptop xcrun simctl io booted screenshot /tmp/<source>.png
scp laptop:/tmp/<source>.png shots/<source>/<device>.png
```

The capture step is done when every source folder holds the same set of file names.

## 6. Build the blind page and hand it over

```
~/.claude/skills/blind-redesign/compare.py ~/worktrees/<repo>-redesign-<slug>/compare \
  current=$HOME/worktrees/<repo>-redesign-<slug>/shots/current \
  v1=$HOME/worktrees/<repo>-redesign-<slug>/shots/v1 v2=$HOME/worktrees/<repo>-redesign-<slug>/shots/v2
preview ~/worktrees/<repo>-redesign-<slug>/compare <slug>-blind
```

`compare.py` shuffles the sources onto letters, writes a self-contained `index.html` with every image inlined, and writes the key to `compare.key.txt` beside the served folder, outside what `preview` publishes.

Hand the user the preview URL and the key's path, and ask which letter they pick. Keep which letter is the current design out of the conversation until they have chosen; the key file is where they learn it.

The variant branches stay unmerged. The picked one becomes a normal PR only when the user asks for it. Its orphan root shares no history with main, so branch from `origin/main` and copy the variant's files over (`git fetch <vN clone> redesign/<slug>-vN`, then `git checkout FETCH_HEAD -- <paths>`).
