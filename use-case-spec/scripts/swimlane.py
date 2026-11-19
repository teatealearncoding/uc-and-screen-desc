#!/usr/bin/env python3
"""Render a swimlane activity diagram (PNG) from a small JSON spec.

Usage:  python swimlane.py spec.json out.png

Spec:
{
  "lanes": ["User", "System"],                  # left-to-right order
  "nodes": [
    {"id": "s",  "type": "start", "lane": "User"},
    {"id": "n1", "type": "step",  "lane": "User",   "no": "1",   "text": "Select to create new Case"},
    {"id": "d1", "type": "decision", "lane": "User"},
    {"id": "e",  "type": "end",   "lane": "System"}
  ],
  "edges": [["s","n1"], ["d1","n2","No"], ["d1","n3","Yes"]]   # optional 3rd item = edge label
}
Node types: start, step, decision, end. A step may carry "no" (shown as "(no)") and "text".
Optional per-node "row" (int) forces the row. Loops back to an earlier node are detected
automatically and routed along the left side of the node.
"""
import json
import sys
import textwrap

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon, Circle, Rectangle

plt.rcParams["font.family"] = ["Liberation Sans", "DejaVu Sans"]

LANE_W, ROW_H, HEAD_H = 5.2, 1.5, 0.6
BOX_H, BOX_W_MAX, DIAM, CIRC = 0.85, 3.4, 0.38, 0.24


def load(path):
    with open(path, encoding="utf8") as f:
        spec = json.load(f)
    ids = {n["id"] for n in spec["nodes"]}
    for e in spec["edges"]:
        for x in e[:2]:
            if x not in ids:
                sys.exit(f"Edge references unknown node id: {x}")
    for n in spec["nodes"]:
        if n["lane"] not in spec["lanes"]:
            sys.exit(f"Node {n['id']} uses unknown lane: {n['lane']}")
    return spec


def find_back_edges(nodes, edges):
    adj = {n["id"]: [] for n in nodes}
    for i, e in enumerate(edges):
        adj[e[0]].append((e[1], i))
    state, back = {}, set()

    def dfs(u):
        state[u] = 1
        for v, i in adj[u]:
            if state.get(v) == 1:
                back.add(i)
            elif v not in state:
                dfs(v)
        state[u] = 2

    for n in nodes:  # declared order, so the first node is the root
        if n["id"] not in state:
            dfs(n["id"])
    return back


def assign_rows(nodes, edges, back):
    row = {n["id"]: 0 for n in nodes}
    for _ in range(len(nodes) + 1):  # longest-path layering
        changed = False
        for i, e in enumerate(edges):
            if i in back:
                continue
            if row[e[1]] < row[e[0]] + 1:
                row[e[1]] = row[e[0]] + 1
                changed = True
        if not changed:
            break
    for n in nodes:
        if "row" in n:
            row[n["id"]] = int(n["row"])
    return row


def render(spec, out):
    nodes, edges, lanes = spec["nodes"], spec["edges"], spec["lanes"]
    back = find_back_edges(nodes, edges)
    row = assign_rows(nodes, edges, back)
    nrows = max(row.values()) + 1
    W, H = LANE_W * len(lanes), HEAD_H + ROW_H * nrows

    # nodes sharing a (lane,row) cell are spread across the lane
    groups = {}
    for n in nodes:
        groups.setdefault((n["lane"], row[n["id"]]), []).append(n)
    pos = {}
    for (lane, r), grp in groups.items():
        k, li = len(grp), lanes.index(lane)
        for j, n in enumerate(grp):
            cx = li * LANE_W + LANE_W * (j + 0.5) / k
            cy = -(HEAD_H + ROW_H * (r + 0.5))
            w = min(BOX_W_MAX, LANE_W / k - 0.5)
            pos[n["id"]] = dict(n=n, x=cx, y=cy, w=w, r=r)

    fig, ax = plt.subplots(figsize=(W, H))
    ax.set_xlim(0, W)
    ax.set_ylim(-H, 0)
    ax.axis("off")
    ax.add_patch(Rectangle((0.02, -H + 0.02), W - 0.04, H - 0.04, fill=False, lw=1.2))
    for i, name in enumerate(lanes):
        ax.text(i * LANE_W + LANE_W / 2, -HEAD_H / 2, name, ha="center", va="center",
                fontsize=12, fontweight="bold")
        if i:
            ax.plot([i * LANE_W] * 2, [0, -H], color="black", lw=1)

    def half(p):  # half-width, half-height of a node
        t = p["n"]["type"]
        if t == "decision":
            return DIAM, DIAM
        if t in ("start", "end"):
            return CIRC, CIRC
        return p["w"] / 2, BOX_H / 2

    for p in pos.values():
        n, x, y = p["n"], p["x"], p["y"]
        t = n["type"]
        if t == "start":
            ax.add_patch(Circle((x, y), CIRC, color="black", zorder=3))
        elif t == "end":
            ax.add_patch(Circle((x, y), CIRC, fc="white", ec="black", lw=1.2, zorder=3))
            ax.add_patch(Circle((x, y), CIRC * 0.68, color="black", zorder=4))
        elif t == "decision":
            ax.add_patch(Polygon([(x, y + DIAM), (x + DIAM, y), (x, y - DIAM), (x - DIAM, y)],
                                 fc="white", ec="black", lw=1.1, zorder=3))
        else:
            ax.add_patch(FancyBboxPatch((x - p["w"] / 2, y - BOX_H / 2), p["w"], BOX_H,
                                        boxstyle="round,pad=0,rounding_size=0.28",
                                        fc="white", ec="black", lw=1.1, zorder=3))
            label = f"({n['no']})\n" if n.get("no") else ""
            label += "\n".join(textwrap.wrap(n.get("text", ""), max(14, int(p["w"] * 6.2))))
            ax.text(x, y, label, ha="center", va="center", fontsize=10.5, zorder=5,
                    linespacing=1.25)

    def draw(points, label=None):
        for a, b in zip(points[:-2], points[1:-1]):
            ax.plot([a[0], b[0]], [a[1], b[1]], color="black", lw=1, zorder=2,
                    solid_capstyle="butt")
        ax.annotate("", xy=points[-1], xytext=points[-2], zorder=2,
                    arrowprops=dict(arrowstyle="-|>", lw=1, color="black", shrinkA=0,
                                    shrinkB=0, mutation_scale=11))
        if label:
            (x0, y0), (x1, y1) = points[0], points[1]
            lx, ly = (x0 + x1) / 2, (y0 + y1) / 2
            if abs(x1 - x0) < 1e-6:
                lx += 0.22
                ly = y0 + (y1 - y0) * 0.3
            else:
                ly += 0.14
            ax.text(lx, ly, label, ha="center", va="center", fontsize=9, zorder=6,
                    bbox=dict(fc="white", ec="none", pad=0.8))

    used_side = {}
    for i, e in enumerate(edges):
        a, b, lab = e[0], e[1], (e[2] if len(e) > 2 else None)
        pa, pb = pos[a], pos[b]
        ha, hb = half(pa), half(pb)
        sx, sy, dx, dy = pa["x"], pa["y"], pb["x"], pb["y"]
        if i in back:  # loop back along the left side
            xc = max(0.12, min(sx - ha[0], dx - hb[0]) - 0.32)
            draw([(sx - ha[0], sy), (xc, sy), (xc, dy), (dx - hb[0], dy)], lab)
        elif pa["r"] == pb["r"] and abs(sx - dx) > 1e-6:  # same row, side to side
            s = 1 if dx > sx else -1
            draw([(sx + s * ha[0], sy), (dx - s * hb[0], dy)], lab)
        else:
            side = "bottom"
            if pa["n"]["type"] == "decision" and abs(dx - sx) > 1e-6:
                want = "right" if dx > sx else "left"
                if (a, want) not in used_side:
                    side = want
            used_side[(a, side)] = True
            top = (dx, dy + hb[1])
            if side == "bottom":
                start = (sx, sy - ha[1])
                if abs(sx - dx) < 1e-6:
                    draw([start, top], lab)
                else:
                    ym = sy - ROW_H * 0.5
                    draw([start, (sx, ym), (dx, ym), top], lab)
            else:
                s = 1 if side == "right" else -1
                draw([(sx + s * ha[0], sy), (dx, sy), top], lab)

    fig.savefig(out, dpi=150, bbox_inches="tight", pad_inches=0.05)
    plt.close(fig)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    render(load(sys.argv[1]), sys.argv[2])
    print("Saved", sys.argv[2])
