#!/bin/zsh
# Autonomous triage runner, invoked hourly by launchd.
# Launches Claude only when the inbox root holds a dump, so idle hours
# never touch Fable usage. Runs on Fable with no fallback: if Fable is
# out of usage the run fails and is logged, rather than downgrading.
#
# Usage: auto-triage.sh [dry-run|execute]   (default: dry-run)
set -u

# Interactive aliases (ls -> eza) have hung this script's listings. Drop every
# alias up front, and list with zsh globs or find rather than ls. The commands
# below are still ordinary PATH lookups; unalias is what keeps them honest.
unalias -a 2>/dev/null

INBOX="${AUTO_TRIAGE_INBOX:-$HOME/inbox}"
CLAUDE="${AUTO_TRIAGE_CLAUDE:-/Users/kennedy/.local/bin/claude}"
RUNLOG="$INBOX/auto-triage-runs.log"
DECISIONLOG="$INBOX/auto-triage.log"
# Outside $INBOX on purpose: the pass commits the inbox with `add -A`, and
# this marker is machine state, not inbox content.
COOLDOWN_FILE="${TMPDIR:-/tmp}/auto-triage-cooldown"
MODE="${1:-dry-run}"
# Production runs on Fable with no fallback. Override for a manual off-Fable
# test or a degraded pass: AUTO_TRIAGE_MODEL=claude-opus-4-8 auto-triage.sh ...
MODEL="${AUTO_TRIAGE_MODEL:-claude-fable-5}"
# An item deferred this many times is parked in someday/ instead of being
# re-read every hour; the next interactive pass re-offers it.
MAX_DEFERS="${AUTO_TRIAGE_MAX_DEFERS:-5}"
# A hung claude call or git commit ends this run, not the hour.
RUN_TIMEOUT="${AUTO_TRIAGE_TIMEOUT:-1800}"
GIT_TIMEOUT=120
# Out of Fable usage: skip this many seconds of hourly runs before retrying.
COOLDOWN_SECONDS="${AUTO_TRIAGE_COOLDOWN:-21600}"

ts() { date '+%Y-%m-%d %H:%M:%S'; }

# A typo'd override must not break parking or the cooldown arithmetic: any
# non-integer falls back to the default.
num() {
  case "$1" in (""|*[!0-9]*) print -r -- "$2" ;; (*) print -r -- "$1" ;; esac
}
MAX_DEFERS=$(num "$MAX_DEFERS" 5)
RUN_TIMEOUT=$(num "$RUN_TIMEOUT" 1800)
COOLDOWN_SECONDS=$(num "$COOLDOWN_SECONDS" 21600)

# gtimeout (coreutils) when present, perl's alarm otherwise.
run_limited() {
  local secs=$1; shift
  if command -v gtimeout >/dev/null 2>&1; then
    gtimeout "$secs" "$@"
  else
    perl -e 'alarm shift; exec @ARGV' "$secs" "$@"
  fi
}

# Cooldown: a previous run hit the usage limit, so skip until it expires.
if [ -f "$COOLDOWN_FILE" ]; then
  until_epoch=$(cat "$COOLDOWN_FILE" 2>/dev/null)
  case "$until_epoch" in (*[!0-9]*|"") until_epoch=0 ;; esac
  if [ "$(date +%s)" -lt "$until_epoch" ]; then
    # One line so a throttled hour is distinguishable from a dead launchd job.
    echo "[$(ts)] throttled: out of usage until $(date -r "$until_epoch" '+%Y-%m-%d %H:%M:%S')" >> "$RUNLOG"
    exit 0
  fi
  rm -f "$COOLDOWN_FILE"
fi

# Guard: any dump in the inbox root (ignore README, archive/, someday/).
items=$(find "$INBOX" -maxdepth 1 -name '*.md' ! -name 'README.md' 2>/dev/null)
if [ -z "$items" ]; then
  exit 0
fi

echo "[$(ts)] start auto-triage ($MODE)" >> "$RUNLOG"

out=$(mktemp -t auto-triage)
run_limited "$RUN_TIMEOUT" "$CLAUDE" \
  -p "Run the triage skill in autonomous $MODE mode, exactly as defined in its 'Autonomous mode' section. Process $INBOX." \
  --model "$MODEL" \
  --permission-mode bypassPermissions \
  > "$out" 2>&1
rc=$?
cat "$out" >> "$RUNLOG"

# Out of usage: start a cooldown instead of retrying every hour. The session
# limit message carries its own reset time ("resets 4:40am"); we ignore it and
# use one fixed window rather than parsing a localised clock string.
if [ $rc -ne 0 ] && grep -qiE "hit your (session|usage) limit|usage limit|out of (usage|credit)|credit balance is too low|insufficient credit" "$out"; then
  echo $(( $(date +%s) + COOLDOWN_SECONDS )) > "$COOLDOWN_FILE"
  echo "[$(ts)] out of usage; skipping runs for ${COOLDOWN_SECONDS}s" >> "$RUNLOG"
fi
rm -f "$out"

# Park items the autonomous pass keeps deferring. Each defer writes one
# "<file>  ->  DEFER" line to the decision log, so the log is the count. The
# count restarts at the item's last PARKED line: a file a person pulls back
# out of someday/ gets a fresh budget instead of being parked again at once.
parked=0
if [ "$MODE" = execute ] && [ -f "$DECISIONLOG" ]; then
  for f in "$INBOX"/*.md(N); do
    base=${f##*/}
    [ "$base" = README.md ] && continue
    defers=$(awk -v pre="  $base  ->  " '
      index($0, pre "someday/ (PARKED") { n = 0; next }
      index($0, pre "DEFER")            { n++ }
      END { print n + 0 }' "$DECISIONLOG")
    [ "$defers" -ge "$MAX_DEFERS" ] || continue
    mkdir -p "$INBOX/someday"
    # -n: never clobber an older someday/ file of the same name.
    mv -n "$f" "$INBOX/someday/"
    if [ -e "$f" ]; then
      echo "[$(ts)] park refused, someday/$base already exists: $base" >> "$RUNLOG"
      continue
    fi
    echo "$(date -u '+%Y-%m-%dT%H:%M:%SZ')  $base  ->  someday/ (PARKED after $defers defers; awaiting interactive pass)" >> "$DECISIONLOG"
    parked=$((parked + 1))
  done
fi
if [ "$parked" -gt 0 ]; then
  # The move already happened; the commit is best-effort, so say which it was.
  # An uncommitted move is picked up by the next pass's `add -A`.
  crc=1
  if run_limited "$GIT_TIMEOUT" git -C "$INBOX" add -A; then
    run_limited "$GIT_TIMEOUT" git -C "$INBOX" commit -q -m "Triage: park $parked item(s) after $MAX_DEFERS defers"
    crc=$?
  fi
  if [ $crc -eq 0 ]; then
    echo "[$(ts)] parked $parked item(s) to someday/, committed" >> "$RUNLOG"
  else
    echo "[$(ts)] parked $parked item(s) to someday/, commit failed (rc=$crc); inbox left dirty" >> "$RUNLOG"
  fi
fi

echo "[$(ts)] end auto-triage ($MODE) exit=$rc" >> "$RUNLOG"
exit $rc
