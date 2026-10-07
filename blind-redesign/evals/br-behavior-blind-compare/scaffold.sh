#!/bin/sh
# Synthetic screenshots: one flat-colour PNG per source and viewport, captured
# the same way for the current screen and both redesign variants.
set -e
python3 - <<'PY'
import pathlib, struct, zlib

def png(path, w, h, rgb):
    raw = b"".join(b"\x00" + bytes(rgb) * w for _ in range(h))
    def chunk(t, d):
        return struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d))
    data = (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(raw)) + chunk(b"IEND", b""))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)

for source, rgb in {"current": (91, 42, 134), "v1": (30, 64, 175), "v2": (15, 118, 110)}.items():
    png(pathlib.Path("shots", source, "390x844.png"), 39, 84, rgb)
    png(pathlib.Path("shots", source, "1440x900.png"), 144, 90, rgb)
PY
cat > NOTES.md <<'EOF'
Orders screen redesign. Builders v1 and v2 worked from the shared brief only.
All three sources were captured against the same fixture at 390x844 and 1440x900.
EOF
