#!/usr/bin/env python3
"""Build serialized, leakage-masked ToolTask cases for guard-model baselines.

Reads the split manifest produced by train_sbert_rgcn_graph_classifier.py
(identical split logic: split-seed 2026, 7:1.5:1.5, 15% abnormal per split),
maps each split graph to its recorded trajectory, serializes the run, applies
the same LEAKAGE_WORD_RE masking used in detector training, and emits JSONL.

Leakage masking must match training exactly:
  (?i)\b(?:attack|attacked|malicious|unsafe|harmful|injection|benign|normal|abnormal)\b -> ""
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

LEAKAGE_WORD_RE = re.compile(
    r"(?i)\b(?:attack|attacked|malicious|unsafe|harmful|injection|benign|normal|abnormal)\b"
)


def mask_text(text: str) -> str:
    return LEAKAGE_WORD_RE.sub("", text)


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_trajectories(bundle_root: Path) -> dict[str, dict]:
    path = bundle_root / "ToolTask-Benchmark" / "data" / "trajectories" / "trajectories.jsonl"
    index: dict[str, dict] = {}
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            record = json.loads(line)
            index[record["sample_id"]] = record
    return index


def serialize_case(task: str, steps: list[dict]) -> str:
    lines = [f"Task: {task}"]
    for step in steps:
        role = str(step.get("role", "")).lower()
        content = str(step.get("content", "") or "")
        thought = str(step.get("thought", "") or "")
        action = str(step.get("action", "") or "")
        if role == "user":
            lines.append(f"[USER] {content}")
        elif role == "agent":
            piece = "[AGENT]"
            if thought:
                piece += f" thought: {thought}"
            if action:
                piece += f" action: {action}"
            if content:
                piece += f" content: {content}"
            lines.append(piece)
        else:
            lines.append(f"[TOOL] {content}")
    return "\n".join(lines)


def truncate_head_tail(text: str, keep_head: int, keep_tail: int) -> tuple[str, bool]:
    if len(text) <= keep_head + keep_tail:
        return text, False
    head = text[:keep_head]
    tail = text[-keep_tail:]
    marker = "\n[...TRUNCATED...]\n"
    return head + marker + tail, True


def build_split_cases(split_entries: list[dict], trajectories: dict[str, dict], keep_head: int, keep_tail: int) -> list[dict]:
    cases = []
    missing = 0
    for entry in split_entries:
        graph = read_json(Path(entry["path"]))
        graph_id = graph["graph_id"]
        source = graph.get("source_trajectory") or graph_id
        trajectory = trajectories.get(source) or trajectories.get(graph_id)
        if trajectory is None:
            missing += 1
            continue
        text = serialize_case(str(trajectory.get("task", graph.get("task", ""))), trajectory.get("steps", []))
        text = mask_text(text)
        text, truncated = truncate_head_tail(text, keep_head, keep_tail)
        cases.append({
            "case_id": graph_id,
            "label": int(entry["label"]),
            "task_index": entry.get("task_index"),
            "chars": len(text),
            "truncated": truncated,
            "text": text,
        })
    if missing:
        print(f"WARNING: {missing} split graphs had no matching trajectory")
    return cases


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--splits", type=Path, required=True)
    parser.add_argument("--bundle-root", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--keep-head", type=int, default=8000)
    parser.add_argument("--keep-tail", type=int, default=16000)
    args = parser.parse_args()

    split_manifest = read_json(args.splits)
    trajectories = load_trajectories(args.bundle_root)
    args.out_dir.mkdir(parents=True, exist_ok=True)

    for split_name in ("test", "validation"):
        cases = build_split_cases(split_manifest[split_name], trajectories, args.keep_head, args.keep_tail)
        out_path = args.out_dir / f"{split_name}_cases.jsonl"
        with out_path.open("w", encoding="utf-8") as handle:
            for case in cases:
                handle.write(json.dumps(case, ensure_ascii=False) + "\n")
        labels = [case["label"] for case in cases]
        truncated = sum(case["truncated"] for case in cases)
        print(f"{split_name}: n={len(cases)} abnormal={sum(labels)} truncated={truncated} -> {out_path}")


if __name__ == "__main__":
    main()
