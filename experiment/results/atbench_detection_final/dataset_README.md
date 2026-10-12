# ATBench DeepSeek Full

This package contains the final ATBench trajectories and strict semantic DAGs.

- `trajectories/trajectories_1000.jsonl`: all 1,000 final trajectories.
- `trajectories/summary.json`: outcome and eligibility counts.
- `graphs/normal/`: 608 strict normal graphs (`clean` or `defended`, task-valid).
- `graphs/abnormal/`: 196 abnormal graphs (`compromised`).
- `graphs/manifest.json`: graph construction metadata.

The strict graph set excludes 190 clean-but-incomplete trajectories and 6 unresolved
trajectories. Graph edge generation was label-blind and used `deepseek-flash` with
thinking disabled. No real external tools were executed. API credentials, private
attack audits, checkpoints, and internal prompt files are not included.
