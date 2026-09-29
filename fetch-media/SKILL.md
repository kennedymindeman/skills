---
name: fetch-media
description: Reads YouTube transcripts and frames and Reddit threads that WebFetch and curl can't. Use for any youtube.com, transcript-site (youtubetotranscript, tactiq), or reddit.com URL; when a fetch returns 403, 405, or nav chrome instead of content; before telling the user a source is unreachable; and when writing a brief that sends a subagent at YouTube or Reddit.
---

These sources are reachable - the fetch tools just aren't how you reach them. `WebFetch` and `curl` hand back nav chrome or a 403/405 for youtube.com, for the third-party transcript sites, and for all of reddit.com, and the failure looks like the source being closed rather than the tool being wrong. `~/wiki/fetching-media.md` is the reference behind this skill: the same recipes with the full pitfall notes.

## YouTube transcript

```sh
uvx youtube_transcript_api <VIDEO_ID>
```

When the ask is to explain, summarize, or argue with the video rather than to reach it, the transcript is the input and `distill-video` is the skill that turns it into a thesis with timestamped evidence.

Underscores - the package's executable is `youtube_transcript_api` and the hyphenated name no longer resolves. Inside a script, `uv run --with youtube-transcript-api python -c "..."`. uv caches the package, so repeat runs don't re-download it.

## YouTube frames

For what the transcript can't carry - on-screen text, posters, labels, hardware. The order is transcript for what's said, storyboards to find the moment, then a slice to read it.

**Storyboards locate the moment** (no video download, ~1MB, seconds):

```sh
yt-dlp -f sb0 -o 'sb.%(ext)s' '<URL>'
```

That writes `.mhtml` carrying one WebP sheet per part - WebP, so scanning the raw bytes for JPEG markers finds nothing. Parse it with the stdlib `email` module, reading the whole file in with `message_from_bytes`; `message_from_binary_file` eats a trailing byte off some parts:

```sh
python3 -c "
import email
sheets = [p for p in email.message_from_bytes(open('sb.mhtml','rb').read()).walk()
          if p.get_content_type().startswith('image/')]
for i, p in enumerate(sheets):
    open(f'sheet{i:02d}.webp','wb').write(p.get_payload(decode=True))
print(len(sheets), 'sheets')
"
```

The image API rejects WebP, so re-encode each sheet before reading it:

```sh
for f in sheet*.webp; do sips -s format png "$f" --out "${f%.webp}.png"; done
```

Read the grid off the sheet rather than assuming it: the sheet's pixel size (`sips -g pixelWidth -g pixelHeight`) divided by the tile size `yt-dlp -F` prints for `sb0` gives the tiles per sheet - 5×5 of 160×90 today. Each sheet's `<figcaption>Slide #N: HH:MM:SS</figcaption>` gives its start and its `duration:` gives its span, so `tile_seconds = duration / tiles` maps a timestamp to a tile. Take that ratio off a full sheet: the last sheet is short and its trailing tiles are blank. Storyboards are too low-res to read text - they tell you where to slice.

**Full resolution reads text and specs.** Download only the slice:

```sh
yt-dlp -f 'bv[height<=1080][ext=mp4]/bv[height<=1080]/b[height<=1080]' --download-sections '*<start>-<end>' -o clip.mp4 '<URL>'
ffmpeg -y -i clip.mp4 -vf 'select=eq(n\,20)' -vframes 1 frame.png
```

Every branch caps at 1080p. That is the resolution where conference posters and screen text stay legible, and five seconds of it costs about 4MB. Only the slice downloads, never the whole video. The two slashes are fallbacks, not the cap: mp4 video-only first, then video-only in any container, then a combined audio+video stream for the videos that publish no video-only one. Video-only comes first because it is the smaller download. That last branch is why a video with no video-only stream still yields a frame instead of `Requested format is not available`. Ask for `ext=mp4` first because plain `bv` sometimes picks webm. yt-dlp sorts on `ext` near last, so webm wins only when it beats mp4 on an earlier key. The usual cause is an mp4 stream served as HLS (`m3u8`), which yt-dlp ranks below plain https. yt-dlp then muxes the webm into a file named `clip.mp4`, so the extension lies. `yt-dlp -F` warns about a missing JS runtime (no deno). The warning is benign: extraction still works through a fallback client. When `ffmpeg` is off PATH, `uvx --from imageio-ffmpeg python -c "import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())"` prints a binary to run in its place.

## Reddit

The edge 403s scripted access, and Reddit tightens the block from time to time. Work down this ladder and stop at the first rung that returns comments.

1. **reddit-fetch, logged out.** It drives headless chromium and prints the post plus its comment tree, or a listing, as markdown:

   ```sh
   node ~/projects/reddit-fetch/reddit.mjs <url|r/sub|"search terms"> [--limit N]
   ```

   The checkout lives on the mini only. From the laptop run `ssh mini 'node ~/projects/reddit-fetch/reddit.mjs <url> --limit N'`, and put that form in a brief when the session is on the laptop. A 403 on a plain `r/<sub> --limit 3` listing means the logged-out session is blocked everywhere; go to rung 2.

2. **reddit-fetch, logged in.** Add `--load-storage <file>` with a Reddit bot storageState. The `browser-session` skill owns finding an existing file and capturing a new one; capturing needs the user to log the bot in.

3. **A Redlib mirror**, e.g. `https://safereddit.com/r/<sub>/comments/<id>/?sort=top` via `curl`/WebFetch. Mirrors come and go, and most answer scripted clients with an Anubis "Verifying your browser..." page, a 429, or a redirect. Count a mirror as working only when the body contains comment text.

4. **Ask the user** with AskUserQuestion: paste the thread text now, or set up the bot login from rung 2. Report which rungs failed and their status codes.

## Delegating

A subagent sent at one of these sources hits the same 403 and reports it as unreachable. Put the tool it needs in the brief - `~/wiki/fetching-media.md` for YouTube work, the `reddit-fetch` path for reddit research - so it starts where you would.
