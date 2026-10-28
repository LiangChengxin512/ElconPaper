# Nature-Writing Prompt Pack

These prompts are intended for Antigravity after copying the complete `Paper Material` folder into its working directory. They ask the nature-writing skill to draft in English while using the supplied code-checked facts and tables as evidence. The target is the 2027 ElCon conference paper and registration abstract, not a Nature Portfolio journal submission.

## Prompt for the registration-form abstract

```text
请使用 Nature-writing skill，为 2027 ElCon Conference of Young Researchers in Communication and Networking 的 Signal Processing & Analysis track 起草报名表摘要。

请先通读当前 Paper Material 文件夹，尤其是：
- Research Facts and Mathematical Logic.md
- Nature-Writting.md
- Ablation Experiment/result.csv 和 ABLATION_GUIDE.md
- Comparison Experiment/readme.md、comparison.tex、comprison_latest_model.tex
- Sensitivity Analysis/readme.md 及两个 CSV
- Model Architecture/readme.md 和架构图
- registration-form.docx 与 paper-template.docx

输出必须符合报名表：英文摘要 150–200 words，内容按 problem, method, results 组织。先给一个推荐版本，再给一个备选版本；每个版本单独给出精确 word count，并列出它使用的结果数据及对应来源文件。

事实与写法规则：
1. 只写材料明确支持的事实。把 Research Facts and Mathematical Logic.md 中的代码事实作为当前实现说明，把表格当作报告值。不要虚构作者、数据集规模、采样频率、统计显著性、运行次数、数据处理流程、引用或理论保证。
2. 以 Research Facts and Mathematical Logic.md 开头列出的作者确认作为 M0–M4 的事实来源：所有数据集采用相同的固定消融序列，M0=TranAD，M1=TranAD_C，M2=TranAD_C_G，M3=TranAD_C_G_E，M4=TranAD_C_G_E+TOPK。不存在数据集路由；其他提供的实验使用最终模型 M4。ABLATION_GUIDE.md 对模型映射/路由和 M3/M4 处理的描述有误，不要照搬。
3. 重点围绕多变量时间序列异常检测及信号分析任务。用简洁语句交代问题、方法、八个数据集上的核心结果，以及结果适用范围。优先选可核实的 F1 结果；除非先解决事实说明中的指标口径问题，否则不要把表格中名为 ROC-AUC 的数值称作标准 ROC-AUC，也不要用它支撑领先性结论。
4. `result.csv` 的 seed_count 与 `±` 数值存在未解决的矛盾。不要称这些 `±` 为标准差/置信区间，不要声称多次重复或统计显著。可以报告表格中的单个显示值，但必须在结果核对清单中说明这项数据来源问题。
5. 表格中的旧粗体和 `\\best` 标记已过时。不要照抄它们作为“最佳”或 SOTA 依据。可准确说 M4 在当前消融表的八个数据集上均有高于 M0–M3 的 F1 显示值，但不得据此宣称统计显著、对每个指标或基线都最好。
6. 报名表和会议模板禁止在题目或摘要里放符号、特殊字符、脚注和数学公式。标题与摘要用普通英文文字，不写 LaTeX、希腊字母、下标、上标、加号表达式或公式；避免 `TranAD_C_G_E+TOPK` 这种模型记法。正常英文标点和必要的普通十进制结果数字可以使用。
7. 语气克制，写出证据边界。若一个关键结论因当前数据问题无法负责任地写进摘要，请提供带 `[AUTHOR CHECK]` 标记的候选表述，并说明具体需要确认什么，不要自行猜测。

请按此结构返回：
A. 推荐英文摘要（150–200 words）和 word count。
B. 备选英文摘要（150–200 words）和 word count。
C. 两版各自的逐句事实来源表。
D. 报名前必须由作者确认的事项，最多列五项，按影响摘要可信度排序。

摘要正文必须可直接粘贴到报名表，不要在摘要正文中插入来源标记、脚注、公式或待办说明。来源表与作者核对项单独放在摘要之外。
```

## Prompt for the conference paper draft

```text
请使用 Nature-writing skill，根据当前 Paper Material 文件夹撰写一篇面向 2027 ElCon Conference of Young Researchers in Communication and Networking、Signal Processing & Analysis track 的英文会议论文初稿。输出应便于之后套用同目录的 paper-template.docx。

先阅读整个 Paper Material 文件夹。特别把 Research Facts and Mathematical Logic.md 作为代码实现和证据边界的核对清单；把 CSV/TeX 表格视为当前提供的实验数值；把 Nature-Writting.md 视为 nature-writing 能力与输出说明。复制到 Antigravity 工作目录后如果没有仓库源代码，不要假设可以访问代码；遵循研究事实文件中已经核实的实现细节。

写作目标：
- 形成一条由问题、研究缺口、可回答问题、方法、实验设计、结果、局限组成的证据链。目标读者是信号处理与时间序列分析研究者。
- 给出 2–3 个朴素、准确、无公式符号的英文标题候选；给出一个 150–200-word 英文摘要候选，符合 registration-form.docx 与 paper-template.docx 的标题/摘要限制，并提供 word count。
- 论文正文依模板可组织为 Introduction、Related Work、Method、Experimental Setup、Results、Discussion、Conclusions、Acknowledgments、References。模板中要求 Conclusions；套版时保留内置 A4、列布局、字体和标题样式，删除模板说明文字。所给模板/报名表未列出总页数限制，请勿自行编造页限。
- 在 Method 中定义时间序列、通道、窗口、两阶段重构、通道平方误差、C/G/E 模块和 Top-K 通道误差聚合。使用 Research Facts and Mathematical Logic.md 中的公式并在公式附近定义符号。对 Top-K 只说明已知的一般公式；具体 `k`、固定或自适应策略、是否有 guard/fallback 都要等原始运行配置确认，不要从其他代码路径推断。不要加入数据集路由、M4 背景毛刺过滤或 SWaT 平台唤醒。
- 准确写出固定的 M0–M4 顺序，并说明同一组件序列用于所有数据集。C 是 kernel 3 且使用对称 padding 的时间卷积，不是因果卷积；G 是特征门控；E 是两阶段输出的可训练标量混合，不是 embedding。可以说明通道数 D 随数据集变化，但不能把输入维度变化描述成模型路由。
- 清楚区分模型训练、无标签分数聚合/阈值校准、以及用标签进行 point-adjusted evaluation。说明 point adjustment 会使用 ground-truth anomaly interval。不要称整套评估完全无标签。
- 把 M0–M4 在八个数据集的消融、基线比较、训练比例、窗口大小、SMD 通道诊断分别安放到合适的 Results 子节或表注；其中消融表及其他提供的实验以固定最终模型 M4 为依据。只在能由材料支持时陈述跨数据集趋势；把单点估计描述为观察值，不推断统计显著性。
- 若列出 ROC-AUC，必须先解决实现口径问题：当前代码对 point-adjusted binary predictions 调用 roc_auc_score，而不是对连续异常分数计算常规 ROC-AUC。不能默默改名或把它与文献中的标准 ROC-AUC 比较；请将问题列入作者核对事项，必要时先在草稿中标注 `[AUTHOR CHECK: verify/recompute AUC]`。
- 对 SMD HitRate/NDCG，只能报告表中数值并注明定义需补充；不要自行发明 top-k、相关性或排名公式。
- 忽略旧 `\\best`/粗体标记，不据此写“最佳方法”或 SOTA。任何基线优势说法都必须先核实数据、指标、阈值、point-adjustment、运行设置及引用的一致性。
- 引言和 Related Work 需要引用时，优先整理材料中已提供的原始数据集/模型参考文献。不要编造引用或 DOI；若证据不足，使用清晰的 `[CITATION NEEDED: claim]` 标记并在作者核对表说明要补哪类来源。不要为填满引言而加入未经核实的最新文献。
- Discussion 应说明方法贡献和实测范围，同时明确局限：结果数值的 seed_count/± 矛盾；AUC 口径；Top-K 具体配置及阈值协议待核实；敏感性实验脚本/采样协议缺失；SMD 诊断公式未给出；硬件软件记录不全。不要把 M4 描述成含有背景过滤、SWaT 唤醒或其他 score correction。
- 不得编造作者/机构、样本量、通道数、采样率、预处理、统计检验、实际训练超参数、部署延迟或理论保证。缺失项用 `[AUTHOR TO CONFIRM: ...]`，不要猜。

最终交付顺序：
1. 一页以内的 claim–evidence map：每个主张、对应结果/文件、支持强度、未决限制。
2. 论文结构提纲及每节目标。
3. 完整英文论文初稿，标题、摘要和关键词在前，正文按会议模板组织。
4. 表格/图建议及每张图表应承载的结论；不要伪造不存在的图或数值。
5. 作者核对清单，按“会改变摘要/主结论”“影响可复现性”“格式/作者信息”分组。
6. 给出状态 `ready`、`ready_with_author_checks` 或 `blocked`，并用一两句说明判定原因。根据现有未解决的数据与指标问题，除非用户补充证据，不要标记为无条件 ready。
```

## Suggested Antigravity sequence

1. Copy the full `Paper Material` folder so the two prompt source documents and all tables/figures remain together.
2. Run the registration abstract prompt first; review the exact word counts and the unresolved metric/seed questions.
3. Run the paper prompt using the selected abstract as a style/claim reference, then answer the generated author-check list before treating the draft as submission-ready.
