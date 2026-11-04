"""Synthesize one narration clip with a Gemini custom voice.

Usage: python3 gemini_tts.py OUT.wav "text" [voice_id]
Reads the paid key from ~/.config/gemini/paid.key. Writes 24 kHz mono 16-bit WAV.
"""

import base64
import json
import pathlib
import sys
import time
import urllib.error
import urllib.request
import wave

MODEL = "gemini-3.8-flash-tts"
VOICE = "voice_c6e1hkt5c9jr"  # "tex-raspy", the user's default (2026-09-28); expires 2027-09-28
URL = "https://generativelanguage.googleapis.com/v1beta/interactions"


def find_audio(o):
    if isinstance(o, dict):
        for k, v in o.items():
            if k == "data" and isinstance(v, str) and len(v) > 1000:
                return v
            if r := find_audio(v):
                return r
    if isinstance(o, list):
        for v in o:
            if r := find_audio(v):
                return r


def synth(text, out, voice=VOICE):
    key = (pathlib.Path.home() / ".config/gemini/paid.key").read_text().strip()
    body = json.dumps(
        {
            "model": MODEL,
            "input": text,
            "response_format": {"type": "audio"},
            "generation_config": {"speech_config": [{"voice": voice}]},
        }
    ).encode()
    for i in range(6):
        req = urllib.request.Request(
            URL,
            data=body,
            headers={"x-goog-api-key": key, "Content-Type": "application/json"},
        )
        try:
            resp = json.load(urllib.request.urlopen(req, timeout=180))
            break
        except urllib.error.HTTPError as e:
            if e.code not in (429, 500, 502, 503, 504):
                sys.exit(f"{e.code} {e.read()[:400]!r}")
            time.sleep(min(60, 8 * 2**i))
    else:
        sys.exit("gave up after retries")
    b64 = find_audio(resp)
    if not b64:
        sys.exit(f"no audio in response: {json.dumps(resp)[:400]}")
    raw = base64.b64decode(b64)
    if raw[:4] == b"RIFF":
        pathlib.Path(out).write_bytes(raw)
        return
    with wave.open(str(out), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(24000)
        w.writeframes(raw)


if __name__ == "__main__":
    if len(sys.argv) not in (3, 4):
        sys.exit(__doc__)
    synth(sys.argv[2], sys.argv[1], *sys.argv[3:4])
