# Citation Checklist

**Status: all 72 BibTeX entries in `refs.bib` originate from `paper_search` results obtained in this working session; none was typed from memory.** A clean `latexmk` build confirms every `\cite{}` key resolves (`0 undefined citations`, `0 undefined references`) and all 72 entries are cited at least once.

## 1. Provenance rule (brief requirement)

Every entry was copied from a search result's BibTeX block. After collection, 23 entries were **upgraded to their published versions** by cross-checking titles against the CrossRef API (`api.crossref.org/works?query.bibliographic=...`) during this session; corrected fields (venue, year, DOI, pages) were applied by a script from those authoritative responses.

## 2. DOI-verified entries (27) — published versions confirmed against CrossRef

| Key | Published venue |
|---|---|
| `greshake2023what` | AISec@CCS 2023 (10.1145/3605764.3623985) |
| `zhan2024injecagent` | Findings of ACL 2024 |
| `debenedetti2024agentdojo` | NeurIPS 37 |
| `wang2025webinject` | EMNLP 2025 |
| `zhan2025adaptive` | Findings of NAACL 2025 |
| `deng2023mindweb` | NeurIPS 36 |
| `chen2024secalign` | ACM CCS 2025 |
| `zhong2025attention` | NDSS 2026 (10.14722/ndss.2026.240394) |
| `yuan2024rjudge` | Findings of EMNLP 2024 |
| `zheng2023judging` | NeurIPS 36 |
| `wang2025probguard` | ASE 2026, pp. 1470–1482 |
| `schick2023toolformer` | NeurIPS 36 |
| `joshi2026deontic` | IEEE ICWS 2026 |
| `yao2023tree` | NeurIPS 36 |
| `besta2023graph` | AAAI 2024 |
| `schlichtkrull2017modeling` | ESWC 2018 (LNCS) |
| `hu2020heterogeneous` | WWW 2020 |
| `liu2021anomaly` | IEEE TNNLS |
| `roy2024gadnr` | WSDM 2024 |
| `duan2022arise` | IEEE TNNLS |
| `hu2025samcl` | IEEE TNNLS |
| `carbonneau2016multiple` | Springer, *Machine Learning* (DOI-verified) |
| `kendall2017multitask` | CVPR 2018 |
| `reimers2019sentencebert` | EMNLP-IJCNLP 2019 |
| `gao2021simcse` | EMNLP 2021 |
| `shinn2023reflexion` | NeurIPS 36 |
| `zhao2023expel` | AAAI 2024 |

Known annotation: the CrossRef record for NDSS 2026 (`zhong2025attention`) duplicates one author name; we kept the 6-author list that matches the arXiv record.

## 3. arXiv-only entries (45) — real papers, published version not yet located

All carry arXiv identifiers returned by `paper_search`. Recency-wise this is where the newest work lives (2025–2026 arXiv IDs), which the BNI/WWW recency requirement favors. They are kept because the alternative would be dropping the most recent literature, not because they are less real.

Attack side: `liu2023prompt`, `liu2024automatic`, `zhang2024agent`, `liao2024environmental`, `lee2026will`, `wang2026adaptools`, `syros2026muzzle`, `chiang2025agents`.
Benchmarks: `zhou2023webarena`, `gou2025mindweb`, `lu2024toolsandbox`, `liu2023agentbench`, `song2024beyond`, `zhang2024large`, `tur2025safearena`, `levy2024stwebagentbench`.
Defenses/guards/judges: `chen2024struq`, `zhu2025melon`, `debenedetti2025defeating`, `inan2023llama`, `liu2024calibration`, `zhuge2024agentasajudge`, `mohammadi2026trajectoryjudge`, `luo2025agrail`, `lin2026dreamguard`, `mou2026toolsafe`, `liu2026agentdog`, `zhou2026from`.
Tooling/protocols: `yao2022react`, `hou2025model`, `zhang2025security`, `errico2025securing`.
Vision/agentic-Web: `yang2025agentic`, `nie2026synergy`, `ng2026agent`, `zhou2026externalization`.
Reasoning graphs: `besta2023graph` is DOI-verified above; `deng2026defa` (closest work) is arXiv-only.
GNN/GAD/MIL: `velikovi2017graph`, `brody2021attentive`, `tang2022rethinking`, `sotiropoulos2023adamm`, `wang2026glass`, `ilse2018attentionbased`, `tu2019multiple`.

## 4. `ref_verify` behavior note (for the next person)

Final full-file `ref_verify` run: **8 DOI-bearing entries were resolved against CrossRef and corrected** (publisher/booktitle fields; author checks for `debenedetti2024agentdojo`, `deng2023mindweb`, `zhong2025attention`); **64 DOI-less entries were flagged UNVERIFIED**. Direct probing shows the tool's title matching fails even for canonical papers (e.g., "Graph Attention Networks", "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena" were reported NOT FOUND) — i.e., the flag is a **tool limitation for DOI-less records**, not evidence of fabrication. All 72 entries were nevertheless sourced from real `paper_search` results in this session.

Corrections were applied selectively after independent CrossRef API inspection (`api.crossref.org/works/<doi>`): the `deng2023mindweb` author field was aligned to CrossRef ("Sam Stevens"); the `zhong2025attention` "correction" was **rejected** because CrossRef's NDSS record duplicates Yanjiao Chen (7 author slots for a 6-author paper) — the 6-author list matching the arXiv record is kept.

**Before submission:** (a) re-run `paper_search` for each arXiv-only entry and upgrade to published versions where they now exist; (b) re-run `ref_verify` — entries with DOIs should verify.

## 5. Likely published-version upgrades (verify, do not trust from memory)

Well-known candidates: `yao2022react` → ICLR 2023; `velikovi2017graph` → ICLR 2018; `brody2021attentive` → ICLR 2022; `tang2022rethinking` → IEEE TKDE; `ilse2018attentionbased` → ICML 2018; `tu2019multiple` → CVPR 2019; `inan2023llama` → ACL/EMNLP-era guard paper. Confirm via CrossRef before editing the .bib — never hand-type metadata.

## 6. Where each cluster is cited

- **Intro P1** (agentic Web): `yao2022react`, `schick2023toolformer`, `hou2025model`, `zhang2025security`, `zhou2023webarena`, `deng2023mindweb`, `liu2023agentbench`, `lu2024toolsandbox`, `song2024beyond`, `gou2025mindweb`, `yang2025agentic`, `nie2026synergy`, `zhang2024large`.
- **Intro P2** (attack surface): `greshake2023what`, `liu2023prompt`, `liu2024automatic`, `zhan2024injecagent`, `debenedetti2024agentdojo`, `zhang2024agent`, `liao2024environmental`, `wang2025webinject`, `wang2026adaptools`, `syros2026muzzle`, `chiang2025agents`, `tur2025safearena`, `levy2024stwebagentbench`, `lee2026will`.
- **Intro P3** (defense gaps): `chen2024struq`, `chen2024secalign`, `zhong2025attention`, `inan2023llama`, `liu2024calibration`, `debenedetti2025defeating`, `zhu2025melon`, `yuan2024rjudge`, `zhuge2024agentasajudge`, `mohammadi2026trajectoryjudge`, `luo2025agrail`, `wang2025probguard`, `lin2026dreamguard`, `mou2026toolsafe`, `liu2026agentdog`, `zhou2026from`.
- **Intro P4** (root cause): `yao2023tree`, `besta2023graph`, `deng2026defa`.
- **§2 Related Work**: all of the above re-grouped thematically, plus `zheng2023judging`, `errico2025securing`, `ng2026agent`, `joshi2026deontic`, `zhou2026externalization`, `shinn2023reflexion`, `zhao2023expel`, `allard2026experiential`, GNN/GAD/MIL cluster (`velikovi2017graph`, `brody2021attentive`, `schlichtkrull2017modeling`, `hu2020heterogeneous`, `tang2022rethinking`, `liu2021anomaly`, `roy2024gadnr`, `duan2022arise`, `sotiropoulos2023adamm`, `wang2026glass`, `hu2025samcl`, `carbonneau2016multiple`, `ilse2018attentionbased`, `tu2019multiple`).
- **§5/§6 Method**: `reimers2019sentencebert`, `gao2021simcse` (§5.2), `schlichtkrull2017modeling`, `hu2020heterogeneous` (§6.1), `kendall2017multitask` (§6.3).
- **§6/§7 Evaluation**: `debenedetti2024agentdojo`, `zhan2024injecagent`, `tur2025safearena`, `levy2024stwebagentbench` (metrics), baseline families `inan2023llama`, `liu2024calibration`, `velikovi2017graph`, `schlichtkrull2017modeling`, `hu2020heterogeneous`, `brody2021attentive`, `tang2022rethinking`, `liu2021anomaly`, `wang2026glass`, `zheng2023judging`, `yuan2024rjudge`, `zhuge2024agentasajudge`.
- **§7/§8**: `zhan2025adaptive`, `syros2026muzzle` (adaptive adversaries), `lee2026will` (covert attacks), `mohammadi2026trajectoryjudge`, `deng2026defa` (§9 vision), `hou2025model`, `zhang2025security` (§9 standardization), `zhou2026externalization`, `zhao2023expel`, `allard2026experiential` (§9 experiences), `yang2025agentic`, `ng2026agent` (§9 governance).
