# WWW 论文生成任务书：语义轨迹图异常检测、Action 定位与经验防御

> 用途：将本文件直接提供给另一个写作 Agent，请其生成一份可供作者参考和二次改写的英文论文初稿。  
> 目标形态：The Web Conference（WWW）Research Track 风格的 ACM `acmart` / `sigconf` 论文草稿。  
> 隐私边界：本文件不包含任何私有数据规模、样本分布、实验结果、运行记录、模型服务信息或本地文件路径。

---

## 1. 给写作 Agent 的直接任务

请基于本任务书生成一篇完整、连贯的英文论文初稿，供作者参考和二次写作。论文围绕一条科学主线展开：工具调用 Agent 的安全风险通常通过任务、推理、环境状态和工具操作之间的依赖逐步形成，因此安全分析既需要完整轨迹的全局上下文，也需要以真实工具操作为单位的局部风险证据。本文将执行轨迹建模为有向语义图，以 Action 执行单元构造候选子图，通过共享图编码器联合完成图级检测和局部定位，再将定位结果转化为可供 Agent 使用的安全经验。

必须遵守以下要求：

1. 输出完整英文论文，而不是提纲、摘要或写作建议。
2. 优先输出 LaTeX，并使用 ACM `acmart` 的 `sigconf` 结构；如果环境不便生成 LaTeX，则输出章节完整的 Markdown。
3. 论文应包含题目、摘要、引言、相关工作、问题定义、数据与建图、方法、实验设置、结果、经验防御、分析与局限、结论。
4. 不得要求、推断或补写作者未提供的实验数据。
5. 任何依赖私有数据或实验结果的句子、表格和图注都使用本文件规定的 `TBD` 占位符。
6. 不得虚构参考文献、BibTeX、数据集出处、实验数字、显著性结论或优先权声明。无法核验的文献位置使用 `[CITATION NEEDED]`。
7. 不得声称方法已经优于 baseline、达到统计显著、实现高精度定位或降低攻击成功率，除非作者之后自行填入相应证据。
8. 使用直接、自然的学术写作，从问题、洞见、机制和证据需求出发，不写面向假想审稿人的防御性措辞。
9. 统一使用 `semantic trajectory graph`、`Action execution unit`、`candidate subgraph`、`contextual semantic-subgraph MIL` 和 `safety experience` 等核心术语。
10. 写作 Agent 只能生成论证结构、方法描述和待填实验接口，不能替作者完成事实核验。

---

## 2. 隐私与信息隔离规则

以下内容不得出现在生成的论文中，也不得在输出末尾复述：

- 私有数据集的真实名称、目录、文件名和存储位置；
- 正常/异常样本数量、划分比例、候选数量和人工标注数量；
- 任意 accuracy、precision、recall、F1、ROC-AUC、PR-AUC、ASR、成本或显著性数值；
- 单个随机种子的结果、均值、标准差、阈值、混淆矩阵和失败案例编号；
- 训练作业编号、checkpoint、日志、运行时间、硬件和 API token 消耗；
- 数据生成、标注、经验生成或评测所使用的私有模型服务名称；
- 作者的本地环境、用户名、绝对路径或尚未公开的工程细节。

写作 Agent 不应尝试从上下文、文件系统、历史对话或常识中恢复上述信息。所有实验位置仅保留语义化占位符，作者稍后在本地手动填写。

---

## 3. 推荐题目与论文定位

### 3.1 推荐题目

首选：

**Detect, Localize, and Defend: Action-Centered Semantic Trajectory Graphs for Tool-Using Agents**

备选：

- **Action-Centered Subgraph Anomaly Detection for Defending Tool-Using Language Agents**
- **From Trajectory Graph Anomalies to Action-Centered Defense Experiences for Tool-Using Agents**

### 3.2 研究对象

研究对象是能够规划、调用工具、读取环境反馈并继续行动的语言模型 Agent。输入是一条从用户任务到最终结果的完整执行轨迹；输出包括：

- 整条轨迹是否异常；
- 哪一个或哪一组 Action 及其语义上下文最可能形成风险；
- 如何将局部风险证据转化为可供 Agent 在后续决策中使用的安全经验。

### 3.3 根本问题

工具 Agent 的攻击不一定表现为单个恶意句子。风险可能从外部状态进入，在推理中被采纳，再通过一个或多个工具调用产生受损结果。扁平文本分类难以显式表示这种跨步骤依赖；仅做整图分类又不能直接回答哪个工具操作造成风险；没有局部证据的告警也难以转化为具体防御策略。

### 3.4 核心洞见

Action 是 Agent 与环境发生实际交互的自然执行边界。以 Action 为锚点，将其输入状态、支撑推理、调用本身、输出状态及相关反思组合成不可拆分的执行单元，可以比固定 hop 邻域更忠实地表示局部操作语义。完整轨迹图与 Action 子图承担互补作用：前者描述全局行为模式，后者聚焦具体风险操作。

---

## 4. 全文故事线

全文采用以下因果链，而不是按模块堆叠内容：

```text
工具 Agent 的风险沿执行依赖传播
→ 扁平文本或单一整图分数难以同时表达传播结构与操作级证据
→ Action 是连接意图、状态和环境后果的自然执行边界
→ 构造有向语义轨迹图和 Action 执行单元候选
→ 共享编码器联合建模完整轨迹与局部候选
→ 图级监督与配对弱监督共同学习检测和候选排序
→ 高风险 Action 子图被转化为可操作的安全经验
→ 检测、定位和防御实验分别检验这条机制链
```

全文只保留一个核心问题：如何从完整 Agent 轨迹中发现异常、定位具有执行语义的风险操作，并使检测证据能够服务于防御。不要将数据构建、图模型、子图定位和经验生成写成互不相关的四个故事。

---

## 5. 建议贡献表述

引言末尾可以使用以下贡献结构，但不得加入没有证据的效果描述：

1. 提出一种面向工具 Agent 的有向语义轨迹表示，联合编码任务、推理、工具调用、环境状态以及边的语义、类型和方向。
2. 提出 Action-centered candidate construction，以完整工具操作而非固定 hop 邻域作为候选子图的原子单位，并沿真实执行依赖逐步恢复上下文。
3. 提出 contextual semantic-subgraph MIL 模型，用共享 Edge-GAT 对齐完整图和候选子图，并通过可学习的局部聚合与全局/局部融合完成图级检测和候选排序。
4. 设计从异常检测、Action 级定位、结构化安全经验生成到 Agent 再决策的评估闭环，分别衡量检测能力、定位质量和防御效果。

不要使用 `the first`、`state-of-the-art`、`significantly outperforms`、`highly accurate` 或类似表述，除非作者之后提供经核验的文献与实验依据。

---

## 6. 方法定义

### 6.1 工具执行轨迹与标签

一条轨迹记录 Agent 从接收任务到产生最终结果的完整过程，包括用户目标、计划与反思、工具调用及参数、环境返回状态和最终结果。图标签记为 $y_G\in\{0,1\}$：0 表示正常完成或成功抵御攻击，1 表示攻击导致错误、越权、泄露或其他受损结果。

数据生成方式、标注者、质量控制细节和一致性结果均写作：

```text
TBD-DATA-PROVENANCE
TBD-LABELING-PROTOCOL
TBD-DATA-QUALITY-CONTROL
```

### 6.2 有向语义轨迹图

将轨迹表示为有向属性图：

$$
G=(V,E,X_V,X_E),
$$

其中 $V$ 和 $E$ 分别表示节点和有向边，$X_V$ 与 $X_E$ 分别表示节点和边特征。

节点类型：

| 节点类型 | 含义 |
|---|---|
| `Problem` | 用户任务或原始目标 |
| `Thinking` | Agent 的计划、分析或反思 |
| `Action` | Agent 发起的工具调用 |
| `State` | 工具输出、环境反馈或最终状态 |

边类型：

| 边类型 | 含义 |
|---|---|
| `computes_from` | Action 产生 State |
| `depends_on` | 后续推理或操作依赖前序信息 |
| `sequential` | 仅具有执行顺序关系 |
| `reflects` | 推理或结论反映某个状态 |
| `branches_from` | 不同计划从共享信息产生分支 |

建图分为两个阶段。第一阶段恢复 `Thinking → Action → State` 等基本执行骨架；第二阶段补充高置信度的跨步骤依赖、分支和汇合边。扩展阶段不能修改第一阶段已经确定的节点、文本和边，建图过程也不能使用图标签。

### 6.3 节点与边表示

节点文本由句向量编码器表示。长文本被划分为有重叠的 token chunks。每个 chunk 独立编码并计算风险门控：

$$
z_{ij}=\operatorname{TextEncoder}(c_{ij}),\qquad
r_{ij}=\sigma(\operatorname{MLP}(z_{ij})).
$$

风险增强后的 chunk 经过 max pooling 得到节点文本表示：

$$
h_i^{text}=\max_j\left(\phi(z_{ij})\odot(1+r_{ij})\right).
$$

节点初始特征进一步拼接节点类型 embedding、相对位置和文本长度。每条边同时编码 justification 文本、关系类型和方向：

$$
g_{ij}=\operatorname{MLP}_E([
\operatorname{TextEncoder}(t_{ij});e_{rel(i,j)};e_{dir(i,j)}]).
$$

具体编码器、chunk 长度、overlap 和特征维度统一使用：

```text
TBD-ENCODER-CONFIGURATION
```

### 6.4 Action 执行单元

以每个 Action $a$ 为锚点构造不可拆分的语义执行单元：

$$
U_a=\{a\}\cup R_a\cup I_a\cup O_a\cup F_a,
$$

其中 $R_a$ 是沿语义入边递归恢复的 Thinking 链，$I_a$ 是支撑该 Action 或 Thinking 的输入 State/Problem，$O_a$ 是 Action 产生的输出 State，$F_a$ 是与输出状态直接相关的反思或结果节点。典型结构为：

```text
输入 State / Problem → Thinking 链 → Action → 输出 State
```

该定义以一次完整工具操作为最小粒度，而不是以节点距离为边界。

### 6.5 候选子图构造

若前一个执行单元的输出 State 被后一个执行单元使用，则建立单元依赖 $U_{a_i}\rightarrow U_{a_j}$。对锚点单元逐层加入完整前置单元：

$$
C_a^{(0)}=U_a,
$$

$$
C_a^{(l+1)}=C_a^{(l)}\cup
\bigcup_{U_p\in\operatorname{Pred}(C_a^{(l)})}U_p.
$$

候选满足以下约束：

- 每个候选以真实 Action 为锚点；
- 节点和边来自原图；
- 候选内部通过真实边连通；
- 每次扩展加入完整执行单元；
- 独立分支分别形成候选，汇合 Action 可形成联合上下文候选；
- 候选数量限制不能删除某个 Action 的全部锚点候选。

### 6.6 共享 Edge-GAT 编码

完整图与候选子图共享同一个 directed Edge-GAT。每层从真实入边邻居聚合：

$$
h_i^{(l+1)}=\operatorname{ResNorm}\left(
h_i^{(l)}+
\sum_{j:(j,i)\in E}
\alpha_{ji}^{(l)}\operatorname{Msg}(h_j^{(l)},g_{ji})
\right).
$$

注意力由源节点、目标节点和边表示共同决定。节点表示通过 Mean/Max pooling 形成图表示：

$$
h_G=\operatorname{MeanPool}(\{h_i\})\Vert
\operatorname{MaxPool}(\{h_i\}).
$$

完整图和候选子图使用共享 LayerNorm 对齐表示尺度。层数、attention heads、隐藏维度和 dropout 使用 `TBD-GRAPH-ENCODER-CONFIGURATION`。

### 6.7 上下文候选评分与图级预测

候选分类器比较局部子图与完整轨迹：

$$
q_k=[h_{C_k};h_G;|h_{C_k}-h_G|;h_{C_k}\odot h_G].
$$

候选异常 margin 和概率分别记为 $m_k$ 与 $p_k=\sigma(m_k)$。局部分支融合最高候选和 Top-K 候选均值：

$$
S_{local}=\alpha\max_k m_k
+(1-\alpha)\operatorname{Mean}(\operatorname{TopK}(\{m_k\})).
$$

最终图级分数为：

$$
S_G=\beta S_{full}+(1-\beta)S_{local},\qquad
p_G=\sigma(S_G),
$$

其中 $\alpha$ 和 $\beta$ 经 sigmoid 参数化并由训练数据学习。

### 6.8 弱监督目标

总损失为：

$$
\mathcal L_{total}
=\mathcal L_{graph}
+\lambda_p\mathcal L_{pseudo}
+\mathcal U(\mathcal L_{normal};s_n)
+\mathcal U(\mathcal L_{rank};s_r).
$$

- $\mathcal L_{graph}$ 是图级交叉熵；
- $\mathcal L_{pseudo}$ 使用正常/异常配对轨迹中的变化 Action 构造候选弱标签；
- $\mathcal L_{normal}$ 抑制正常图中的高风险候选；
- $\mathcal L_{rank}$ 要求同任务异常图的分数高于正常图。

辅助损失使用有界不确定性加权：

$$
v=\operatorname{softplus}(s),\qquad
w=\exp(-v)\in(0,1],
$$

$$
\mathcal U(\mathcal L;s)=w\mathcal L+v.
$$

### 6.9 异常定位与安全经验

推理时先使用验证集阈值判断图级异常。只有完整图被判为异常时，才对候选概率排序并触发经验生成。分数接近时优先保留更小的候选，对高度重叠候选去重；Top-1 作为主要风险证据，Top-K 用于辅助判断和定位评估。

安全经验生成器只接收检测分数、Action 锚点、局部节点文本、真实语义边和 justification，不接收 ground-truth label。输出结构为：

```text
risk_type
what_went_wrong
warning_signals
recommended_agent_policy
supporting_node_ids
confidence
```

经验作为软安全上下文，而不是依据单个检测分数直接阻断。Agent 在工具调用前重新检查目标一致性、输入可信度、参数与数据范围授权，以及潜在泄露或越权后果。

---

## 7. 实验设计与统一占位符

### 7.1 数据与划分

所有数据统计均使用以下占位符：

```text
TBD-DATASET-NAME-A
TBD-DATASET-NAME-B
TBD-PRIVATE-DATASET-NAME
TBD-DATASET-STATISTICS
TBD-SPLIT-PROTOCOL
TBD-ANOMALY-RATIO
TBD-RANDOM-SEEDS
TBD-DATA-LEAKAGE-CONTROL
```

生成的论文可以解释每一项为什么重要，但不得为其填写示例数值。

### 7.2 检测指标

计划报告 ROC-AUC、PR-AUC、异常 precision/recall/F1、macro-F1、specificity、false-positive rate、balanced accuracy 和 confusion matrix。在类别不平衡设置中，应说明为何 PR-AUC 和异常类别指标比 accuracy 更有解释力。

所有结果写成：

```text
TBD-DETECTION-MAIN-RESULTS
TBD-DETECTION-SIGNIFICANCE
TBD-THRESHOLD-ANALYSIS
```

### 7.3 定位指标

计划报告 Action Hit@1、Hit@K/Recall@K、预测子图与变化 Action 上下文的 node/edge IoU、候选子图规模和人工解释有效性。候选生成阶段的覆盖率不能代替最终定位指标。

所有结果写成：

```text
TBD-LOCALIZATION-RESULTS
TBD-CANDIDATE-COVERAGE
TBD-QUALITATIVE-LOCALIZATION-CASES
```

### 7.4 防御指标

计划报告攻击成功率、经验注入后的攻击成功率、绝对与相对变化、detector 命中和漏检子集的攻击成功率、正常任务完成率、正常样本防御触发率，以及经验生成的 token、时间和 API 成本。配对样本可使用 McNemar 检验或 bootstrap 置信区间。

所有结果写成：

```text
TBD-DEFENSE-ASR-RESULTS
TBD-NORMAL-UTILITY-RESULTS
TBD-DEFENSE-SIGNIFICANCE
TBD-DEFENSE-COST
```

---

## 8. Baseline 与消融结构

### 8.1 Baseline 类别

论文应比较以下类别，但具体方法名、版本、配置、引用和结果均由作者之后填写：

- 文本轨迹分类方法；
- 普通图神经网络；
- 关系感知、异构或边感知图神经网络；
- 图异常检测方法；
- LLM-as-a-Judge；
- 面向内容安全的 Guard 模型。

写作 Agent 只生成以下表格接口：

```text
TBD-BASELINE-LIST
TBD-BASELINE-CONFIGURATIONS
TBD-FAIR-COMPARISON-PROTOCOL
TBD-MAIN-COMPARISON-TABLE
```

不同输入范式必须分组展示。直接读取文本轨迹的安全模型与读取语义图的图模型不能被描述为完全相同的输入条件。

### 8.2 Action 执行单元的定位价值

核心对照是固定 hop 候选与 Action 执行单元候选。两者应同时比较候选覆盖、最终 Action Hit@K、子图 IoU 和候选规模。

```text
TBD-FIXED-HOP-VS-ACTION-UNIT
```

### 8.3 全局与局部的互补性

至少比较：

- full graph only；
- Action subgraph only；
- full graph + Action subgraph。

```text
TBD-GLOBAL-LOCAL-ABLATION
```

### 8.4 表示与训练目标消融

建议检验：

- 移除 edge justification；
- 移除 relation type；
- 移除 direction；
- 文本截断、chunk mean 与 chunk risk max；
- 固定与可学习的 $\alpha/\beta$；
- 无 LayerNorm 与共享 LayerNorm；
- 无配对伪标签与 Action 配对伪标签；
- 固定辅助损失权重与有界不确定性权重。

```text
TBD-REPRESENTATION-ABLATIONS
TBD-OBJECTIVE-ABLATIONS
```

### 8.5 防御闭环对照

在相同攻击样本上配对比较：

1. Attack only；
2. Generic warning；
3. Full-graph experience；
4. Random connected-subgraph experience；
5. Detected Action-subgraph experience；
6. Oracle Action-subgraph experience。

Oracle 组表示定位信息的上限，Generic warning 区分通用提示效应，Full-graph 和 Random-subgraph 区分局部证据本身的作用。正常样本同步评估任务效用与误触发。

```text
TBD-DEFENSE-CONTROLLED-COMPARISON
```

---

## 9. 各章节写作要求

### 9.1 Abstract

采用“挑战 → 洞见 → 方法 → 证据接口”的结构，控制在约 180–220 词。摘要应说明 Action 是语义执行边界、完整图和候选子图被联合建模、局部证据可用于经验防御。结果句必须写成：

```text
Across [TBD-EVALUATION-SCOPE], the proposed method achieves [TBD-KEY-RESULTS] under [TBD-PROTOCOL].
```

不得用想象出的形容词代替数字。

### 9.2 Introduction

建议五段：

1. 工具调用扩大 Agent 能力，也使外部内容、状态和操作后果形成连续攻击面；
2. 现有文本级或整轨迹判断难以显式表示跨步骤依赖并提供操作级证据；
3. 根本原因是风险单位与执行单位错位，固定 hop 也可能截断完整工具操作；
4. 提出语义轨迹图、Action 执行单元和全局/局部共享编码；
5. 贡献与证据预览。

所有关于现有研究的事实都需要真实引用。不要先写“现有方法普遍失败”再寻找支持它的文献。

### 9.3 Related Work

建议分为三组：

- Tool-using Agent security 与 prompt injection / indirect injection；
- Agent trajectory、execution trace 与图结构建模；
- 图异常检测、弱监督定位与 experience/reflection-based defense。

每组说明其与本文问题的关系和技术区别，避免逐篇罗列。最接近的工作需要单独说明。无法核验时使用 `[CITATION NEEDED]`。

### 9.4 Problem Formulation

明确给出轨迹、图、图标签、Action 执行单元、候选集合、图级检测、局部定位和防御目标。符号首次出现时定义；公式前解释其作用，公式后说明其含义。

### 9.5 Dataset and Graph Construction

使用公开数据集 A、公开数据集 B 和私有数据集三个抽象名称。说明需要报告的数据来源、标签、匹配控制、去除无 Action 轨迹、分组切分和结构审计，但所有私有细节保留为 `TBD`。

### 9.6 Method

推荐小节顺序：

1. Overview；
2. Chunk-aware node and edge representation；
3. Action execution units；
4. Dependency-aware candidate construction；
5. Shared Edge-GAT and contextual candidate scoring；
6. Global-local aggregation；
7. Weakly supervised objectives；
8. Localization and safety-experience generation。

每个模块按“为什么需要 → 如何工作 → 输出什么 → 哪个实验验证”展开，避免公式堆叠。

### 9.7 Experiments

先说明统一设置，再按检测、定位、机制消融和防御组织结果。每个结果段落预留研究问题、观察和支持的解释。没有数字时保留完整表格骨架与 `TBD`，不得编写虚假的趋势性结论。

### 9.8 Analysis and Limitations

应预留以下分析位置，但不写成已经观察到的事实：

- 数据生成或采集过程是否造成风格伪影；
- 标签是否依赖自动判定以及一致性如何；
- 检测排序能力是否稳定转化为阈值后性能；
- 候选覆盖与真实定位准确率之间的差异；
- 经验生成器、执行 Agent 和 Judge 是否存在同源模型偏差；
- 离线决策评估与真实工具执行之间的差距；
- detector 漏检对经验防御覆盖率的限制。

每项最终都应由作者填写观察、证据和对结论的影响。统一使用：

```text
TBD-OBSERVED-LIMITATIONS
TBD-THREATS-TO-VALIDITY
```

### 9.9 Conclusion

结论只总结方法洞见，不写结果优越性。建议结束于：Action-centered semantic subgraphs 为工具轨迹风险提供了与执行边界一致的局部表示，而全局与局部联合建模为连接检测、定位和防御提供了统一框架。最终效果结论由作者在补齐证据后填写。

---

## 10. 表格与图形接口

建议生成以下占位内容：

1. 方法总览图：trajectory → semantic graph → Action units → candidates → shared Edge-GAT → detection/localization → safety experience；
2. Action 执行单元和候选扩展示意图，展示链、分支和汇合；
3. `TBD-DATASET-TABLE`；
4. `TBD-MAIN-DETECTION-TABLE`；
5. `TBD-LOCALIZATION-TABLE`；
6. `TBD-ABLATION-TABLE`；
7. `TBD-DEFENSE-TABLE`；
8. `TBD-QUALITATIVE-CASES`。

LaTeX 表格使用 `booktabs`，不使用竖线或 `\hline`。表格中不要放示例数字。每张表或图只承担一个主要信息。

---

## 11. 引用规则

1. 数据集、baseline、文本编码器、GAT/RGCN/HGT、MIL、不确定性加权、Agent 安全和 prompt injection 等外部事实需要引用经核验的原始来源。
2. 不得生成未经核验的作者、题名、年份、venue、DOI、URL 或 BibTeX。
3. 相关工作中的比较必须由原论文支持，不得根据方法名称推断其输入、监督方式或能力。
4. 报告已有论文数字时，应引用方法论文和数字的实际来源；本任务书不提供任何可供报告的数字。
5. 如果写作 Agent不能进行可靠检索，则只保留 `[CITATION NEEDED: topic]`。

---

## 12. 统一 TBD 字典

生成的论文只使用以下占位符，方便作者之后全局搜索和替换：

| 占位符 | 作者需要补充的内容 |
|---|---|
| `TBD-DATA-PROVENANCE` | 数据来源与构造流程 |
| `TBD-LABELING-PROTOCOL` | 标签定义、标注者与一致性 |
| `TBD-DATASET-STATISTICS` | 数据规模与类别分布 |
| `TBD-SPLIT-PROTOCOL` | 数据划分与泄漏控制 |
| `TBD-ENCODER-CONFIGURATION` | 文本编码与 chunk 参数 |
| `TBD-GRAPH-ENCODER-CONFIGURATION` | 图编码器与训练超参数 |
| `TBD-BASELINE-LIST` | 最终 baseline 名单与引用 |
| `TBD-MAIN-DETECTION-TABLE` | 图级检测结果 |
| `TBD-LOCALIZATION-TABLE` | Action 定位结果 |
| `TBD-ABLATION-TABLE` | 全局/局部、表示与目标消融 |
| `TBD-DEFENSE-TABLE` | ASR、正常效用与成本 |
| `TBD-KEY-RESULTS` | 摘要中的最终关键结果 |
| `TBD-DETECTION-SIGNIFICANCE` | 检测显著性或置信区间 |
| `TBD-DEFENSE-SIGNIFICANCE` | 防御配对检验或置信区间 |
| `TBD-OBSERVED-LIMITATIONS` | 已观察到的失败模式与边界 |
| `TBD-QUALITATIVE-CASES` | 经作者筛选的案例 |

不得把占位符改写为虚构的自然语言结果。例如，在 `TBD-KEY-RESULTS` 未填时，不得写“the method consistently outperforms all baselines”。

---

## 13. 最终交付格式

请输出：

1. 一份完整英文论文初稿；
2. 一个单独的 `TBD / Evidence Needed` 清单，逐项指出缺失证据影响的章节、表格和句子；
3. 一个引用待核验清单，不得使用虚构 BibTeX 填充；
4. 若输出 LaTeX，保证文档结构可编译，并将缺失图片用可编译占位框表示；
5. 不输出写作过程、自我评价、虚拟审稿分数或投稿成熟度判断；
6. 不访问、请求或复述作者的私有实验数据。

这份初稿的职责是搭建准确的科学论证和方法表达，并为作者保留清晰、可检索的证据接口。