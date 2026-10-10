# TBD Evidence Checklist

Every `TBD-*` token that appears in the draft (`main.pdf`, 11 pages) maps to a slot that must be filled **only** with evidence from actual experiments or from the private/underlying corpora. This checklist is the complete inventory. The draft contains **no** fabricated numbers; each token below lists where it occurs and what evidence fills it.

## A. Abstract

| Token | Location | Evidence needed |
|---|---|---|
| `TBD-EVALUATION-SCOPE` | Abstract, sentence 4 (results clause) | One clause naming which corpora/benchmarks the reported numbers span (e.g., "across two public tool-agent benchmarks and one in-house paired corpus"). |
| `TBD-KEY-RESULTS` | Abstract, sentence 4 (results clause) | Headline detection metric (e.g., PR-AUC) and headline localization metric (e.g., Hit@1) from the final runs; plus defense ΔASR if desired. Must match Tables 3–5. |
| `TBD-PROTOCOL` | Abstract, sentence 4 (results clause) | One clause on the evaluation protocol (seeds/splits/statistical tests) consistent with §6.1. |

## B. Data and Graph Construction (§4, Table 1)

| Token | Location | Evidence needed |
|---|---|---|
| `TBD-DATASET-NAME-A` | §4.1, §6.5 (RQ5) | Public identity of tool-integrated injection corpus A (e.g., AgentDojo / InjecAgent-style source actually used). |
| `TBD-DATASET-NAME-B` | §4.1, §6.5 (RQ5) | Public identity of web-agent corpus B (e.g., WebArena-derived runs actually used). |
| `TBD-PRIVATE-DATASET-NAME` | §4.1, §6.5 (RQ5) | Internal name/description of the paired normal/anomalous corpus. |
| `TBD-DATASET-STATISTICS` | §4.1, §4.5, §8 (Threats to external validity), Table 1 | Full Table 1 row values: source, task counts, label source, #runs, anomaly rate per corpus; agent/model configurations represented. |
| `TBD-ANOMALY-RATIO` | §4.1 | Per-corpus normal:anomalous ratios. |
| `TBD-DATA-PROVENANCE` | §3.1 (Problem), §4.1, §8 (Reproducibility) | Data collection provenance statement; licensing/redistribution constraints; release governance for the private corpus. |
| `TBD-LABELING-PROTOCOL` | §3.1, §4.2 | Who labeled, against what ground truth (tool traces? benchmark verdicts?), adjudication process. |
| `TBD-DATA-QUALITY-CONTROL` | §3.1, §4.2 | Inter-annotator agreement, audit sampling, label-error handling. |
| `TBD-SPLIT-PROTOCOL` | §3.1 (implied), §6.1 | Exact train/val/test splits, task/site/payload-family grouping, per-corpus sizes. |
| `TBD-DATA-LEAKAGE-CONTROL` | §4.1, §6.1, §8 (Threats to internal validity) | Audit results proving no task/site/payload overlap across splits and label-blind construction. |
| `TBD-RANDOM-SEEDS` | §4.1, §6.1 | Number of seeds and their values. |
| `TBD-CODE-AND-ARTIFACTS` | §8 (Reproducibility) | Repository URL / anonymized artifact link and contents list. |

## C. Method Configuration (§5.2, §6.1)

| Token | Location | Evidence needed |
|---|---|---|
| `TBD-ENCODER-CONFIGURATION` | §5.2 | Sentence-encoder identity/version, chunk length, overlap, embedding dims, risk-gate MLP dims. |
| `TBD-GRAPH-ENCODER-CONFIGURATION` | §6.1 | Depth, heads, hidden dim, dropout, training config of the shared Edge-GAT. |

## D. Main Detection Results (§6, Table 3)

| Token | Location | Evidence needed |
|---|---|---|
| `TBD-MAIN-DETECTION-TABLE` | Table 3 | All cells: ROC-AUC, PR-AUC, F1(anom), FPR, Bal-Acc for every baseline group and the full model, per corpus (or the chosen headline corpus with others in appendix). |
| `TBD-BASELINE-LIST` | §6.2 | Final roster: exact method names/versions per family (guard models used as text-screening baselines, which GAD scorers, which judge model). |
| `TBD-BASELINE-CONFIGURATIONS` | §6.2 | Prompts, temperatures, token budgets for LLM baselines; hyperparameters for GNN/GAD baselines. |
| `TBD-FAIR-COMPARISON-PROTOCOL` | §6.2 | The written fairness protocol: same split, same normal-class treatment, compute-matched judge budgets. |
| `TBD-GLOBAL-LOCAL-ABLATION` | §5.3 (Method II pointer), §6.3 (RQ1) | Numbers for full-graph-only vs. Action-subgraph-only vs. full model. |
| `TBD-DETECTION-SIGNIFICANCE` | §6.3 (RQ1) | Statistical test results for the RQ1 comparison (e.g., paired bootstrap/t-test over seeds, exact p-values). |
| `TBD-THRESHOLD-ANALYSIS` | §6.1, §6.3, §8 | Sensitivity of F1/FPR/precision to the operating threshold; chosen operating point rationale. |

## E. Localization Results (§6.4–6.5, Table 4)

| Token | Location | Evidence needed |
|---|---|---|
| `TBD-LOCALIZATION-TABLE` | Table 4 | Hit@1, Hit@K, node/edge IoU, candidate size for fixed-hop vs. unit-wise candidates. |
| `TBD-LOCALIZATION-RESULTS` | §6.4 (RQ2) | Full localization results across corpora, including Top-K auxiliary evidence behavior. |
| `TBD-CANDIDATE-COVERAGE` | §4.5 (audit), §6.4 (RQ2) | Fraction of true loci present in the candidate set at all (upper bound on recall), plus candidate size distribution. |
| `TBD-FIXED-HOP-VS-ACTION-UNIT` | §5.4 (Method I pointer), §6.5 (RQ3) | The controlled representation comparison with everything else held fixed. |

## F. Ablations (§6.6, Table 5)

| Token | Location | Evidence needed |
|---|---|---|
| `TBD-ABLATION-TABLE` | Table 5 | All ablation rows × (ROC-AUC, PR-AUC, Hit@1). |
| `TBD-REPRESENTATION-ABLATIONS` | §6.6 (RQ4) | Numbers for: −justification text, −relation type, −directionality, chunk-mean/truncation pooling, fixed vs. learned α/β, −shared LayerNorm. |
| `TBD-OBJECTIVE-ABLATIONS` | §5.3 (Method II pointer), §6.6 (RQ4), §8 | Numbers for: −paired pseudo-labels, bounded uncertainty weighting vs. fixed weights. |

## G. Defense (§7, Table 6)

| Token | Location | Evidence needed |
|---|---|---|
| `TBD-DEFENSE-TABLE` | Table 6 | ASR, task SR, false-trigger rate, cost, ΔASR for all six conditions; plus the cross-configuration transfer column. |
| `TBD-DEFENSE-SIGNIFICANCE` | §7.1 | Statistical comparisons between paired conditions (McNemar or paired bootstrap over task instances), exact p-values. |
| `TBD-QUALITATIVE-CASES` | §5.4 (Method II pointer), §6.4 (RQ2), §7.3 | Curated case studies: generated experiences verbatim, induced policy changes, failure cases. |

## H. Retired tokens (section deleted at author request)

| Token | Status | Note |
|---|---|---|
| `TBD-THREATS-TO-VALIDITY` | **Retired** | The standalone Analysis and Limitations section was removed from the paper; a one-clause limitation statement (graph-construction coverage, paired-supervision faithfulness) remains in the Conclusion. Do not re-add without re-opening the section. |
| `TBD-CODE-AND-ARTIFACTS` | **Retired** | Was anchored in the deleted Reproducibility paragraph. If an artifact release is added back, reintroduce the token there. |

The section reference for `TBD-OBSERVED-LIMITATIONS` is now **§4.4 only** (Structural Audit); it remains active.

## Rules for filling

1. Fill each token **only** from completed experiments or corpus documentation; if an experiment is not run, keep the token or delete the claim — never invent numbers or narrative results.
2. The draft must never contain superiority/significance claims until `TBD-DETECTION-SIGNIFICANCE` / `TBD-DEFENSE-SIGNIFICANCE` exist; after filling, wording must stay within what the test supports.
3. `TBD-CANDIDATE-COVERAGE` is reported **separately** from final localization accuracy and must never be substituted for it (§6.4 rule).
4. After filling, delete the token (the `\tbd{}` wrapper renders red — remove the wrapper too) and re-run `latexmk`.
