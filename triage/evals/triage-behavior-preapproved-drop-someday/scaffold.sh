#!/bin/sh
set -e
# The eval sandbox gives each run its own HOME; refuse to touch a real inbox.
[ ! -e "$HOME/inbox" ] || { echo "refusing: $HOME/inbox already exists" >&2; exit 1; }
mkdir inbox
printf '# inbox\n\nThought dumps land here, unsorted.\n' > inbox/README.md
cat > inbox/2026-09-02-0815-parking-permit.md <<'DUMP'
---
captured: 2026-09-02T08:15
source: phone dump
---
renew the office parking permit before it lapses on sept 1
DUMP
cat > inbox/2026-09-03-2210-kayak-trip.md <<'DUMP'
---
captured: 2026-09-03T22:10
source: phone dump
---
kayak trip down the river next summer? would need to rent boats
DUMP
git -C inbox init -q
git -C inbox add README.md
git -C inbox commit -qm "Start inbox"
# The skill works on ~/inbox; point it at the copy inside the case cwd so graders can see moves.
ln -s "$PWD/inbox" "$HOME/inbox"
