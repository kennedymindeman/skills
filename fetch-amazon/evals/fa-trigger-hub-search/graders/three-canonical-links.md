---
type: regex
pattern: "https://www\\.amazon\\.com/dp/([A-Z0-9]{10})(?![\\w/?%-])[\\s\\S]*?https://www\\.amazon\\.com/dp/(?!\\1)([A-Z0-9]{10})(?![\\w/?%-])[\\s\\S]*?https://www\\.amazon\\.com/dp/(?!\\1|\\2)[A-Z0-9]{10}(?![\\w/?%-])"
weight: 2
---
