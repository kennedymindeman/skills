# Sourced by each case's scaffold.sh: installs the learn stand-in in the cwd.
mkdir -p bin learn-app learn-sandbox
cp "$(dirname "$0")/../learn-stub.py" bin/learn
chmod +x bin/learn
cat > learn-app/CONTEXT.md <<'MD'
# learn glossary (sandbox copy)

- **Learning inbox**: the app-owned list of captured intents. Not a queue.
- **Inbox item**: one captured intent. Not a card candidate.
- **Consumed**: an item's exit, by a mission started from it or an explicit decline.
- **Digest**: background enrichment that maps an item into the concept graph.
- **Mission**: the teaching engagement an item can become.
MD
