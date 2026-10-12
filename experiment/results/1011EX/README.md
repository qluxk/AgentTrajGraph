# 1011EX — consolidated experiment results (2026-10-11)

Unified-protocol test split (n=269, 40 abnormal; train/val/test = 70/15/15,
all-splits abnormal fraction 0.15, split-seed 2026). Leakage-masked
trajectory text; guard instruction templates kept verbatim; 8192-token
input cap; RTX 4090, single deterministic run per guard.

| guard | ROC-AUC | PR-AUC |
| --- | --- | --- |
| agentdog_qwen3_4b_test | 0.393 | 0.116 |
| agentdog_qwen3_4b_test_v3 | 0.408 | 0.120 |
| alignmentcheck_llama31_8b_test | 0.585 | 0.204 |
| llamaguard3_8b_test | 0.378 | 0.127 |
| qwen3guard_gen8b_test | 0.641 | 0.231 |

Files: raw JSONL scores + summaries + case builders/runners + per-run logs (logs/).
Provenance: per-experiment directories pushed by labrun.sh; see ANALYSIS.md files there.
