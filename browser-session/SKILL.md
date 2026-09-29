---
name: browser-session
description: Drives a site with Playwright under a bot identity held in a storageState file. Use when automating or validating anything in a browser, when a script or check needs a logged-in account, when capturing or reusing a bot login (`--save-storage`, `--load-storage`, `storageState:`), when a site rejects the automated browser, or when personal Chrome or claude-in-chrome is about to act as one of the user's bot accounts.
---

Playwright is the standard for browser automation and validation, and the scarce part of it is never the script - it is the login. A session is captured once, by hand, in a headed window the user has to sit in front of; after that it is a JSON file that costs nothing to reuse on any machine. So the identity lives in that file and travels to the work, rather than the work travelling to whatever browser happens to be logged in.

## Look for the session before capturing one

Sessions are canonical in Playwright storageState JSON files, **one per friend per site** - one file is one identity on one site, and two identities never share a file. Capturing a new one spends the user's attention, so before asking for it, grep the project for `storageState`, `--load-storage`, or `.json` session paths and reuse what is already there.

## Capture with the user in the window

```
npx playwright open --save-storage=<file> <url>
```

The headed window opens, the user does the login themselves - access codes and any other challenge - and closing the browser writes `<file>`. That login step is theirs, not the agent's, so hand over the command and wait rather than driving the form.

## Load it everywhere

The same file drives laptop dev, headless runs on the mini, and Playwright MCP. In a script:

```js
const context = await browser.newContext({ storageState: '<file>' });
```

On the CLI, and for looking at a bot session with your own eyes:

```
npx playwright open --load-storage=<file> <url>
```

A headed window loaded from the file is the way to see what the bot sees - check the session visually there instead of adding screenshots to the automated run.

## When the site rejects the browser

Bundled Chromium is the default and is what most sites accept. A site that blocks it usually accepts real Chrome:

```js
const browser = await chromium.launch({ channel: 'chrome' });
```

## Keep personal Chrome personal

Personal Chrome and claude-in-chrome are for casual checks of the user's own stuff - reading their inbox, glancing at a page they asked about. Every action taken as one of the bot identities goes through a storageState context instead, so the identities stay in files where they can be inspected, copied, and thrown away. Build a cookie-import-to-Chrome bridge only when the user asks for one by name.

The reference page for these sessions - fingerprinting notes and the rest of the convention: `~/wiki/playwright-sessions.md`.
