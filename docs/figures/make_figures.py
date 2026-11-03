#!/usr/bin/env python
"""Draw the figures of docs/round-01-report.md. Needs matplotlib and numpy.

    python docs/figures/make_figures.py

Reads only published files; writes PNGs next to this script.
"""
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

HERE = os.path.dirname(os.path.abspath(__file__))
STREAMS = os.path.join(HERE, "..", "..", "trials", "01-lepton-negative-control", "streams.json")

OPH = "#1f4e79"
FORM = "#2e7d5b"
MORPH = "#c05a1e"
GREY = "#555555"
LIGHT = "#f4f4f4"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11})


def box(ax, x, y, w, h, title, lines, color, title_size=14, text_size=9.5):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.04",
                                linewidth=2, edgecolor=color, facecolor="white"))
    ax.text(x + w / 2, y + h - 0.09, title, ha="center", va="top", fontsize=title_size,
            fontweight="bold", color=color)
    ax.text(x + w / 2, y + h - 0.42, "\n".join(lines), ha="center", va="top", fontsize=text_size,
            color=GREY, linespacing=1.45)


def arrow(ax, a, b, text, color=GREY, rad=0.0, text_offset=(0, 0)):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="<->", mutation_scale=16, linewidth=1.6,
                                 color=color, connectionstyle="arc3,rad=%s" % rad))
    mid = ((a[0] + b[0]) / 2 + text_offset[0], (a[1] + b[1]) / 2 + text_offset[1])
    ax.text(mid[0], mid[1], text, ha="center", va="center", fontsize=9.5, color=color,
            bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="none"))


def fig_triad():
    fig, ax = plt.subplots(figsize=(9, 6.6))
    ax.set_xlim(0, 10); ax.set_ylim(0, 7); ax.axis("off")
    box(ax, 3.0, 5.1, 4.0, 1.7, "OPH",
        ["the instrument and its records:", "one repair law, an executable model,", "decoders that read records only"], OPH)
    box(ax, 0.1, 0.4, 4.0, 1.7, "F O R M",
        ["the standing of a reading:", "where each component entered", "the record, and what it earned"], FORM)
    box(ax, 5.9, 0.4, 4.0, 1.7, "MORPH",
        ["the transformation:", "M → ⊙ → R → PH → M₁,", "and the correction stays as a scar"], MORPH)
    ax.add_patch(plt.Circle((5, 3.4), 0.78, facecolor=LIGHT, edgecolor=GREY, linewidth=1.5))
    ax.text(5, 3.52, "the trial", ha="center", va="center", fontsize=12, fontweight="bold", color=GREY)
    ax.text(5, 3.18, "sealed key", ha="center", va="center", fontsize=9.5, color=GREY)
    arrow(ax, (3.1, 5.05), (2.1, 2.2), "records with a sealed origin,\nlabels on every inference", text_offset=(-1.2, 0.1))
    arrow(ax, (6.9, 5.05), (7.9, 2.2), "Patch Healing is named\nafter OPH's patch repair", text_offset=(1.25, 0.1))
    arrow(ax, (4.2, 1.25), (5.8, 1.25), "a disposition for\nevery transition", text_offset=(0, -0.6))
    fig.savefig(os.path.join(HERE, "triad.png"), dpi=200, bbox_inches="tight")
    plt.close(fig)


def fig_steps():
    fig, ax = plt.subplots(figsize=(13, 3.6))
    ax.set_xlim(0, 13.2); ax.set_ylim(0, 3.4); ax.axis("off")
    steps = [
        ("1  M", ["publish the records", "and the one-page card,", "commit the key by hash"], OPH),
        ("2  ⊙", ["readers work from the", "records and the card and", "state what they did"], MORPH),
        ("3  R", ["each reader writes down", "what the records license;", "withholding is an entry"], FORM),
        ("4  control", ["OPH's own decoder runs", "on the same records;", "its output is sealed too"], OPH),
        ("5  PH → M₁", ["open the key, score", "every reading, keep", "all of them"], MORPH),
    ]
    for i, (title, lines, color) in enumerate(steps):
        x = 0.2 + i * 2.6
        box(ax, x, 1.3, 2.4, 1.75, title, lines, color, title_size=13, text_size=9.5)
        if i < 4:
            ax.add_patch(FancyArrowPatch((x + 2.44, 2.15), (x + 2.58, 2.15), arrowstyle="-|>",
                                         mutation_scale=18, linewidth=1.5, color=GREY))
    ax.add_patch(FancyBboxPatch((0.2, 0.3), 10.2, 0.65, boxstyle="round,pad=0.02,rounding_size=0.03",
                                linewidth=1.2, edgecolor=GREY, facecolor=LIGHT, hatch="///", alpha=0.9))
    ax.text(5.3, 0.625, "key sealed: SHA-256 in the repository, OpenTimestamps proof", ha="center",
            va="center", fontsize=10.5, color=GREY,
            bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="none"))
    ax.add_patch(FancyBboxPatch((10.6, 0.3), 2.4, 0.65, boxstyle="round,pad=0.02,rounding_size=0.03",
                                linewidth=1.2, edgecolor=MORPH, facecolor="white"))
    ax.text(11.8, 0.625, "key opened", ha="center", va="center", fontsize=10.5, color=MORPH)
    fig.savefig(os.path.join(HERE, "steps.png"), dpi=200, bbox_inches="tight")
    plt.close(fig)


def fig_ladder():
    fig, ax = plt.subplots(figsize=(9, 5.2))
    ax.set_xlim(0, 10); ax.set_ylim(0, 5.4); ax.axis("off")
    rungs = [
        ("Consequence", "1 : 1.1903 : 1.4982 follows from the declared law\nby exact algebra", True),
        ("Incarnation", "the law runs in a clocked history; the observer\nends with one of 64 six-bit records", True),
        ("Recovery", "a decoder that sees the records and the clock\ncalibration reads the three gaps back", True),
        ("Validation", "measured charged leptons: 1 : 206.8 : 3477", False),
    ]
    for i, (name, text, ok) in enumerate(rungs):
        y = 0.5 + i * 1.2
        color = FORM if ok else "#b23a2a"
        ax.add_patch(FancyBboxPatch((1.2, y), 2.3, 0.85, boxstyle="round,pad=0.02,rounding_size=0.04",
                                    linewidth=2, edgecolor=color, facecolor="white"))
        ax.text(2.35, y + 0.425, name, ha="center", va="center", fontsize=13, fontweight="bold", color=color)
        ax.text(3.8, y + 0.425, text, ha="left", va="center", fontsize=10.5, color=GREY, linespacing=1.4)
        ax.text(0.5, y + 0.425, "✓" if ok else "✗", ha="center", va="center", fontsize=26, color=color,
                fontweight="bold")
        if i < 3:
            ax.add_patch(FancyArrowPatch((2.35, y + 0.88), (2.35, y + 1.17), arrowstyle="-|>",
                                         mutation_scale=16, linewidth=1.5, color=GREY))
    ax.text(5.0, 5.2, "The published lepton law of OPH r2060, step by step", ha="center", va="center",
            fontsize=12.5, fontweight="bold", color=GREY)
    fig.savefig(os.path.join(HERE, "ladder.png"), dpi=200, bbox_inches="tight")
    plt.close(fig)


def fig_record():
    fig, ax = plt.subplots(figsize=(12, 3.6))
    ax.set_xlim(0, 12.4); ax.set_ylim(0, 3.6); ax.axis("off")
    stages = [
        ("interval 1", "three pairs evolve\nunder their couplings", OPH, 1.9),
        ("read", "pair 0, pair 1, pair 2\n(0 empty, 1 occupied)", FORM, 1.9),
        ("phase", "on pair 1,\nif pair 0 read 1", GREY, 1.5),
        ("interval 2", "pairs and clock\nadvance again", OPH, 1.7),
        ("re-read", "pair 1", FORM, 1.3),
        ("clock", "X quadrature,\nthen Y (0 plus, 1 minus)", MORPH, 2.1),
    ]
    x = 0.2
    for name, text, color, w in stages:
        ax.add_patch(FancyBboxPatch((x, 1.5), w, 1.7, boxstyle="round,pad=0.02,rounding_size=0.04",
                                    linewidth=1.8, edgecolor=color, facecolor="white"))
        ax.text(x + w / 2, 3.0, name, ha="center", va="center", fontsize=12, fontweight="bold", color=color)
        ax.text(x + w / 2, 2.2, text, ha="center", va="center", fontsize=9.5, color=GREY, linespacing=1.4)
        x += w + 0.15
    bits = [("pair 0", FORM), ("pair 1", FORM), ("pair 2", FORM), ("pair 1\nagain", FORM), ("clock X", MORPH), ("clock Y", MORPH)]
    ax.text(0.2, 0.85, "the record:", ha="left", va="center", fontsize=11, color=GREY)
    for i, (label, color) in enumerate(bits):
        bx = 1.8 + i * 1.05
        ax.add_patch(FancyBboxPatch((bx, 0.45), 0.8, 0.8, boxstyle="square,pad=0.0", linewidth=1.6,
                                    edgecolor=color, facecolor=LIGHT))
        ax.text(bx + 0.4, 0.85, "bit %d" % i, ha="center", va="center", fontsize=10, color=color, fontweight="bold")
        ax.text(bx + 0.4, 0.2, label, ha="center", va="center", fontsize=8.5, color=GREY)
    ax.text(8.4, 0.85, "64 possible records; the table gives\nthe exact probability of each", ha="left",
            va="center", fontsize=10, color=GREY)
    fig.savefig(os.path.join(HERE, "record.png"), dpi=200, bbox_inches="tight")
    plt.close(fig)


def fig_streams():
    with open(STREAMS) as handle:
        data = json.load(handle)
    ids = sorted(data["streams"], key=lambda s: int(s[1:]))
    records = sorted(data["streams"][ids[0]]["records"])
    grid = np.array([[data["streams"][sid]["records"][r] for r in records] for sid in ids])
    fig, ax = plt.subplots(figsize=(13, 3.4))
    image = ax.imshow(np.log10(np.clip(grid, 1e-8, 1)), aspect="auto", cmap="viridis", vmin=-6, vmax=0)
    ax.set_yticks(range(len(ids))); ax.set_yticklabels(ids)
    ax.set_xticks(range(0, 64, 4)); ax.set_xticklabels([records[i] for i in range(0, 64, 4)], rotation=90, fontsize=8)
    ax.set_xlabel("record (six bits)")
    ax.set_title("The six published streams: probability of each of the 64 records (log scale)", fontsize=12)
    bar = fig.colorbar(image, ax=ax, pad=0.01)
    bar.set_label("log10 probability")
    fig.savefig(os.path.join(HERE, "streams.png"), dpi=200, bbox_inches="tight")
    plt.close(fig)


def fig_gaps():
    fig, ax = plt.subplots(figsize=(8, 4.4))
    law = [1.0, 1.1903, 1.4982]
    measured = [1.0, 206.77, 3477.2]
    x = np.arange(3)
    ax.bar(x - 0.2, law, 0.38, color=OPH, label="OPH trial law at r2060")
    ax.bar(x + 0.2, measured, 0.38, color="#b23a2a", label="measured charged leptons")
    for i in range(3):
        ax.text(x[i] - 0.2, law[i] * 1.15, "%.4g" % law[i], ha="center", fontsize=10, color=OPH)
        ax.text(x[i] + 0.2, measured[i] * 1.15, "%.4g" % measured[i], ha="center", fontsize=10, color="#b23a2a")
    ax.set_yscale("log"); ax.set_ylim(0.5, 2e4)
    ax.set_xticks(x); ax.set_xticklabels(["smallest", "middle", "largest"])
    ax.set_ylabel("ratio to the smallest gap (log scale)")
    ax.set_title("Why the identification failed: the same three slots, two different hierarchies", fontsize=11.5)
    ax.legend(frameon=False)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    fig.savefig(os.path.join(HERE, "gaps.png"), dpi=200, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    fig_triad(); fig_steps(); fig_ladder(); fig_record(); fig_streams(); fig_gaps()
    print("figures written to", HERE)
