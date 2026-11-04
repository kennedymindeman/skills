#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["minatar==1.0.15", "numpy"]
# ///
"""Hand-written (no training) policy network for MinAtar Breakout.

Input: flattened 10x10x4 bool state, index = y*40 + x*4 + c
       channels: 0 paddle, 1 ball, 2 trail, 3 brick.
Net:   h = relu(W1 @ s + b1); logits = W2 @ h + b2; action = argmax.
Actions (full MinAtar indices): no-op=0, left=1, right=3.
"""
import sys

import numpy as np
from minatar import Environment

ACTIONS = [0, 1, 3]  # n, l, r


def idx(y, x, c):
    return y * 40 + x * 4 + c


def weights_v1():
    # T = predicted next ball column = 2*ball_x - trail_x ; P = paddle column.
    # hidden 0 = relu(T - P), hidden 1 = relu(P - T)
    W1 = np.zeros((2, 400))
    for y in range(10):
        for x in range(10):
            W1[0, idx(y, x, 1)] = 2 * x
            W1[0, idx(y, x, 2)] = -x
            W1[0, idx(y, x, 0)] = -x
    W1[1] = -W1[0]
    # logits: no-op = 0.5, left = h1, right = h0
    W2 = np.array([[0, 0], [0, 1], [1, 0]], dtype=float)
    return [(W1, np.zeros(2)), (W2, np.array([0.5, 0, 0]))]


def landing(y, x, vy, vx):
    """Follow the game's movement rules, ignoring bricks, until the ball
    reaches the paddle row. Return the midpoint of the two catch columns."""
    for _ in range(40):
        ny, nx = y + vy, x + vx
        if nx < 0 or nx > 9:
            nx = min(max(nx, 0), 9)
            vx = -vx
        if ny < 0:
            ny, vy = 0, -vy
        elif ny == 9:
            return (x + nx) / 2  # paddle under old or new column catches
        y, x = ny, nx
    raise RuntimeError("no landing")


def weights_v2():
    # Layer 1: one AND-unit per (ball cell, trail offset) + one paddle unit.
    rows, L = [], []
    for y in range(9):
        for x in range(10):
            for ty in (y - 1, y, y + 1):
                for tx in (x - 1, x, x + 1):
                    if not (0 <= ty < 10 and 0 <= tx < 10):
                        continue
                    dy, dx = y - ty, x - tx
                    # dx == 0: clipped against a side wall this step, so it now heads inward
                    vx = dx if dx else (1 if x == 0 else -1 if x == 9 else 0)
                    # dy == 0: vertical bounce this step (ceiling, paddle, brick, or reset)
                    vy = dy if dy else (-1 if y == 8 else 1)
                    if vx == 0:
                        continue  # mid-field dx == 0 never happens
                    w = np.zeros(400)
                    w[idx(y, x, 1)] = 1
                    w[idx(ty, tx, 2)] = 1
                    rows.append((w, -1.0))  # relu(ball + trail - 1): 1 iff both on
                    L.append(landing(y, x, vy, vx))
    wp = np.zeros(400)
    for x in range(10):
        wp[idx(9, x, 0)] = x
    rows.append((wp, 0.0))  # paddle column P
    W1 = np.array([r[0] for r in rows])
    b1 = np.array([r[1] for r in rows])
    # Layer 2: relu(T - P), relu(P - T), with T = sum_k L_k * h_k
    t = np.array(L + [0.0])
    p = np.zeros(len(rows))
    p[-1] = 1
    W2 = np.stack([t - p, p - t])
    # Output: no-op = 0.6 (stay within half a column), left = h1, right = h0
    W3 = np.array([[0, 0], [0, 1], [1, 0]], dtype=float)
    return [(W1, b1), (W2, np.zeros(2)), (W3, np.array([0.6, 0, 0]))]


def simulate(y, x, vy, vx, brick=None):
    """Follow the game's rules (wall clip, ceiling, one optional brick bounce).
    Return (landing midpoint, brick-row cells visited before landing)."""
    cells = []
    for _ in range(60):
        ny, nx = y + vy, x + vx
        if nx < 0 or nx > 9:
            nx = min(max(nx, 0), 9)
            vx = -vx
        if ny < 0:
            ny, vy = 0, -vy
        elif (ny, nx) == brick:
            ny, vy, brick = y, -vy, None
        elif ny == 9:
            return (x + nx) / 2, cells
        elif 1 <= ny <= 3 and (ny, nx) not in cells:
            cells.append((ny, nx))
        y, x = ny, nx
    raise RuntimeError("no landing")


def unit(on, off):
    """ReLU unit that outputs 1 iff every input in `on` is 1 and every input in `off` is 0."""
    w = np.zeros(400)
    for i in on:
        w[i] += 1
    for i in off:
        w[i] -= 1
    return w, -(len(on) - 1.0)


def weights_v3():
    rows, L = [], []
    for y in range(9):
        for x in range(10):
            for ty in (y - 1, y, y + 1):
                for tx in (x - 1, x, x + 1):
                    if not (0 <= ty < 10 and 0 <= tx < 10):
                        continue
                    dy, dx = y - ty, x - tx
                    vx = dx if dx else (1 if x == 0 else -1 if x == 9 else 0)
                    if vx == 0:
                        continue
                    base = [idx(y, x, 1), idx(ty, tx, 2)]
                    if y == 8 and dy == 0 and dx:
                        # paddle bounce: under old column = centre hit keeps vx,
                        # under new column = corner hit reverses vx
                        cases = [([idx(9, tx, 0)], vx, -1), ([idx(9, x, 0)], -vx, -1)]
                    else:
                        cases = [([], vx, dy if dy else (-1 if y == 8 else 1))]
                    for extra, cvx, cvy in cases:
                        on = base + extra
                        _, path = simulate(y, x, cvy, cvx)
                        bricks = [idx(by, bx, 3) for by, bx in path]
                        for k, cell in enumerate(path):  # first brick hit is path[k]
                            rows.append(unit(on + [bricks[k]], bricks[:k]))
                            L.append(simulate(y, x, cvy, cvx, brick=cell)[0])
                        rows.append(unit(on, bricks))  # clear path
                        L.append(simulate(y, x, cvy, cvx)[0])
    wp = np.zeros(400)
    for x in range(10):
        wp[idx(9, x, 0)] = x
    rows.append((wp, 0.0))
    W1 = np.array([r[0] for r in rows])
    b1 = np.array([r[1] for r in rows])
    t = np.array(L + [0.0])
    p = np.zeros(len(rows))
    p[-1] = 1
    W2 = np.stack([t - p, p - t])
    W3 = np.array([[0, 0], [0, 1], [1, 0]], dtype=float)
    return [(W1, b1), (W2, np.zeros(2)), (W3, np.array([0.6, 0, 0]))]


def policy(net, s):
    h = s.reshape(-1).astype(float)
    for i, (W, b) in enumerate(net):
        h = W @ h + b
        if i < len(net) - 1:
            h = np.maximum(0, h)
    return ACTIONS[int(np.argmax(h))]


def evaluate(net, episodes, cap, seed, random_policy=False):
    rng = np.random.default_rng(seed)
    scores, capped = [], 0
    for ep in range(episodes):
        env = Environment("breakout", sticky_action_prob=0.1)
        env.seed(seed + ep)
        env.reset()
        total, steps, done = 0.0, 0, False
        while not done and steps < cap:
            a = rng.choice(ACTIONS) if random_policy else policy(net, env.state())
            r, done = env.act(a)
            total += r
            steps += 1
        capped += not done
        scores.append(total)
    return np.array(scores), capped


if __name__ == "__main__":
    episodes = int(sys.argv[1]) if len(sys.argv) > 1 else 200
    cap = int(sys.argv[2]) if len(sys.argv) > 2 else 10_000
    for name, net, rand in [("random", None, True), ("v1 chase", weights_v1(), False),
                            ("v2 landing", weights_v2(), False),
                            ("v3 bricks", weights_v3(), False)]:
        if net:
            print(f"{name}: layer shapes {[W.shape for W, _ in net]}, "
                  f"params {sum(W.size + b.size for W, b in net)}")
        s, c = evaluate(net, episodes, cap, seed=0, random_policy=rand)
        print(f"{name:17s} mean={s.mean():8.1f} std={s.std():7.1f} "
              f"min={s.min():6.0f} max={s.max():6.0f} hit_cap={c}/{episodes}")
