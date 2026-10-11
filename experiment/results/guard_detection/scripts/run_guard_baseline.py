#!/usr/bin/env python3
"""Run an open-weight safety guard model as a zero-shot detection baseline.

Scores each serialized trajectory with p(unsafe) computed from the guard's
first-answer-token logprobs (constrained candidate set), then reports
ROC-AUC and PR-AUC on the given split. Deterministic (greedy scoring).
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import torch
from sklearn.metrics import average_precision_score, roc_auc_score
from transformers import AutoModelForCausalLM, AutoTokenizer

QWEN_CANDIDATES = ["Safety: Safe", "Safety: Unsafe", "Safety: Controversial"]
QWEN_UNSAFE_IDX = 1
LLAMA_CANDIDATES = ["safe", "unsafe"]
LLAMA_UNSAFE_IDX = 1


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def candidate_logprobs(scores, tokenizer, candidates: list[str]) -> list[float]:
    total_logprob = torch.zeros(len(candidates), dtype=torch.float64)
    for candidate_index, candidate in enumerate(candidates):
        token_ids = tokenizer(candidate, add_special_tokens=False).input_ids
        accumulated = 0.0
        for step, token_id in enumerate(token_ids):
            if step >= len(scores):
                accumulated = -1e9
                break
            log_probs = torch.log_softmax(scores[step][0].float(), dim=-1)
            accumulated += float(log_probs[token_id].item())
        total_logprob[candidate_index] = accumulated
    log_normalizer = torch.logsumexp(total_logprob, dim=0)
    return (total_logprob - log_normalizer).tolist()


def greedy_verdict(model_inputs, model, tokenizer, max_new_tokens: int) -> str:
    generated = model.generate(
        **model_inputs,
        max_new_tokens=max_new_tokens,
        do_sample=False,
        output_scores=True,
        return_dict_in_generate=True,
        pad_token_id=tokenizer.eos_token_id,
    )
    new_tokens = generated.sequences[0][model_inputs["input_ids"].shape[1]:]
    verdict = tokenizer.decode(new_tokens, skip_special_tokens=True)
    return generated.scores, verdict.strip()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", choices=("qwen", "llama"), required=True)
    parser.add_argument("--model-path", type=str, required=True)
    parser.add_argument("--cases", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--max-input-tokens", type=int, default=3072)
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--device", type=str, default="cuda")
    args = parser.parse_args()

    cases = read_jsonl(args.cases)
    if args.limit:
        cases = cases[: args.limit]

    tokenizer = AutoTokenizer.from_pretrained(args.model_path)
    model = AutoModelForCausalLM.from_pretrained(
        args.model_path, torch_dtype=torch.bfloat16, device_map=args.device
    )
    model.eval()

    if args.model == "qwen":
        candidates, unsafe_idx = QWEN_CANDIDATES, QWEN_UNSAFE_IDX
    else:
        candidates, unsafe_idx = LLAMA_CANDIDATES, LLAMA_UNSAFE_IDX

    rows = []
    for case in cases:
        if args.model == "qwen":
            messages = [{"role": "user", "content": case["text"]}]
            prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        else:
            messages = [{"role": "user", "content": case["text"]}]
            prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        model_inputs = tokenizer(
            prompt, return_tensors="pt", truncation=True, max_length=args.max_input_tokens
        ).to(model.device)
        with torch.inference_mode():
            scores, verdict = greedy_verdict(model_inputs, model, tokenizer, max_new_tokens=24)
            probs = candidate_logprobs(scores, tokenizer, candidates)
        p_unsafe = probs[unsafe_idx]
        rows.append({
            "case_id": case["case_id"],
            "label": case["label"],
            "p_unsafe": p_unsafe,
            "probs": probs,
            "verdict": verdict,
            "truncated": case["truncated"],
        })
        print(f"{case['case_id']} label={case['label']} p_unsafe={p_unsafe:.4f} verdict={verdict[:40]!r}")

    labels = [row["label"] for row in rows]
    scores_out = [row["p_unsafe"] for row in rows]
    summary = {
        "model_path": args.model_path,
        "model_variant": args.model,
        "n": len(rows),
        "n_abnormal": sum(labels),
        "roc_auc": roc_auc_score(labels, scores_out),
        "pr_auc": average_precision_score(labels, scores_out),
        "candidates": candidates,
        "scoring": "first-answer-token constrained logprob softmax",
        "max_input_tokens": args.max_input_tokens,
        "n_truncated": sum(row["truncated"] for row in rows),
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    summary_path = args.out.with_suffix(".summary.json")
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
