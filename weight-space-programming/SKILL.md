---
name: weight-space-programming
description: Writes or edits neural network weights directly from known rules, with no gradient training. Use when a task needs a small network or policy whose rules you can read (a game, a controller, a classifier with a spec), when a trained model needs a surgical behaviour fix, or when the user mentions weight-space programming.
---

# Weight-space programming

Weight-space programming means reasoning out a network's weights the way you would write code, then checking the result by running it. The MIT CSAIL report (Takehi, Teoh, Zhang, Khattab, Nov 2026) used it to write MinAtar game policies from scratch and to edit Qwen3.5-0.8B's math reasoning. Frontier models from late 2026 onward (GPT-6 Astra, Opus 5.5) can do it; earlier ones scored near zero.

## Fit

Reach for it when the deliverable must be a network: it ships into a runtime that only executes weights, it must match an existing architecture, or a trained model needs a targeted fix without retraining. When plain code would do the same job, write the code; a hand-written network is a program compiled into weights, and the code is easier to read and change.

The method is strongest when the rules are small and readable (the environment source, a spec). For an edit to a large trained model, the rules are unknown, so expect many rounds of probe and measure.

## Steps

1. Read the rules at the source: the environment code, the spec, or the model's activations. Note every case the observation leaves ambiguous; each one needs an extra input condition. Done when you can state the exact update rule and every case the input cannot distinguish.
2. Write a generator script that builds the weights, never a training loop. Build ReLU units as exact logic: `relu(sum(on) - sum(off) - (len(on) - 1))` is 1 only when every `on` input is 1 and every `off` input is 0. A layer of these units is a lookup table, and the next layer reads the looked-up values as a weighted sum. Compute each unit's output weight from the rules (simulate the game forward, for example).
3. Evaluate against random play and against a baseline, with seeded episodes. Report the episode or step cap, and how many runs hit it.
4. When a score falls short, log the state at each failure and group the failures before changing any weights. Change the weights to fix the largest group, then re-run step 3. Done when the failure log has no large group you can explain from the rules.
5. Report the score next to the baseline's source (trained here, or quoted from a paper), the cap, and the network's size. A ratio against a weak baseline or a capped episode can grow or shrink several times over, so give both raw numbers.

## Worked example

`breakout_example.py` in this folder holds three hand-written MinAtar Breakout policies from 2026-11-02, run with `uv run --script breakout_example.py 50 10000`. Each fix came from a failure log (step 4):

- v1, 2 units chasing the ball's next column, scored 11.7: the paddle could never catch a ball moving away at the same speed.
- v2 aimed at the landing column on an empty field and scored 7.3: every miss followed a brick bounce that came too late to reach.
- v3, 1,799 lookup units that condition on the first brick in the ball's path and on the paddle position for corner hits, scored 235.9 with 44 of 50 episodes at the 10,000-step cap. The paper's PPO baseline scored 25.3.
