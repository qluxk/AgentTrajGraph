#!/usr/bin/env python3
"""ROC/PR curves for the 5-seed ToolTask detector (test split)."""
import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import roc_curve, precision_recall_curve, auc

BASE = Path("/data/lab/atglad/GAD-Method-Portable/training")
OUT = Path("/data/lab/atglad/GAD-Method-Portable/figures")
OUT.mkdir(exist_ok=True)
OKABE = ["#0072B2", "#D55E00", "#009E73", "#CC79A7", "#56B4E9"]

fig, axes = plt.subplots(1, 2, figsize=(9.5, 4.0))
aucs_roc, aucs_pr = [], []
for i, seed in enumerate(range(42, 47)):
    preds = json.load(open(BASE / f"tooltask_edge_gat_15pct_seed{seed}" / "predictions.json"))["test"]
    y = np.array([r["label"] for r in preds], dtype=int)
    p = np.array([r["abnormal_probability"] for r in preds], dtype=float)
    fpr, tpr, _ = roc_curve(y, p)
    roc_auc = auc(fpr, tpr)
    prec, rec, _ = precision_recall_curve(y, p)
    pr_auc = auc(rec, prec[::-1]) if False else auc(rec, prec)
    aucs_roc.append(roc_auc); aucs_pr.append(pr_auc)
    axes[0].plot(fpr, tpr, color=OKABE[i], lw=1.4, label=f"seed {seed} (AUC {roc_auc:.3f})")
    axes[1].plot(rec, prec, color=OKABE[i], lw=1.4, label=f"seed {seed} (AUC {pr_auc:.3f})")
base_rate = None
preds0 = json.load(open(BASE / "tooltask_edge_gat_15pct_seed42" / "predictions.json"))["test"]
base_rate = np.mean([r["label"] for r in preds0])
axes[0].plot([0, 1], [0, 1], ls=":", color="grey", lw=1)
axes[1].axhline(base_rate, ls=":", color="grey", lw=1)
axes[0].set_xlabel("False positive rate"); axes[0].set_ylabel("True positive rate")
axes[1].set_xlabel("Recall"); axes[1].set_ylabel("Precision")
axes[0].set_title(f"ROC, test split (mean AUC {np.mean(aucs_roc):.3f})", fontsize=10)
axes[1].set_title(f"PR, test split (mean AUC {np.mean(aucs_pr):.3f})", fontsize=10)
for ax in axes:
    ax.legend(fontsize=7, loc="lower right"); ax.grid(alpha=0.25)
fig.tight_layout()
fig.savefig(OUT / "detection_curves.pdf", bbox_inches="tight")
fig.savefig(OUT / "detection_curves.png", dpi=200, bbox_inches="tight")
print("saved", OUT / "detection_curves.pdf", "mean ROC", np.mean(aucs_roc), "mean PR", np.mean(aucs_pr))
