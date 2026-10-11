#!/usr/bin/env python3
"""Summarize 5-seed detector metrics and paired replay ASR analysis.

Handles the main baseline/experience pair (runs_full_v2), the recall-gate
condition (runs_full_recall) and the four ablation arms (runs_abl_*).
"""
from __future__ import annotations
import json, math
from pathlib import Path
from collections import Counter

BASE = Path("/data/lab/atglad/GAD-Method-Portable")
EXP = BASE / "server_upload_sbert_rgcn/experiments/unused_attack_mitigation"
OUT = BASE / "analysis"
OUT.mkdir(exist_ok=True)


def load_json(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def read_jsonl(p: Path):
    rows = {}
    if not p.is_file():
        return rows
    for line in p.read_text(encoding="utf-8").splitlines():
        if line.strip():
            row = json.loads(line)
            rows[str(row["case_id"])] = row
    return rows


def wilson(k: int, n: int, z: float = 1.96):
    if n == 0:
        return None, None
    p = k / n
    denom = 1 + z * z / n
    center = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return center - half, center + half


def mcnemar_exact(b: int, c: int):
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    p = sum(math.comb(n, i) for i in range(0, k + 1)) * (2 ** -n) * 2
    return min(1.0, p)


def seed_summary():
    rows = []
    for s in range(42, 47):
        d = BASE / "training" / f"tooltask_edge_gat_15pct_seed{s}"
        m = load_json(d / "metrics.json")
        test = m.get("test", m.get("final_test", {}))
        val = m.get("validation", m.get("best_validation", {}))
        rows.append({
            "seed": s,
            "test_roc_auc": test.get("roc_auc"),
            "test_pr_auc": test.get("pr_auc"),
            "test_accuracy": test.get("accuracy"),
            "test_recall": test.get("recall"),
            "test_abnormal_f1": test.get("abnormal_f1"),
            "threshold": (test.get("threshold") or val.get("threshold") or m.get("threshold")),
            "best_epoch": m.get("best_epoch") or m.get("history", {}).get("best_epoch"),
        })
    (OUT / "seed_summary.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")
    print(json.dumps(rows, indent=2))


def domains_map():
    traj_path = Path("/data/lab/atglad/ToolTask-Benchmark/data/trajectories/trajectories.jsonl")
    dom = {}
    if traj_path.is_file():
        for line in traj_path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                row = json.loads(line)
                dom[str(row.get("sample_id"))] = str(row.get("domain", "unknown"))
    cases_path = EXP / "tooltask_cases/tooltask_cases_100.json"
    if cases_path.is_file():
        cases = load_json(cases_path)
        cases = cases["cases"] if isinstance(cases, dict) and "cases" in cases else cases
        for c in cases:
            dom.setdefault(str(c["case_id"]), "unknown")
    return dom


def condition_asr(rows):
    ok = {c: r for c, r in rows.items() if not r.get("error")}
    succ = {c: int(bool(r.get("attack_success"))) for c, r in ok.items()}
    lo, hi = wilson(sum(succ.values()), len(succ)) if succ else (None, None)
    return {
        "completed": len(ok),
        "errors": len(rows) - len(ok),
        "attack_success_count": sum(succ.values()),
        "asr": (sum(succ.values()) / len(succ)) if succ else None,
        "ci95": [lo, hi],
        "succ": succ,
        "decisions": Counter(d.get("decision", "?") for r in ok.values() for d in r.get("decisions", [])),
        "terminations": Counter(r.get("termination", "?") for r in ok.values()),
    }


def pair_stats(a_rows, b_rows, label_a, label_b):
    shared = sorted(set(a_rows) & set(b_rows))
    both = [c for c in shared if not a_rows[c].get("error") and not b_rows[c].get("error")]
    a_succ = {c: int(bool(a_rows[c].get("attack_success"))) for c in both}
    b_succ = {c: int(bool(b_rows[c].get("attack_success"))) for c in both}
    n10 = sum(1 for c in both if a_succ[c] == 1 and b_succ[c] == 0)
    n01 = sum(1 for c in both if a_succ[c] == 0 and b_succ[c] == 1)
    return {
        "paired_cases": len(both),
        f"asr_{label_a}": (sum(a_succ.values()) / len(both)) if both else None,
        f"asr_{label_b}": (sum(b_succ.values()) / len(both)) if both else None,
        "delta": ((sum(a_succ.values()) - sum(b_succ.values())) / len(both)) if both else None,
        "discordant_a_only": n10, "discordant_b_only": n01,
        "mcnemar_exact_p": mcnemar_exact(n10, n01),
    }


def paired_analysis():
    rb = read_jsonl(EXP / "runs_full_v2/baseline_replay_runs.jsonl")
    re_ = read_jsonl(EXP / "runs_full_v2/experience_replay_runs.jsonl")
    rr = read_jsonl(EXP / "runs_full_recall/experience_replay_runs.jsonl")
    if not rb:
        print("no baseline rows yet")
        return
    dom = domains_map()
    admitted = set()
    jf = EXP / "experiences/llm_judgments.jsonl"
    if jf.is_file():
        for line in jf.read_text(encoding="utf-8").splitlines():
            if line.strip():
                r = json.loads(line)
                j = r.get("llm_judgment") or {}
                if not r.get("error") and j.get("is_reusable_experience") is True:
                    admitted.add(str(r["graph_id"]))
    out = {"treated_admitted_case_ids": sorted(admitted), "treated_count": len(admitted)}

    cond = {}
    for name, rows in (("baseline", rb), ("experience", re_), ("experience_recall", rr)):
        if rows:
            cond[name] = condition_asr(rows)
    out["conditions"] = {
        n: {k: v for k, v in c.items() if k not in ("succ",)} for n, c in cond.items()
    }
    for n, c in cond.items():
        agg = {}
        for cid, s in c["succ"].items():
            a = agg.setdefault(dom.get(cid, "unknown"), [0, 0])
            a[0] += s; a[1] += 1
        out["conditions"][n]["per_domain"] = {
            d: {"n": n2, "asr": s / n2} for d, (s, n2) in agg.items()
        }
    if "baseline" in cond and "experience" in cond:
        out["paired_baseline_vs_experience"] = {
            k: v for k, v in pair_stats(rb, re_, "baseline", "experience").items()
        }
        treated = cond["experience"]
        sub = {c: r for c, r in re_.items() if c in admitted and not r.get("error")}
        sub_b = {c: r for c, r in rb.items() if c in admitted and not r.get("error")}
        out["paired_treated_only"] = pair_stats(sub_b, sub, "baseline", "experience")
        lo, hi = wilson(sum(1 for c in sub if bool(sub[c].get("attack_success"))), len(sub))
        out["treated_asr_experience"] = {"n": len(sub), "asr": (
            sum(1 for c in sub if bool(sub[c].get("attack_success"))) / len(sub)) if sub else None,
            "ci95": [lo, hi]}
        out["treated_asr_baseline"] = {"n": len(sub_b), "asr": (
            sum(1 for c in sub_b if bool(sub_b[c].get("attack_success"))) / len(sub_b)) if sub_b else None}
    if "baseline" in cond and "experience_recall" in cond:
        out["paired_baseline_vs_recall"] = {
            k: v for k, v in pair_stats(rb, rr, "baseline", "experience_recall").items()
        }
    (OUT / "paired_asr_analysis.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))


def ablation_analysis():
    rb = read_jsonl(EXP / "runs_full_v2/baseline_replay_runs.jsonl")
    arms = {}
    for arm, path in (
        ("experience", EXP / "runs_full_v2/experience_replay_runs.jsonl"),
        ("generic", EXP / "runs_abl_generic/experience_replay_runs.jsonl"),
        ("raw", EXP / "runs_abl_raw/experience_replay_runs.jsonl"),
        ("full", EXP / "runs_abl_full/experience_replay_runs.jsonl"),
        ("shuffled", EXP / "runs_abl_shuffled/experience_replay_runs.jsonl"),
        ("experience_recall", EXP / "runs_full_recall/experience_replay_runs.jsonl"),
    ):
        rows = read_jsonl(path)
        if rows:
            arms[arm] = condition_asr(rows)
    if not arms:
        print("no ablation rows yet")
        return
    out = {}
    dom = domains_map()
    for arm, c in arms.items():
        sub = c["succ"]
        agg = {}
        for cid, s in sub.items():
            a = agg.setdefault(dom.get(cid, "unknown"), [0, 0])
            a[0] += s; a[1] += 1
        out[arm] = {
            "completed": c["completed"], "asr": c["asr"], "ci95": c["ci95"],
            "attack_success_count": c["attack_success_count"],
            "per_domain": {d: {"n": n, "asr": s / n} for d, (s, n) in agg.items()},
        }
    base = {c: r for c, r in rb.items() if not r.get("error")}
    base_succ = {c: int(bool(r.get("attack_success"))) for c, r in base.items()}
    for arm, c in arms.items():
        shared = sorted(set(c["succ"]) & set(base_succ))
        if not shared:
            continue
        a_s = {x: int(bool(c["succ"].get(x, 0))) for x in shared}
        b_s = {x: base_succ[x] for x in shared}
        n10 = sum(1 for x in shared if b_s[x] == 1 and a_s[x] == 0)
        n01 = sum(1 for x in shared if b_s[x] == 0 and a_s[x] == 1)
        out[arm]["vs_baseline"] = {
            "paired_cases": len(shared),
            "asr_baseline": sum(b_s.values()) / len(shared),
            "asr_arm": sum(a_s.values()) / len(shared),
            "discordant_baseline_only": n10, "discordant_arm_only": n01,
            "mcnemar_exact_p": mcnemar_exact(n10, n01),
        }
    (OUT / "ablation_asr_analysis.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    seed_summary()
    paired_analysis()
    ablation_analysis()
