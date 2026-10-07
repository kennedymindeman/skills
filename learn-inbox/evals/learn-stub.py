#!/usr/bin/env python3
"""Sandbox stand-in for the learn CLI. Records calls under ./learn-sandbox/;
touches no database, network, or ssh."""
import json
import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG = os.path.join(HERE, "learn-sandbox")
HELP = """usage: learn <command>

  inbox capture TOPIC [--why TEXT] [--source TEXT]   file one learning-inbox item
  inbox list                                         list inbox items
  _inbox-capture                                     mini-side capture, JSON on stdin
  mission start ITEM                                 start a mission from an item
  cards add TOPIC                                    draft SRS cards
  digest ITEM                                        request background digest
"""


def record(name, row):
    os.makedirs(LOG, exist_ok=True)
    with open(os.path.join(LOG, name), "a") as f:
        f.write(json.dumps(row) + "\n")


def items():
    try:
        with open(os.path.join(LOG, "inbox.jsonl")) as f:
            return [json.loads(line) for line in f]
    except FileNotFoundError:
        return []


def capture(argv):
    if not argv or argv[0].startswith("-"):
        sys.exit("learn inbox capture: TOPIC is required")
    row = {"topic": argv[0], "motivation": "", "source_material": ""}
    rest = argv[1:]
    while rest:
        flag = rest.pop(0)
        if flag not in ("--why", "--source") or not rest:
            sys.exit(f"learn inbox capture: bad argument {flag!r}")
        row["motivation" if flag == "--why" else "source_material"] = rest.pop(0)
    record("inbox.jsonl", row)
    print(f"Filed inbox item #{len(items())}: {row['topic']}")


def main(argv):
    if not argv or argv[0] in ("-h", "--help", "help"):
        print(HELP)
    elif argv[:2] == ["inbox", "capture"]:
        capture(argv[2:])
    elif argv[:2] == ["inbox", "list"]:
        for i, row in enumerate(items(), 1):
            print(f"#{i} {row['topic']}")
    elif argv[0] == "_inbox-capture":
        try:
            payload = json.loads(sys.stdin.read())
        except json.JSONDecodeError as e:
            sys.exit(f"payload rejected: {e}")
        record("inbox.jsonl", {k: payload.get(k, "") for k in ("topic", "motivation", "source_material")})
    else:
        record("other-calls.jsonl", {"argv": argv})
        print("ok")


main(sys.argv[1:])
