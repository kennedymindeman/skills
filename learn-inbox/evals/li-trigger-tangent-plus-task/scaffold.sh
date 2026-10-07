#!/bin/sh
set -e
. "$(dirname "$0")/../sandbox-setup.sh"
cp "$(dirname "$0")/etl.py" .
