# 1011EX — consolidated experiment results (2026-10-11)

Unified-protocol test split (n=269, 40 abnormal; train/val/test = 70/15/15,
all-splits abnormal fraction 0.15, split-seed 2026). Leakage-masked
trajectory text; guard instruction templates kept verbatim; 8192-token
input cap; RTX 4090, single deterministic run per guard.

| guard | n | n_abnormal | ROC-AUC | PR-AUC |
| --- | --- | --- | --- | --- |
| agentdog_qwen3_4b_test_v3 | 269 | 40 | 0.408 | 0.120 |
| alignmentcheck_llama31_8b_test | 269 | 40 | 0.585 | 0.204 |
| llamaguard3_8b_test | 269 | 40 | 0.378 | 0.127 |
| qwen3guard_gen8b_test | 269 | 40 | 0.641 | 0.231 |

Files: raw JSONL scores + summaries + case builders/runners + per-run logs (logs/).
Provenance: per-experiment directories pushed by labrun.sh; see ANALYSIS.md files there.
Note: the invalid AgentDoG masked-template run and the 3072-cap run were removed;
the canonical AgentDoG entry is agentdog_qwen3_4b_test_v3 (renamed agentdog_qwen3_4b_test).
