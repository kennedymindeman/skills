---
type: llm
---

The final message is a brief for a subagent that will read a .pptx file.

PASS if the brief tells the subagent how to get the slide text out as text - for example by naming a text-extraction library or command such as python-pptx, a script that walks slide shapes, or a conversion to text - rather than leaving the method unspecified.
FAIL if the brief only says to "read", "open", or "review" the deck without naming a text-extraction method, or tells it to look at the slides as images or screenshots.
