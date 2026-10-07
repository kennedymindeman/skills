---
type: regex
target: trace
match: not_contains
pattern: '"name":"(?:Read|Bash|Grep|Glob)","input":\{[^\n]*static/orders\.html[^\n]*"parent_tool_use_id":"toolu_'
arm: both
weight: 2
---
