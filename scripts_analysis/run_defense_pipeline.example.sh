#!/bin/bash
# Defense pipeline: wait for seeds -> node risk predictions -> cases -> experiences -> replay runs
set -uo pipefail
cd /data/lab/atglad/GAD-Method-Portable/server_upload_sbert_rgcn
export HF_HOME=/data/lab/hf_cache TOKENIZERS_PARALLELISM=false CUBLAS_WORKSPACE_CONFIG=:4096:8
export OPENAI_API_KEY=${DEEPSEEK_API_KEY}
export OPENAI_BASE_URL=https://api.deepseek.com/v1
export MODEL_NAME=deepseek-flash
export JUDGE_API_KEY=${JUAIPROXY_API_KEY}
export JUDGE_BASE_URL=https://www.juapi.net/v1
export JUDGE_MODEL_NAME=gpt-5.5
LOGDIR=/data/lab/atglad/GAD-Method-Portable/logs
mkdir -p "$LOGDIR"
echo "[PIPELINE] start $(date)"

for s in 44 45 46; do
  until [ -f ../training/tooltask_edge_gat_15pct_seed$s/metrics.json ]; do
    sleep 60; echo "[WAIT] seed$s pending $(date)"
  done
done
echo "[PIPELINE] all detector seeds done $(date)"

echo "[PIPELINE] stage1 node-risk predictions $(date)"
python3 scripts/predict_node_risk.py \
  --scorer-checkpoint ../training/tooltask_node_risk_seed42/best_node_risk_scorer.pt \
  --detector-checkpoint ../training/tooltask_edge_gat_15pct_seed42/best_model.pt \
  --detector-model-type edge_gat \
  --splits-file ../training/tooltask_edge_gat_15pct_seed42/splits.json \
  --sbert-cache ../training/tooltask_edge_gat_15pct_seed42/sbert_embeddings.pt \
  --edge-sbert-cache ../training/tooltask_edge_gat_15pct_seed42/edge_sbert_embeddings.pt \
  --normal-dir ../../ToolTask-Benchmark/data/graphs/normal \
  --abnormal-dir ../../ToolTask-Benchmark/data/graphs/abnormal \
  --split all --top-k 3 --device cuda \
  --output-dir ../training/tooltask_node_risk_seed42/inference_all \
  > "$LOGDIR/predict_all.log" 2>&1 || { echo "[PIPELINE] stage1 FAILED"; tail -30 "$LOGDIR/predict_all.log"; exit 1; }
echo "[PIPELINE] stage1 done $(date)"

echo "[PIPELINE] stage2 cases $(date)"
python3 experiments/unused_attack_mitigation/tooltask_cases.py \
  --bundle ../../ToolTask-Benchmark \
  --splits ../training/tooltask_edge_gat_15pct_seed42/splits.json \
  --output-dir experiments/unused_attack_mitigation/tooltask_cases \
  --sample-count 100 --sample-seed 20261006 \
  > "$LOGDIR/cases.log" 2>&1 || { echo "[PIPELINE] stage2 FAILED"; tail -30 "$LOGDIR/cases.log"; exit 1; }
echo "[PIPELINE] stage2 done $(date)"

CASES=experiments/unused_attack_mitigation/tooltask_cases/tooltask_cases_100.json
EXPDIR=experiments/unused_attack_mitigation/experiences

echo "[PIPELINE] stage3 experience synthesis dry-run $(date)"
python3 scripts/llm_judge_risk_experiences.py \
  --predictions ../training/tooltask_node_risk_seed42/inference_all/node_risk_predictions.json \
  --output-dir "$EXPDIR" \
  --base-url https://api.deepseek.com/v1 --model deepseek-v4-pro --api-key-env OPENAI_API_KEY \
  --max-tokens 8192 --workers 8 --dry-run \
  > "$LOGDIR/synth_dry.log" 2>&1 || { echo "[PIPELINE] stage3-dry FAILED"; tail -30 "$LOGDIR/synth_dry.log"; exit 1; }
echo "[PIPELINE] stage3 dry-run done $(date)"

echo "[PIPELINE] stage3 experience synthesis live $(date)"
python3 scripts/llm_judge_risk_experiences.py \
  --predictions ../training/tooltask_node_risk_seed42/inference_all/node_risk_predictions.json \
  --output-dir "$EXPDIR" \
  --base-url https://api.deepseek.com/v1 --model deepseek-v4-pro --api-key-env OPENAI_API_KEY \
  --max-tokens 8192 --workers 8 \
  > "$LOGDIR/synth_live.log" 2>&1 || { echo "[PIPELINE] stage3 FAILED"; tail -30 "$LOGDIR/synth_live.log"; exit 1; }
echo "[PIPELINE] stage3 done $(date)"

echo "[PIPELINE] stage4 mini validation $(date)"
python3 - "$CASES" <<'PY'
import json, sys, pathlib
rows=json.load(open(sys.argv[1]))
cases=rows['cases'] if isinstance(rows,dict) and 'cases' in rows else rows
out=pathlib.Path(sys.argv[1]).parent/'mini_cases.json'
json.dump(cases[:3], open(out,'w'), ensure_ascii=False, indent=1)
print('mini cases:', out, len(cases[:3]))
PY
python3 experiments/unused_attack_mitigation/run_replay_agent_experiment.py \
  --dataset tooltask --condition baseline --cases experiments/unused_attack_mitigation/tooltask_cases/mini_cases.json \
  --output-dir experiments/unused_attack_mitigation/runs_mini_baseline \
  > "$LOGDIR/mini_baseline.log" 2>&1 || { echo "[PIPELINE] stage4-baseline FAILED"; tail -30 "$LOGDIR/mini_baseline.log"; exit 1; }
python3 experiments/unused_attack_mitigation/run_replay_agent_experiment.py \
  --dataset tooltask --condition experience --cases experiments/unused_attack_mitigation/tooltask_cases/mini_cases.json \
  --experiences "$EXPDIR/llm_judgments.jsonl" \
  --output-dir experiments/unused_attack_mitigation/runs_mini_experience \
  > "$LOGDIR/mini_experience.log" 2>&1 || { echo "[PIPELINE] stage4-experience FAILED"; tail -30 "$LOGDIR/mini_experience.log"; exit 1; }
echo "[PIPELINE] stage4 done $(date)"

echo "[PIPELINE] stage5 full runs $(date)"
python3 experiments/unused_attack_mitigation/run_replay_agent_experiment.py \
  --dataset tooltask --condition baseline --cases "$CASES" \
  --output-dir experiments/unused_attack_mitigation/runs_baseline --workers 3 \
  > "$LOGDIR/full_baseline.log" 2>&1 || { echo "[PIPELINE] stage5-baseline FAILED"; tail -30 "$LOGDIR/full_baseline.log"; exit 1; }
echo "[PIPELINE] stage5 baseline done $(date)"
python3 experiments/unused_attack_mitigation/run_replay_agent_experiment.py \
  --dataset tooltask --condition experience --cases "$CASES" \
  --experiences "$EXPDIR/llm_judgments.jsonl" \
  --output-dir experiments/unused_attack_mitigation/runs_experience --workers 3 \
  > "$LOGDIR/full_experience.log" 2>&1 || { echo "[PIPELINE] stage5-experience FAILED"; tail -30 "$LOGDIR/full_experience.log"; exit 1; }
echo "[PIPELINE] stage5 experience done $(date)"
echo "[PIPELINE] ALL DONE $(date)"
