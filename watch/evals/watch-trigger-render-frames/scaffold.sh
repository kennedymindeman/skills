#!/bin/sh
set -e
cat > render.sh <<'S'
#!/bin/sh
# Fake renderer: writes one PNG every 1.5 seconds, 30 frames total.
mkdir -p frames
i=1
while [ $i -le 30 ]; do
  sleep 1.5
  printf '\211PNG\r\n\032\n' > "frames/frame_$(printf %03d $i).png"
  i=$((i + 1))
done
S
chmod +x render.sh
