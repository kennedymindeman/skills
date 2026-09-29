---
name: paste-screenshot
description: Fetches the PNG behind a Cmd+V-pasted screenshot path that exists only on the machine that took the shot. Use when a `~/.cache/clipaste/shot-*.png` path arrives in a message and the file is missing locally, or when the user refers to a screenshot they just pasted and no image came with it - typically a session running over ssh on the mini.
---

The user pastes screenshots with Cmd+V everywhere, and clipaste puts the saved PNG's *path* on the clipboard - so what lands in the message is `/Users/kennedy/.cache/clipaste/shot-*.png`, a path rather than a picture. On the machine that took the shot that path is real and the image auto-attaches, and there is nothing to do. Over ssh on the mini it names a file that was never written there, and the picture is one fetch away through the clipaste tunnel.

The tunnel serves the clipboard's *current* image, so fetch promptly: anything copied in between replaces it, and a late fetch returns the wrong picture without complaining.

## Fetch it

1. `ls` the pasted path. It exists → the screenshot is already attached; read it and carry on.
2. It is missing → fetch, passing the path verbatim from the message:

   ```sh
   ~/.claude/skills/paste-screenshot/scripts/fetch-clipaste-image.sh /Users/kennedy/.cache/clipaste/shot-1234.png
   ```

   The script writes the clipboard image to that path, so the file the message named is the file that ends up on disk.
3. Read the file and answer about what is in it.

## A failed fetch means the tunnel is down

The port forward lives only as long as a plain `ssh mini` terminal, and herdr-attach and reused connections don't carry it - so a fetch failure is a diagnosis, not a retry loop. Say so and ask for the terminal:

> The clipaste tunnel is down - open a plain `ssh mini` terminal and keep it open, and I'll grab the screenshot.

Then fetch again once it's open. The clipboard still holds the same image, so the original paste is fine to work from as long as nothing has been copied since.

## Reference

`~/wiki/clipaste-screenshot-paste.md` - how the tunnel is wired, which connection types carry the port forward, and the parked idea for replacing it with a real clipboard mirror.
