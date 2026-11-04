---
name: video
description: Produces a short narrated video (explainer, motion graphics, math animation) from a topic or script, verifies it, and publishes it with preview. Use when the user asks for a video, animation, or explainer clip.
---

# video

Make the video in code, timed to real narration audio, checked with cheap batched stills, encoded web-safe. Work in `~/scratch/<slug>/`. Sources and dates behind these choices: `references/research-2026-09.md`.

## 1. Pick the engine by content

| Content | Engine | Setup |
|---|---|---|
| Motion graphics, kinetic text, charts, UI-style scenes (default) | Remotion (React) | `export PATH=/opt/homebrew/bin:$PATH` first (node is not on the agent PATH). `npx create-video@latest --yes --blank <dir>`; `npx skills add remotion-dev/skills` and read the relevant skill files. Bundles its own ffmpeg and Chrome Headless Shell. Free for individuals. |
| Equations, geometry, plots that transform | Manim Community via uv | `uv run --with manim` (cairo/pkgconf already in Homebrew). No LaTeX installed: use `Text`, not `MathTex`, unless you install it. |
| Few static slides, a quick draft | Pillow frames piped to ffmpeg | `imageio-ffmpeg` wheel gives an ffmpeg 7.1 binary (`imageio_ffmpeg.get_ffmpeg_exe()`). |

Avoid: MoviePy (v2 broke the v1 API that models tend to write), Motion Canvas (stalled), Playwright `recordVideo` (scaled to 800px, not frame-accurate). For HTML scenes, seek then screenshot each frame. Brew ffmpeg 9 and ffprobe live in `/opt/homebrew/bin`, which the agent's default PATH omits. Set `FF=/opt/homebrew/bin/ffmpeg` and `FP=/opt/homebrew/bin/ffprobe` and use `$FF` wherever this skill says `ffmpeg`; full paths work whether or not you ran the `export` above. If they are missing, `imageio_ffmpeg.get_ffmpeg_exe()` gives an ffmpeg (no ffprobe), and inside a Remotion project `npx remotion ffmpeg` and `npx remotion ffprobe` work for simple commands. `npx remotion ffmpeg` mangles the quoting of complex `-vf`/`-filter_complex` strings, so call a real binary for those.

## 2. Script first, then audio, then timing

1. Write a one-line message ("This video tells <audience> that <point>") and a beat table: scene, beat, narration phrase, what the picture shows at that moment. A scene is one narration clip holding one or more beats; beats are the picture changes inside it. Keep 45-120 s unless asked otherwise. Check every factual number against a source before recording.
2. Show, don't tell. The narration carries the words; the screen shows the thing being said, when it is said. The user's feedback on a run that got this wrong: visuals were sometimes unrelated to the line being spoken, and there were too many words and not enough picture.
   - Every narration phrase that names a thing, change, or comparison gets a visual of that thing on screen while it is spoken: the clock ticking slower, the satellite moving, the error growing on a map. A heading or a sentence of text does not count.
   - On-screen text is labels and key numbers only: at most about 6 words per text element and 2 text elements at a time. Never put a narration sentence on screen.
   - Keep narration sentences short (under about 20 words) so each one maps to one picture.
   - Cue visual changes to the word that introduces them, using word timestamps from faster-whisper on the narration clip, not to the scene start. Start the visual about 6 frames (0.2 s) before the word so the picture lands as the word is heard.
3. Generate narration per scene, one clip per scene. The default voice is the user's Gemini custom voice "tex-raspy" (`voice_c6e1hkt5c9jr`, warm, sweet, low-to-medium female with a husky rasp, chosen 2026-09-28). This paid use is approved.
   - Run `python3 ~/.claude/skills/video/references/gemini_tts.py s1.wav "..."` per scene. It reads `~/.config/gemini/paid.key` and writes 24 kHz mono WAV. Never print the key.
   - The paid key allows about 10 requests a minute and 100 a day, so keep scripts short and run at most 3 clips at a time. The script retries 429s with backoff.
   - Designed voices sometimes add or drop words. Transcribe every clip with faster-whisper `small.en` and compare it to the scene text, treating spelled-out numbers and digits as equal. Re-synthesize any clip that differs, up to 3 tries, and report beats that still differ.
   - Keep each clip once it passes; re-renders must not re-synthesize.
   - The voice expires 2027-09-28. If the API rejects the ID, recreate it with `POST https://generativelanguage.googleapis.com/v1beta/voices`, body `{"store": true, "voice": {"model": "gemini-3.8-flash-tts", "type": "prompted", "display_name": "video-tex-raspy", "prompted": {"input": "A woman in her early 30s with a warm, sweet, affectionate voice, low-to-medium pitch, with a noticeable husky rasp and a little grit. General American English. Clear diction on numbers."}}}`, then update `VOICE` in `gemini_tts.py`. The voice-design filter blocks prompts with words like "sultry", "breathy", "intimate" or "seductive".
   - This voice reads slower than `say -r 175`; a 70 s `say` video ran about 90 s.
   - Fallback without network or key: macOS `say -r 175 -o s1.wav --file-format=WAVE --data-format=LEI16@24000 "..."`.
   - Mix the scene clips at their scene offsets into one `narration.wav` and give Remotion that single file (or mux it at encode), so audio timing cannot drift from scene timing.
4. Measure each clip's real duration and set scene length to `ceil(duration * fps) + pad` (pad about 0.4-0.8 s). Real audio duration always wins; never hand-tune scene lengths against the voice.
5. Captions (optional): word timings from `faster-whisper` (`uv run --with faster-whisper`, `word_timestamps=True`; no ffmpeg needed). Burn in or ship a `.vtt` beside the mp4.
6. Pronunciation: write numbers and symbols the way they should be spoken in the narration text ("thirty eight microseconds"), keep the on-screen text numeric.

## 3. Verify cheaply, in batches

Every image you view costs context and breaks the message cache, so batch.

- Draft render first at half resolution if the engine supports it.
- One contact sheet per check, stills at scene midpoints: `$FF -i out.mp4 -vf "fps=1/3,scale=320:-2,tile=4x3" -frames:v 1 sheet.png`, or Remotion `npx remotion still` per frame stitched with Pillow. Look for overlap, text off-frame, unreadable contrast, empty frames, and frames that are mostly text. For the relevance check, take stills at the word timestamps of the beat table and label each with the phrase being spoken; any still whose picture does not show that phrase is a fix.
- Probe the file: duration within one frame of the plan, the planned fps, `yuv420p` with `color_range=tv` (or unknown), an audio stream, `moov` before `mdat` (faststart). `$FP -v error -show_entries stream=codec_name,pix_fmt,color_range,r_frame_rate:format=duration out.mp4` shows them; `head -c 64 out.mp4 | xxd` shows `moov` near the top.
- Listen check without ears: confirm total audio duration equals the sum of scene audio plus pads, and that no scene is silent where narration was planned. Transcribe the final mix with faster-whisper `small.en` and compare it to the script; `base` drops digits in long spoken numbers.
- Fix by scene ("scene 3: labels overlap"), re-render, re-check. Stop after 3 fix rounds and report what is still wrong.

## 4. Encode

`-c:v libx264 -pix_fmt yuv420p -c:a aac -b:a 160k -movflags +faststart`, even dimensions (`scale=trunc(iw/2)*2:trunc(ih/2)*2`; odd sizes fail), 1920x1080 or 1280x720 at 30 fps. Normalize speech with `-af loudnorm=I=-16:TP=-1.5`. If music plays under the voice, duck it hard under speech; unmixed music over narration is not finished. Remotion's JPEG frame output can come out as full-range `yuvj420p` (seen with Remotion 4.0.529); if the probe shows it or `color_range=pc`, re-encode with `-pix_fmt yuv420p -color_range tv`.

## 5. Publish

Put the mp4 in a directory with an `index.html` holding `<video src="x.mp4" controls playsinline preload="metadata">`, a title, and a two-line summary with sources. Then `preview <dir> <slug>` (the `preview` skill); it exits non-zero unless the URL returns 200.

## Generative video

Only when asked, and only as B-roll composited under code-driven graphics. Every clip is a paid call: state provider, clip count, seconds, and estimated cost, and ask first. Current options: Gemini `gemini-omni-1.1-flash` (default) or Veo 3.1 (8 s clips, server copy kept 2 days, download at once), Kling 3.0 (3-15 s). The Sora 2 API was shut down on 2026-09-24.
