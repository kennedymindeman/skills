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

Reddit blocks every logged-out request, JSON and HTML alike, from any IP. Read it through the Redlib mirror red.artemislena.eu with curl's own user agent; the mirror serves browser user agents an Anubis challenge and curl the page:

```sh
curl -s -A 'curl/8.7.1' 'https://red.artemislena.eu/r/<sub>/comments/<id>/?sort=top'   # thread
curl -s -A 'curl/8.7.1' 'https://red.artemislena.eu/r/<sub>/top?t=week'               # listing
curl -s -A 'curl/8.7.1' 'https://red.artemislena.eu/r/<sub>/search?q=<terms>&restrict_sr=on&sort=new'
```

Swap `www.reddit.com` for the mirror host and keep the path; the thread path needs its leading `/`. The mirror returns HTML only. Post text sits in `post_title` and `post_body`, comments in `comment` blocks with `comment_author`, `comment_score`, and `comment_body`, and replies nest under `replies`. The fetch worked when the body contains `comment_body`. When it holds a challenge page, a 429, or a redirect instead, report the status and ask the user to paste the thread.

## Delegating

A subagent sent at one of these sources hits the same 403 and reports it as unreachable. Put the tool it needs in the brief - `~/wiki/fetching-media.md` for YouTube work, the mirror curl line for reddit research - so it starts where you would.
