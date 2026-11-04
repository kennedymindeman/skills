# Agent video generation: research notes (2026-09-27)

Sources behind the `video` skill. Confidence and dates as found on 2026-09-27.

## Engines

- Remotion: official [Agent Skills](https://www.remotion.dev/docs/ai/skills) (`npx skills add remotion-dev/skills`) and [Claude Code plugin](https://www.remotion.dev/docs/ai/claude-code-plugin). Bundles ffmpeg 7.1 since v4 ([docs](https://www.remotion.dev/docs/ffmpeg)) and installs Chrome Headless Shell into node_modules. Defaults: H.264, `yuv420p` ([pixel-format.ts](https://github.com/remotion-dev/remotion/blob/main/packages/renderer/src/pixel-format.ts)), faststart. [License](https://github.com/remotion-dev/remotion/blob/main/LICENSE.md): free for individuals and companies up to 3 employees. Its [voiceover skill](https://github.com/remotion-dev/skills/blob/main/skills/remotion-markup/voiceover.md) sizes scenes from `getAudioDuration()` and defaults to ElevenLabs. Its render skill has no visual self-check loop.
- HyperFrames (HeyGen, HTML + GSAP, Apache-2.0): [repo](https://github.com/heygen-com/hyperframes). Needs Node 22+ and ffmpeg (`HYPERFRAMES_FFMPEG_PATH`). Most complete published agent loop: [production-loop.md](https://github.com/heygen-com/hyperframes/blob/main/skills/hyperframes/references/production-loop.md) (audio -> duration sync -> lint/check -> contact sheet -> deliver; "real duration wins") and [review-loop.md](https://github.com/heygen-com/hyperframes/blob/main/skills/hyperframes/references/review-loop.md) (storyboard first). Deterministic capture is Linux-first per their [research post](https://www.heygen.com/research/html-to-video).
- Manim Community: dropped external ffmpeg for PyAV in [0.19.0](https://docs.manim.community/en/stable/changelog/0.19.0-changelog.html); [uv install](https://docs.manim.community/en/stable/installation/uv.html) needs cairo + pkg-config. [manim-voiceover](https://github.com/ManimCommunity/manim-voiceover) triggers animations on words.
- MoviePy v2 removed `moviepy.editor` and renamed `set_*` to `with_*` ([migration](https://zulko.github.io/moviepy/getting_started/updating_to_v2.html)); models write v1 code. Motion Canvas last stable release 2024-12. Playwright `recordVideo` scales to fit 800x800 ([docs](https://playwright.dev/docs/videos)).
- Editing existing footage is a separate category: [browser-use/video-use](https://github.com/browser-use/video-use) (transcript + filmstrip images, re-render up to 3 times).

## ffmpeg without a system install

- [imageio-ffmpeg](https://github.com/imageio/imageio-ffmpeg): ffmpeg 7.1 for macOS arm64 with libx264, aac, drawtext, subtitles, loudnorm, tile. No ffprobe. Verified locally.
- [static_ffmpeg](https://github.com/zackees/static_ffmpeg): ffmpeg + ffprobe, downloads on first use. Not run locally.
- Odd frame dimensions fail with libx264 (`width not divisible by 2`); verified locally. `yuv420p` and `+faststart` per the [ffmpeg H.264 wiki](https://trac.ffmpeg.org/wiki/Encode/H.264).

## Voice and captions

- ElevenLabs [`with-timestamps`](https://elevenlabs.io/docs/api-reference/text-to-speech/convert-with-timestamps) is the hosted TTS that returns character timings. [OpenAI TTS](https://developers.openai.com/api/docs/guides/text-to-speech) (requires AI-voice disclosure) and [Gemini TTS](https://ai.google.dev/gemini-api/docs/speech-generation) return audio only.
- Local: macOS `say` (verified), [kokoro-onnx](https://github.com/thewh1teagle/kokoro-onnx) (MIT, near real time on M1; not run locally), Piper is now GPL-3.0 ([piper1-gpl](https://github.com/OHF-Voice/piper1-gpl)).
- [faster-whisper](https://github.com/SYSTRAN/faster-whisper) gives word timestamps and decodes with PyAV, no ffmpeg.

## Verification cost

Images in the conversation invalidate the messages prompt cache ([Anthropic prompt caching](https://docs.claude.com/en/docs/build-with-claude/prompt-caching)), so batch stills into one contact sheet per check.

## Generative video (as of 2026-09-27)

- OpenAI Sora 2 API shut down 2026-09-24 ([video guide](https://developers.openai.com/api/docs/guides/video-generation)).
- Google: [Gemini Omni Flash](https://ai.google.dev/gemini-api/docs/omni) is the recommended default; [Veo 3.1](https://ai.google.dev/gemini-api/docs/veo) for extension and frame control, 4/6/8 s clips, stored 2 days.
- [Kling 3.0](https://kling.ai/quickstart/klingai-video-3-model-user-guide): 3-15 s with native audio. Runway's API now also resells third-party models ([models](https://docs.dev.runwayml.com/guides/models/)).

## Gaps

No quantitative data on agent failure rates per engine. Remotion adoption numbers are from secondary write-ups only. HyperFrames determinism on macOS, kokoro-onnx, static-ffmpeg, Manim, and Remotion renders were not run during the research.
