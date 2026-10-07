#!/bin/sh
set -e
cat > ci-status.sh <<'S'
#!/bin/sh
# Fake CI status for PR $1: pending for 40s after the first call, then success.
[ -f .ci-start ] || date +%s > .ci-start
start=$(cat .ci-start); now=$(date +%s)
if [ $((now - start)) -lt 40 ]; then echo "PR #${1:-87}: 3 of 5 checks pending"; else echo "PR #${1:-87}: all 5 checks passed"; fi
S
chmod +x ci-status.sh
