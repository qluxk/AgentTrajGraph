# AgentDoG-Qwen3-4B analysis (test split, unified protocol, 8192-token cap)

ROC-AUC 0.408, PR-AUC 0.120 (n=269, 40 abnormal, first-answer logprob scoring).
Official binary prompt with INTACT template (an earlier attempt accidentally
applied the leakage mask to the template itself, corrupting the task
definition; that run was discarded. A second attempt used a 3072-token cap
inconsistent with the other guards; also discarded. This is the canonical run).

Verdict-level confusion (greedy decode, official format):
- normal  (label 0): 128 unsafe / 101 safe  -> FPR 55.9%
- abnormal(label 1):  21 unsafe /  19 safe  -> TPR 52.5%

Score-level: normal median p_unsafe ~ 0.5, abnormal median ~ 0.29. The ranking
is inverted: the ATBench-trained trajectory guard flags benign ToolTask runs
as unsafe (over half of them) while missing roughly half of the real attacks.

Interpretation (paper): chat-moderation guards (Qwen3Guard-Gen-8B, LlamaGuard-3-8B)
are blind to agentic injection (0 Unsafe verdicts in 269 cases, LlamaGuard-3's
weak residual signal tracks PII density, r = 0.39); the trajectory-aware guard
(AgentDoG) transfers neither precision nor ranking. Both failure modes are
zero-shot transfers without domain adaptation.
