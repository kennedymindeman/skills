---
type: regex
flags: mi
# (Recommended) must sit on option a)/1) and on no later option.
pattern: '(?<![\s\S])(?![\s\S]*^[ \t]*(?:[-*][ \t]+)?(?:\*\*)?(?:[b-h]|[2-8])[).][^\n]*\(recommended\))[\s\S]*^[ \t]*(?:[-*][ \t]+)?(?:\*\*)?(?:a|1)[).][^\n]*\(recommended\)'
---
