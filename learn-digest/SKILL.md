---
name: learn-digest
description: Files what a conversation taught into the learn app's learning inbox, one item per concept, carrying the passages that explain each. Use on "digest this chat into learn", "add what we just covered to learn", "save this explanation for learn", or when asked to keep a substantive explanation, research finding, debugging insight, or decision and its rationale as learning material. For one topic, or for handing off work an agent just did, use learn-inbox instead.
---

An explanation given in chat is gone when the session clears: the user understood it once, in context, with nothing to review and nothing to practise against. The learning inbox is where it survives - but only if it arrives as material the app can teach from. So this skill does two things and stops: pull the concepts out of the conversation, and file each one with the passage that explains it. Everything after that - mapping the concepts into the graph, routing them, drafting cards, running a mission - is learn's, and happens later on the review page.

## Pull the concepts out

A conversation is not one item. File one item per concept, where a concept is a thing that can be known on its own and depended on by the next one - "how a squash-merge rewrites the commits a branch was based on", not "the git conversation".

Two kinds are worth filing, and the second is the one that gets missed:

- What the conversation **taught** - the explanations, the finding, the insight that ended the debugging, the decision and the reasoning behind it.
- What it **relied on** - the ideas the explanation leaned on without explaining, because they were assumed. Those are the prerequisites, and they are why an explanation that landed in the moment does not survive on its own.

Order them dependency-first: the concept another one needs goes in before the one that needs it. Then one **umbrella item** last, for the goal the whole conversation was in service of - the thing the user was actually trying to be able to do - with the concepts it sits on named in its motivation.

That order is the whole signal this skill sends. It does not build prerequisite edges, split routes, or decide what the user already knows; learn's digest step infers edges from the items and the review page does the rest.

## Fill each item

Three fields per item, the same shape `learn-inbox` files:

- **topic** - the concept, in the words the conversation used for it.
- **`--why`** - what made it matter here: the question that was asked, the bug it explained, the decision it settled.
- **`--source`** - the passages of the chat that explain this concept, condensed to around 2 KB.

The source material is the teaching material, so quote the explanation rather than summarising it: the worked example, the concrete numbers, the analogy that landed, the correction where a first answer turned out wrong. What to drop is everything a lesson would not use - the back-and-forth getting to the question, tool calls and their output, the parts of the exchange that went nowhere. When one concept's explanation is longer than the cap, keep the worked example and cut the restatement around it.

## File them and say what was filed

Each item goes through `learn-inbox`'s capture call - `learn inbox capture "<topic>" --why "..." --source "..."` from the laptop, and the mini-side stdin form on the mini. Read that skill for the exact commands and the host split before filing; it also owns what capture does and does not set in motion.

Then one report at the end: the topics filed, in the order they went in, umbrella last. One line each, no summary of the material - the user just had the conversation.

## Digestion is the app's step

Capture stays inert here exactly as it does in `learn-inbox`: no mission started, no SRS cards drafted from the passages, no wiki page written, and no digest requested - digest is the app's own background step over the items, not something a chat session sets off.

The word is the trap: to *digest a chat* is this skill filing items, while **Digest** in `~/projects/learn/CONTEXT.md` is the app enriching an item into the concept graph afterwards. Read that glossary before writing anything the user reads about either.
