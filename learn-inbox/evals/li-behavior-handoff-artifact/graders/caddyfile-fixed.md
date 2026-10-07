---
type: regex
target: {source: file, path: site/Caddyfile}
pattern: 'notes\.example\.test \{[^}]*(?:localhost|127\.0\.0\.1)?:8090[^}]*\}[\s\S]*localhost:8070'
---
