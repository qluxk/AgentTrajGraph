# Guard-model detection baselines (ToolTask, unified protocol)

Test split reproduced from the released ToolTask-Bundle with the exact
launcher protocol: --all-splits-abnormal-fraction 0.15 --train-fraction 0.70
--validation-fraction 0.15 --split-seed 2026 --seed 42.
Test: n=269, abnormal=40 (14.9%). Leakage masking identical to training.
Serialization: Task + [USER]/[AGENT]/[TOOL] steps, head+tail truncation
(8000+16000 chars), 8192-token input cap. Scoring: constrained first-answer
logprob softmax over the guard's candidate labels.

- qwen3guard_gen8b_test: Qwen/Qwen3Guard-Gen-8B, ROC-AUC 0.641, PR-AUC 0.231, 0/269 Unsafe verdicts
- llamaguard3_8b_test: meta-llama/Llama-Guard-3-8B (via ModelScope mirror), ROC-AUC 0.378, PR-AUC 0.127, all 'safe'
- agentdog_qwen3_4b_test: AI45Research/AgentDoG-Qwen3-4B (ModelScope), ROC-AUC 0.393, PR-AUC 0.116, FPR 53.7% / TPR 45% (see guard_agentdog_qwen3_4b_test/ANALYSIS.md)
