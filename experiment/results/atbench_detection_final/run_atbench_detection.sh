#!/bin/bash
# ATBench-DeepSeek-Full detection experiments (final package: 804 strict graphs)
# Unified paper protocol: 7:1.5:1.5 split, 15% abnormal per split, split-seed 2026, seeds 42-46.
set -uo pipefail
ROOT=/data/lab/GAD-Method-Portable/server_upload_sbert_rgcn
cd "$ROOT"
export TOKENIZERS_PARALLELISM=false CUBLAS_WORKSPACE_CONFIG=:4096:8
export HF_HOME="$ROOT/.cache/huggingface"
DATA=/data/lab/ATBench-DeepSeek-Full/graphs
NORMAL=$DATA/normal
ABNORMAL=$DATA/abnormal
SPLIT="--all-splits-abnormal-fraction 0.15 --train-fraction 0.70 --validation-fraction 0.15 --split-seed 2026"
OUT=training/atbench_final
LOG=$OUT/logs
mkdir -p "$LOG"
echo "[atbench-final] start $(date)" >> "$LOG/pipeline.log"

run_one () {
  local out=$1; local log=$2; shift 2
  if [ -f "$out/metrics.json" ]; then echo "skip $(basename "$out") (metrics exists)" >> "$LOG/pipeline.log"; return 0; fi
  mkdir -p "$out"
  local cache=$OUT/edge_rgcn_seed42
  if [ "$out" != "$cache" ] && [ -f "$cache/sbert_embeddings.pt" ]; then
    ln -sf "$cache/sbert_embeddings.pt" "$out/sbert_embeddings.pt"
    [ -f "$cache/edge_sbert_embeddings.pt" ] && ln -sf "$cache/edge_sbert_embeddings.pt" "$out/edge_sbert_embeddings.pt"
  fi
  python3 "$@" >> "$log" 2>&1
  local rc=$?
  echo "$(basename "$out") rc=$rc $(date)" >> "$LOG/pipeline.log"
  return $rc
}

for seed in 42 43 44 45 46; do
  run_one "$OUT/edge_rgcn_seed$seed" "$LOG/edge_rgcn_seed$seed.log" \
    scripts/train_sbert_rgcn_graph_classifier.py \
    --normal-dir "$NORMAL" --abnormal-dir "$ABNORMAL" --output-dir "$OUT/edge_rgcn_seed$seed" \
    --sbert-model sentence-transformers/all-MiniLM-L6-v2 \
    --model-type edge_rgcn --pool mean_max --classification-loss cross_entropy \
    --normal-compactness-weight 0 --normal-abnormal-separation-weight 0 \
    --device cuda --epochs 120 --patience 35 --batch-size 8 \
    --hidden-dim 64 --type-embedding-dim 16 --rgcn-layers 2 --relation-rank 16 \
    --relation-embedding-dim 16 --direction-embedding-dim 8 --gat-heads 4 \
    --dropout 0.02 --learning-rate 0.0007 --weight-decay 0.0001 \
    $SPLIT --seed $seed

  run_one "$OUT/gcn_seed$seed" "$LOG/gcn_seed$seed.log" \
    scripts/train_sbert_rgcn_graph_classifier.py \
    --normal-dir "$NORMAL" --abnormal-dir "$ABNORMAL" --output-dir "$OUT/gcn_seed$seed" \
    --sbert-model sentence-transformers/all-MiniLM-L6-v2 \
    --model-type gcn \
    --normal-compactness-weight 0.01 --normal-abnormal-separation-weight 0.01 --normal-abnormal-margin 1.0 \
    --device cuda --epochs 100 --patience 30 --early-stop-metric loss \
    --batch-size 16 --sbert-batch-size 64 \
    --hidden-dim 64 --type-embedding-dim 16 --rgcn-layers 2 \
    --dropout 0.2 --learning-rate 0.001 --weight-decay 0.0005 \
    $SPLIT --seed $seed

  run_one "$OUT/sbert_mlp_seed$seed" "$LOG/sbert_mlp_seed$seed.log" \
    scripts/train_sbert_rgcn_graph_classifier.py \
    --normal-dir "$NORMAL" --abnormal-dir "$ABNORMAL" --output-dir "$OUT/sbert_mlp_seed$seed" \
    --sbert-model sentence-transformers/all-MiniLM-L6-v2 \
    --model-type sbert_mlp \
    --normal-compactness-weight 0.01 --normal-abnormal-separation-weight 0.01 --normal-abnormal-margin 1.0 \
    --device cuda --epochs 100 --patience 30 --early-stop-metric loss \
    --batch-size 16 --sbert-batch-size 64 \
    --hidden-dim 64 \
    --dropout 0.2 --learning-rate 0.001 --weight-decay 0.0005 \
    $SPLIT --seed $seed

  run_one "$OUT/rgcn_meanmax_seed$seed" "$LOG/rgcn_meanmax_seed$seed.log" \
    scripts/train_sbert_rgcn_graph_classifier.py \
    --normal-dir "$NORMAL" --abnormal-dir "$ABNORMAL" --output-dir "$OUT/rgcn_meanmax_seed$seed" \
    --sbert-model sentence-transformers/all-MiniLM-L6-v2 \
    --model-type rgcn --pool mean_max --classification-loss igad_pmi \
    --normal-compactness-weight 0.01 --normal-abnormal-separation-weight 0.01 \
    --normal-abnormal-margin 1.0 --device cuda --epochs 100 --patience 30 \
    --batch-size 16 --hidden-dim 64 --type-embedding-dim 16 --rgcn-layers 2 \
    --relation-rank 16 --dropout 0.2 --learning-rate 0.001 --weight-decay 0.0005 \
    $SPLIT --seed $seed
done

for seed in 42 43 44 45 46; do
  run_one "$OUT/igad_seed$seed" "$LOG/igad_seed$seed.log" \
    scripts/train_sbert_igad_atbench.py \
    --data-dir "$DATA" --output-dir "$OUT/igad_seed$seed" \
    --sbert-cache "$OUT/igad_sbert_cache.pt" \
    --sbert-model sentence-transformers/all-MiniLM-L6-v2 \
    --device cuda --epochs 100 --patience 30 --batch-size 16 \
    --normal-abnormal-ratio 9 \
    --all-splits-abnormal-fraction 0.15 --train-fraction 0.70 --validation-fraction 0.15 \
    --split-seed 2026 --seed $seed
done

python3 scripts/summarize_five_runs.py --glob "$OUT/edge_rgcn_seed*/metrics.json" --output "$OUT/edge_rgcn_summary.json" --model edge_rgcn_deployed --dataset atbench_final --abnormal-fraction 0.15 >> "$LOG/summary.log" 2>&1
python3 scripts/summarize_five_runs.py --glob "$OUT/gcn_seed*/metrics.json" --output "$OUT/gcn_summary.json" --model gcn --dataset atbench_final --abnormal-fraction 0.15 >> "$LOG/summary.log" 2>&1
python3 scripts/summarize_five_runs.py --glob "$OUT/sbert_mlp_seed*/metrics.json" --output "$OUT/sbert_mlp_summary.json" --model sbert_mlp --dataset atbench_final --abnormal-fraction 0.15 >> "$LOG/summary.log" 2>&1
python3 scripts/summarize_five_runs.py --glob "$OUT/rgcn_meanmax_seed*/metrics.json" --output "$OUT/rgcn_meanmax_summary.json" --model rgcn_meanmax --dataset atbench_final --abnormal-fraction 0.15 >> "$LOG/summary.log" 2>&1
python3 scripts/summarize_five_runs.py --glob "$OUT/igad_seed*/metrics.json" --output "$OUT/igad_summary.json" --model igad --dataset atbench_final --abnormal-fraction 0.15 >> "$LOG/summary.log" 2>&1

echo "[atbench-final] ALL DONE $(date)" >> "$LOG/pipeline.log"
