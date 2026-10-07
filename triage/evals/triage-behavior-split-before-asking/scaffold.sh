#!/bin/sh
set -e
# The eval sandbox gives each run its own HOME; refuse to touch a real inbox.
[ ! -e "$HOME/inbox" ] || { echo "refusing: $HOME/inbox already exists" >&2; exit 1; }
mkdir inbox
printf '# inbox\n\nThought dumps land here, unsorted.\n' > inbox/README.md
cat > inbox/2026-09-10-0732-few-things.md <<'DUMP'
---
captured: 2026-09-10T07:32
source: phone dump
---
few things before i forget. the nas backup job logs to /var/log/restic.log now, not syslog. also i want to actually understand how bloom filters work, they came up in the postgres docs. and the photo-renamer script needs a --dry-run flag before i point it at the real library
DUMP
cat > inbox/2026-09-11-1915-bloom-filters.md <<'DUMP'
---
captured: 2026-09-11T19:15
source: phone dump
---
bloom filters - how do they actually work? false positives but no false negatives??
DUMP
git -C inbox init -q
git -C inbox add README.md
git -C inbox commit -qm "Start inbox"
# The skill works on ~/inbox; point it at the copy inside the case cwd so graders can see moves.
ln -s "$PWD/inbox" "$HOME/inbox"
