#!/bin/sh
# Write the clipboard's current image, served by the clipaste tunnel, to the pasted path.
set -eu

dest=${1:?usage: fetch-clipaste-image.sh <pasted path>}
mkdir -p "$(dirname "$dest")"

if curl -sf --max-time 10 -o "$dest" http://127.0.0.1:18340/clipboard/image; then
  echo "$dest"
else
  rm -f "$dest"
  echo "clipaste tunnel is down: nothing serving 127.0.0.1:18340" >&2
  exit 1
fi
