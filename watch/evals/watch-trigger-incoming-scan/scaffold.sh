#!/bin/sh
set -e
mkdir incoming
# Simulated scp: the scan lands about 40 seconds after setup.
nohup sh -c 'sleep 40; head -c 48213 /dev/zero > incoming/scan-0412.pdf.part; mv incoming/scan-0412.pdf.part incoming/scan-0412.pdf' >/dev/null 2>&1 &
