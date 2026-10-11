# AgentDoG-Qwen3-4B analysis (test split, unified protocol)

ROC-AUC 0.393, PR-AUC 0.116 (n=269, 40 abnormal, first-answer logprob scoring).

Verdict-level confusion (official binary prompt, greedy decode):
- normal  (label 0): 123 unsafe / 102 safe / 4 'not safe'  -> FPR 53.7%
- abnormal(label 1):  18 unsafe / 22 safe                   -> TPR 45.0%

Score-level: normal median p_unsafe ~ 0.5 (borderline-to-confident unsafe),
abnormal median ~ 0.004 (confident safe). The ranking is inverted: the
ATBench-trained trajectory guard flags benign ToolTask runs (failed searches,
retries, task-shaped side effects) as unsafe while missing quiet compromise
driven by poisoned tool outputs.

Interpretation (paper): chat-moderation guards (Qwen3Guard, LlamaGuard-3)
are blind to agentic injection (0 Unsafe verdicts in 269 cases); the
trajectory-aware guard transfers neither. Both failure modes are zero-shot
transfers without domain adaptation.
