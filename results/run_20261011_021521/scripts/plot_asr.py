#!/usr/bin/env python3
"""Paired ASR comparison figure from the new analysis schema."""
import json, math
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

BASE = Path("/data/lab/atglad/GAD-Method-Portable")
A = json.load(open(BASE / "analysis/paired_asr_analysis.json"))
ABL = json.load(open(BASE / "analysis/ablation_asr_analysis.json"))
OUT = BASE / "figures"
OUT.mkdir(exist_ok=True)

C = A["conditions"]
BASE_C, EXP_C, REC_C = C["baseline"], C["experience"], C["experience_recall"]

fig, axes = plt.subplots(1, 2, figsize=(10.0, 4.0))

ax = axes[0]
bars = [
    ("Baseline", 100 * BASE_C["asr"], BASE_C["ci95"], "#0072B2"),
    ("Experience\n(strict gate)", 100 * EXP_C["asr"], EXP_C["ci95"], "#D55E00"),
    ("Experience\n(recall gate)", 100 * REC_C["asr"], REC_C["ci95"], "#009E73"),
]
for x, (name, v, ci, c) in enumerate(bars):
    lo, hi = ci
    ax.bar(x, v, width=0.6, color=c, alpha=0.88)
    ax.errorbar(x, v, yerr=[[v - 100 * lo], [100 * hi - v]], color="k", capsize=4, lw=1)
    ax.text(x, v + 2.2, f"{v:.1f}%", ha="center", fontsize=9)
ax.set_xticks(range(3)); ax.set_xticklabels([b[0] for b in bars], fontsize=9)
ax.set_ylabel("Attack success rate (%)")
ax.set_title("(a) Panel-level ASR, n=100 paired cases", fontsize=10)
ax.grid(axis="y", alpha=0.25); ax.set_ylim(0, 60)
ax.text(0.02, 0.95, "recall gate vs baseline: exact McNemar p=0.031",
        transform=ax.transAxes, fontsize=8, va="top", color="#333333")

ax = axes[1]
arms = [
    ("Baseline", 6, 13, "#0072B2", ""),
    ("Generic", 4, 13, "#999999", ""),
    ("Raw traj.", 3, 13, "#CC79A7", ""),
    ("Full graph", 2, 13, "#56B4E9", ""),
    ("Shuffled", 2, 13, "#E69F00", ""),
    ("Ours", 0, 13, "#D55E00", "p=0.031"),
]
xs = np.arange(len(arms))
vals = [100 * k / n for _, k, n, _, _ in arms]
colors = [a[3] for a in arms]
ax.bar(xs, vals, width=0.62, color=colors, alpha=0.9)
for x, (name, k, n, _, note) in zip(xs, arms):
    ax.text(x, 100 * k / n + 1.5, f"{k}/{n}", ha="center", fontsize=9)
    if note:
        ax.text(x, 100 * k / n + 6.5, note, ha="center", fontsize=8, color="#8B0000")
ax.set_xticks(xs); ax.set_xticklabels([a[0] for a in arms], fontsize=8.5, rotation=20)
ax.set_ylabel("Attack success rate (%)")
ax.set_title("(b) Treated cases (n=13): experience-content ablation", fontsize=10)
ax.grid(axis="y", alpha=0.25); ax.set_ylim(0, 60)

fig.tight_layout()
fig.savefig(OUT / "asr_comparison.pdf", bbox_inches="tight")
fig.savefig(OUT / "asr_comparison.png", dpi=160, bbox_inches="tight")
print("saved", OUT / "asr_comparison.pdf")
