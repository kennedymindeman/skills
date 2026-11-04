#!/usr/bin/env python3
"""Build a blind comparison page from per-source screenshot folders.

    compare.py OUT_DIR SOURCE=SHOTS_DIR [SOURCE=SHOTS_DIR ...]

Each SHOTS_DIR holds one PNG per viewport, named the same in every folder
(390x844.png, 1440x900.png, or the simulator's name). Sources get shuffled
neutral names (Amber, Cobalt, ...) that say nothing about where a design came
from. OUT_DIR/index.html shows only those names, with every image inlined. The
name-to-source key goes to OUT_DIR.key.txt beside OUT_DIR, never
inside it, so serving OUT_DIR does not publish the key.
"""

import base64
import html
import random
import sys
from pathlib import Path

NAMES = (
    "Amber", "Cobalt", "Coral", "Fern", "Indigo", "Jade",
    "Maple", "Olive", "Pearl", "Slate", "Teal", "Umber",
)


def main() -> None:
    args = sys.argv[1:]
    if len(args) < 3 or not all("=" in a for a in args[1:]):
        sys.exit(__doc__)
    out = Path(args[0]).resolve()
    sources = dict(a.split("=", 1) for a in args[1:])
    if len(sources) != len(args) - 1:
        sys.exit("each SOURCE name must be unique")
    if len(sources) > len(NAMES):
        sys.exit(f"at most {len(NAMES)} sources")
    sets = {n: {p.name for p in Path(d).glob("*.png")} for n, d in sources.items()}
    shots = sorted(set().union(*sets.values()))
    uneven = [n for n, s in sets.items() if s != set(shots)]
    if not shots or uneven:
        sys.exit(f"every folder needs the same PNGs; check: {uneven or list(sources)}")
    rng = random.SystemRandom()
    names = list(sources)
    rng.shuffle(names)
    labels = dict(zip(rng.sample(NAMES, len(names)), names))

    sections = []
    for shot in shots:
        cells = []
        for label, name in labels.items():
            png = Path(sources[name]) / shot
            data = base64.b64encode(png.read_bytes()).decode()
            img = (
                f'<img alt="{label}" src="data:image/png;base64,{data}"'
                " onclick=\"this.parentNode.classList.toggle('big')\">"
            )
            cells.append(f"<figure><figcaption>{label}</figcaption>{img}</figure>")
        sections.append(
            f"<h2>{html.escape(shot[:-4])}</h2><div class=row>{''.join(cells)}</div>"
        )

    out.mkdir(parents=True, exist_ok=True)
    (out / "index.html").write_text(
        "<!doctype html><meta charset=utf-8>"
        '<meta name=viewport content="width=device-width, initial-scale=1">'
        "<title>Blind comparison</title><style>"
        "body{font:16px/1.5 system-ui,sans-serif;margin:24px;background:#f4f4f4;color:#111}"
        ".row{display:flex;flex-wrap:wrap;gap:24px;align-items:flex-start;padding-bottom:12px}"
        "figure{margin:0;flex:1 1 0;min-width:280px}figure.big{flex-basis:100%}"
        "img{cursor:zoom-in}.big img{cursor:zoom-out}"
        "figcaption{font-weight:700;font-size:24px;margin-bottom:6px}"
        "img{display:block;border:1px solid #999;max-width:100%;height:auto}"
        "</style><h1>Blind comparison</h1>"
        "<p>Pick a design by name before opening the key. Click a shot to enlarge it.</p>"
        + "".join(sections)
    )
    key = out.parent / f"{out.name}.key.txt"
    key.write_text("".join(f"{k}: {v}\n" for k, v in labels.items()))
    print(out / "index.html")
    print(key)


if __name__ == "__main__":
    main()
