---
name: possessions
description: Tracks and reviews problems with the user's expensive possessions on their ~/wiki pages. Use on "review my stuff", on the monthly possessions lint, or whenever a conversation touches something they own - the car, the 3D printer - with a complaint, a symptom, a repair, or shopping for a replacement.
---

An expensive thing's real cost is the problem nobody wrote down: it gets tolerated for years, and then the replacement is bought with the same flaw. So every encounter with something the user owns exists to get one more problem named, tagged, and onto its page - the conversation forgets, the page does not.

## Start at the page

Everything owned has a wiki page listed under **Possessions** in `~/wiki/index.md`. When a conversation touches one of them, read that page before answering: it already holds what has been tried, what was ruled out on that unit, and the questions waiting to be asked.

A page carries three kinds of material - **Problems**, each tagged with a status line; the criteria for the next one of that thing; and **Open questions**, an interview queue any session may pull from.

## Ask the open questions

Open questions sit on the page because they need the user, not inference. Ask them where the item comes up, with concrete options when the answer is a choice, a few at a time rather than as one long list.

An answered question does not stay answered in place: move the answer into Problems (or into the next-one criteria) and delete the question. A question left standing after its answer is what makes the next session re-ask it.

## Tag every complaint fix or buy-criterion

A new complaint goes under Problems on the item's page, not only into the reply, tagged by whether this unit can change:

- **fix** - solvable on the thing already owned. Write the things to try cheapest-first, and a status line saying where that stands (`not yet tried`, `tried, no change`, `resolved`).
- **buy-criterion** - not fixable on this unit, like a car with no rear wiper. Say what to require instead when buying the next one, and mirror it into that page's next-one criteria so it survives as a positive requirement.

The tag is the whole point of writing it down: one says keep working the problem, the other says stop and remember it at purchase time.

## Run the lint

The lint runs on "review my stuff" and roughly monthly. Its checklist of record is `~/wiki/possessions-review.md` - read it and work it page by page, across every item under Possessions.

The step that earns the pass is the category sweep: visibility and safety, comfort, noise, cost to run, wear that will show at resale, and anything being tolerated without a name. Open questions only surface what some past session already noticed; the sweep is the only part that reaches what nobody has named yet, so it runs on every page even when that page's questions are all answered. Anything expensive bought since the last pass gets its page created in the same pass.

The pass is done when every Possessions page has been through both - its own questions and the sweep - and every **fix (unresolved)** problem has been asked whether its next step was tried, with the status advanced either way.

## Close the pass

Log the pass in `~/wiki/log.md`, update the last-lint line on `~/wiki/possessions-review.md`, commit, and push. An unlogged pass reads as never done, and the next one spends its first questions on answers already given.
