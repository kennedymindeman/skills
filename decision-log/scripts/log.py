#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Append one row to a decision-log TSV.

Usage: log.py <logfile> <phase> <decision> <why> <evidence> <result>
"""

import sys
from datetime import datetime, timezone
from pathlib import Path

HEADER = "ts\tphase\tdecision\twhy\tevidence\tresult\n"
USAGE = "usage: log.py <logfile> <phase> <decision> <why> <evidence> <result>"


def clean(cell):
    cell = cell.replace("\t", " ").replace("\r", " ").replace("\n", " ")
    # Reviewers open the log in spreadsheets, and cells can carry generated or
    # attacker-controlled text (PR titles, filenames), so a leading formula
    # character must not execute.
    return "'" + cell if cell[:1] in ("=", "+", "-", "@") else cell


def append(logfile, cells, now=None):
    path = Path(logfile)
    path.parent.mkdir(parents=True, exist_ok=True)
    ts = (now or datetime.now(timezone.utc)).strftime("%Y-%m-%dT%H:%M:%SZ")
    # Append mode only: a failed emptiness check costs a stray header line,
    # never the existing rows.
    with path.open("a", encoding="utf-8", newline="") as f:
        if f.tell() == 0:
            f.write(HEADER)
        f.write("\t".join([ts, *map(clean, cells)]) + "\n")


def main(argv):
    if len(argv) != 7:
        print(USAGE, file=sys.stderr)
        return 1
    append(argv[1], argv[2:])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
