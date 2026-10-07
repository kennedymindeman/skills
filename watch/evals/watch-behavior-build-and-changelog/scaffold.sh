#!/bin/sh
set -e
cat > long_job.sh <<'JOB'
#!/bin/sh
# Simulated release build: takes about 45 seconds.
sleep 45
echo "build ok: 42 targets" > output.log
JOB
chmod +x long_job.sh
printf '# Changelog\n\n## 1.3.0\n\n- Added dark mode.\n' > CHANGELOG.md.orig
