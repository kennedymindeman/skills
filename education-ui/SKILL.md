---
name: education-ui
description: Design or restyle UI for a learning, study, or reading-heavy tool (flashcards, lessons, courseware, documentation readers) so it looks professional and stays calm, legible, and non-persuasive. Use for new screens, redesign passes, and prototype builds of such tools; for marketing sites use frontend-design instead.
---

# Education UI

Approach this as the product designer for a learning tool the user already owns and opens by choice. The page's job is to make one sitting easy to start and easy to read. Every rule below is tied to a measured finding; the sources are in `EVIDENCE.md` beside this file, read it when a rule needs justifying or a case is not covered.

## Ground it in the subject

If the brief does not pin down the product, its learner, and the page's single job, pin them yourself and state your choice. Build with the brief's real content. Subject flavour goes into structure and wording; imagery, illustration, or motifs that do not carry information stay out (decorative "seductive details" lower recall and transfer, g≈−0.16).

## Principles

**The first screen is the task.** Open with the single next action and the one or two numbers the learner needs to decide whether to start. Layout is prototypical for its genre: appeal forms in 50 ms and is driven by low visual complexity and familiarity, so structural novelty reads as lower quality on first sight.

**Legibility over personality.** One type family (a second only for a real utility role such as code). Body ≥16px, ≥18px on reading views; measure 55-75 characters per line; line-height ≈1.5; contrast ≥4.5:1 for body and 3:1 for large text. Positive polarity (dark text on light) is the default; a dark scheme is an equal-quality option, chosen by the learner. Serif vs sans is a brand choice, not a legibility lever.

**Structure is information.** Numbering, eyebrows, dividers, and labels encode something true about the content: number a real sequence, divide a real change of kind. Test each device before keeping it.

**Earn every house default.** With no direction the model falls back on the same few styles: a cream or off-white page, italic accent words in headings, "01 / 02 / 03" section labels, monospace labels, pill-shaped buttons. Use one only when the plan gives it a reason. When a build swaps in a new default instead, add it to this list.

**Signal sparingly.** One primary action per view. Weight and colour are reserved for it and for the few cues a novice needs; everything else sits at body weight in ink or muted ink. Every status colour carries a second cue (label, icon, or position); ~8% of men have colour-vision deficiency. Neutral tones for wrong answers; a red-dominated verdict surface costs something and buys nothing.

**Adjacent, not elsewhere.** Explanations, hints, and verdicts sit next to the thing they describe (spatial contiguity, d≈0.72). Long material is segmented into learner-controlled chunks; depth is disclosed on request rather than shown to everyone.

**Feedback is elaborated, immediate, and about the task.** A wrong answer shows the correct answer and why (elaborated feedback d≈0.49; right/wrong alone d≈0.05). Feedback names the task and the process; praise, cheerleading, and comments on the person are absent. Errors state what happened and how to fix it.

**Autonomy-supportive.** Choices with reasons, "you can" phrasing, opt-out as easy as opt-in, quiet defaults for reminders and notifications, undo where possible. Urgency, scarcity, streak pressure, and nagging have no place; the learner is not being sold anything.

**Motion shows change.** A transition marks a state change (a card resolving to its verdict, a list settling) and lasts under 300 ms; nothing animates on load or on scroll. `prefers-reduced-motion` disables it. Celebration effects are unproven for learning; if the brief demands one, it is skippable.

**Moderate density.** Enough on screen to work without scrolling for the core task, enough space that nothing crowds. Primary controls are large (≥44px hit area) and near where the hand already is.

## Process

Two passes.

1. **Plan** a compact token system: palette as 4-6 named hex values with a light and dark set; one type family with a scale; a layout described in one sentence plus an ASCII wireframe per view; a signature that is a content structure (a week row, a two-column verdict, a numbered lesson path), never an ornament. Review the plan with two questions: *does any part add complexity a learner does not need?* and *does any part read as selling?* Revise, say what changed.
2. **Build** from the plan exactly, deriving every colour and type decision from the tokens. Keep CSS specificity flat so section spacing composes. Take screenshots at desktop and mobile widths, light and dark; critique against the principles; fix; note what you tried.

Quality floor, unannounced: responsive to 360px, visible keyboard focus, keyboard-only completion of the core flow, reduced motion respected, contrast met, colour never the sole carrier of meaning.

Aesthetics inflate perceived usability. Judge the build by whether the core task is quicker and clearer, not by whether it looks finished.

## Writing

Words are there to make the screen easier to understand. Name things by what the learner controls and recognizes. Active voice; a control says what happens ("Save changes"); an action keeps its name through the flow. Sentence case, plain verbs, no filler. Empty and error states give direction: what to do next, what went wrong and how to fix it, in the interface's own voice, without apology and without vagueness. Each element does one job.
