#!/bin/sh
set -e
cat > issues.json <<'JSON'
[
  {"id": 101, "title": "Saving a draft twice deletes the earlier draft", "body": "Repro: write a draft, save, edit, save again. The first version is gone from history and cannot be restored."},
  {"id": 102, "title": "Typo on settings page", "body": "'Notifcations' should be 'Notifications'."},
  {"id": 103, "title": "Export to CSV is slow for large projects", "body": "A 50k-row export takes about 40 seconds. It does finish."},
  {"id": 104, "title": "Dark mode toggle resets after logout", "body": "Preference is not persisted across sessions."}
]
JSON
