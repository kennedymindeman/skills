#!/bin/sh
set -e
# The eval sandbox runs this with a throwaway HOME under a temp dir and the case cwd inside it; refuse anywhere else.
case "$HOME" in /tmp/?*|/private/tmp/?*|"${TMPDIR:-/nonexistent}"/?*) ;; *) echo "refusing: HOME=$HOME is not an eval sandbox" >&2; exit 1 ;; esac
case "$PWD" in "$HOME"/?*) ;; *) echo "refusing: $PWD is not under $HOME" >&2; exit 1 ;; esac
if [ -e "$HOME/inbox" ] || [ -L "$HOME/inbox" ]; then echo "refusing: $HOME/inbox already exists" >&2; exit 1; fi
mkdir inbox
printf '# inbox\n\nThought dumps land here, unsorted.\n' > inbox/README.md
cat > inbox/2026-09-14-2105-zfs-scrub.md <<'DUMP'
---
captured: 2026-09-14T21:05
source: phone dump
---
the home server's zfs scrub runs sundays at 3am, cron is in /etc/cron.d/zfs-scrub
DUMP
cat > inbox/2026-09-15-1240-recipe-app-export.md <<'DUMP'
---
captured: 2026-09-15T12:40
source: phone dump
---
recipe app: add an export-to-markdown button, people keep asking
DUMP
cat > inbox/2026-09-16-0650-sourdough.md <<'DUMP'
---
captured: 2026-09-16T06:50
source: phone dump
---
try a sourdough starter at some point, no rush
DUMP
git -C inbox init -q
git -C inbox add README.md
git -C inbox commit -qm "Start inbox"
# The skill works on ~/inbox; point it at the copy inside the case cwd so graders can see moves.
ln -s "$PWD/inbox" "$HOME/inbox"
