---
type: regex
target: {source: file, path: site/Caddyfile}
pattern: 'notes\.example\.test \{[^}]*localhost:8090[^}]*\}[\s\S]*localhost:8070'
---
