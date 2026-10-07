#!/bin/sh
set -e
. "$(dirname "$0")/../sandbox-setup.sh"
mkdir -p site
cp "$(dirname "$0")/Caddyfile" "$(dirname "$0")/app.env" site/
