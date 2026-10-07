---
type: regex
target: trace
pattern: '(?:"name":"(?:Edit|Write|MultiEdit)","input":\{[^}]*?"file_path":"[^"]*Caddyfile"|"name":"Bash","input":\{[^}]*?"command":"(?:[^"\\]|\\.)*?(?:sed\s+-i|perl\s+-\w*i|>\s*[\w./~-]*Caddyfile)(?:[^"\\]|\\.)*?Caddyfile)[\s\S]*"name":"Bash","input":\{[^}]*?"command":"(?:[^"\\]|\\.)*?(?:inbox capture|_inbox-capture)'
---
