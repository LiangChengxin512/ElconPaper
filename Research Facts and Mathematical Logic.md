# Research Facts and Mathematical Logic

This file is the evidence brief for drafting the 2027 ElCon conference paper. The intended topic is multivariate time-series anomaly detection for the **Signal Processing & Analysis** track. It records the author-confirmed experiment sequence, implementation details that can be checked in the repository, supplied results, and unresolved reporting details. Use it together with the data tables and figures in this folder.

## Evidence sources and priority

Use these sources in this order when wording conflicts:

1. The author's clarification for this paper: the supplied `Ablation Experiment/result.csv` is the M0–M4 ablation result across eight datasets, with one fixed model sequence for every dataset and no dataset-dependent model routing. The fixed sequence is `TranAD` → `TranAD_C` → `TranAD_C_G` → `TranAD_C_G_E` → `TranAD_C_G_E+TOPK`; M4 is `TranAD_C_G_E+TOPK`. The other supplied experiments use this final M4 model.
2. The numeric values as printed in the CSV and other supplied tables. Preserve them, but do not infer undocumented sample counts or statistical meaning.
3. The checked C/G/E implementation in `src/tranad_variants.py` and shared training/scoring utilities in `src/experiment_utils.py`, only for implementation details that match the experiment described above.
4. `Paper Material/Env.md` and the supplied experiment readmes.
5. `Paper Material/registration-form.docx` and `Paper Material/paper-template.docx` for conference and formatting information.

`Ablation Experiment/ABLATION_GUIDE.md` contains an incorrect account of the M0–M4 mapping and dataset routing. Do not use its routing description, or its M3/M4 score-processing and post-processing narrative, to describe `result.csv`. The workspace also contains other progressive/experimental code paths with route logic and optional score guards; their presence does not establish that those paths generated this table. If a run-specific setting is not stated in the files below, mark it for author confirmation rather than importing a setting from a different code path.

The folder does not include every run log, data split manifest, or comparison protocol. Where those details are missing below, mark them for author confirmation; do not fill them in from assumptions.

## Conference and manuscript constraints

- Event named in the supplied form: **2027 ElCon Conference of Young Researchers in Communication and Networking (2027 ElCon-CN)**.
- Track/section: **Signal Processing & Analysis**.
- Dates and venue printed on the supplied registration form: **February 2–4, 2027, St. Petersburg, Russia**. Treat these as the contents of the provided form, not as independently re-verified current event details.
- The registration form requires a **150–200-word abstract** and labels its intended content “problem-method-results.”
- The supplied paper template is an A4 Word conference template with built-in section and column styles. Preserve its styles and layout. It requires a Conclusions block and says to remove all instructional/template text before submission. It does not state a paper page limit in the supplied copy.
- The template says not to place symbols, special characters, footnotes, or mathematics in the title or abstract. For those fields, use plain English, no equations or LaTeX, and avoid model notation such as `TranAD_C_G_E+TOPK`. Use ordinary prose and define unavoidable abbreviations.
- The registration form has author, affiliation, student status, location, email, phone, and copyright-transfer-contact fields. Their values are not present in this research material.
- `Nature-Writting.md` describes the nature-writing skill as an evidence-led drafting and claim-organization tool. The target here is a conference paper using the supplied conference template, not a Nature Portfolio journal submission.

## Study question and defensible contribution

**Study question:** How does a fixed sequence of TranAD extensions—temporal convolution, feature gating, phase-output blending, and Top-K reconstruction-error aggregation—affect multivariate time-series anomaly-detection results?

**Defensible contribution, subject to resolving the reporting checks below:** The study compares a fixed M0–M4 ablation sequence across eight datasets. The final M4 configuration uses the C, G, and E components together with Top-K score aggregation. In the supplied table, M4 has a higher displayed F1 point estimate than M0, M1, M2, and M3 on all eight datasets. This is a descriptive table-level comparison, not evidence of statistical significance, a guaranteed stage-by-stage improvement, or state-of-the-art performance.

Use the same model-component sequence across datasets. Do not describe dataset-dependent model routing, dataset-specific component substitutions, M4 background-crossing filters, or a SWaT wake-up rule as part of these results. Do not claim causality, online operation, universal anomaly detection, or a mathematical guarantee of improved metrics.

### Ablation ladder

| Variant | Fixed configuration | What is added at this step |
| --- | --- | --- |
| M0 | `TranAD` | Base model |
| M1 | `TranAD_C` | Temporal convolution adapter C |
| M2 | `TranAD_C_G` | Feature gate G added to C |
| M3 | `TranAD_C_G_E` | Trainable phase-output blend E added to C+G |
| M4 | `TranAD_C_G_E+TOPK` | Top-K aggregation of channel reconstruction errors added to C+G+E |

This exact sequence is the author's clarification of what the M0–M4 labels in `result.csv` mean. It is fixed across datasets; dataset routing is not part of this experiment. The other supplied experiments use the final M4 configuration. The exact Top-K setting (fixed `k`, adaptive `k`, or a guard/fallback option) is not recoverable from `result.csv` alone; do not invent it. The corresponding run configuration should be recorded before stating a specific `k` policy.

## Model definition from the current code

Let a multivariate sequence be `X = (x_1, ..., x_T)`, where `x_t` is in `R^D`. The TranAD runner uses overlapping windows of length `L = 10`. In the current training and scoring path, the reconstruction target is the final sample of the input window. The initial windows are padded by repeating the first observation. Describe score-to-label time alignment from the actual preprocessing/run logs before publication; do not silently change this to a future-prediction claim.

The base TranAD backbone uses one Transformer encoder and two Transformer decoders. The first phase decodes from the window with a zero conditioning tensor. The second phase is conditioned on the squared difference between the first-phase output and every sample in the input window. Let `W` be the length-10 input window, `y = W[-1]` the last-sample training/scoring target, and `y^(1)` the first-phase output. The current code computes

`C^(1) = 0`, and `C^(2)[i,d] = (y^(1)[d] - W[i,d])^2` for each window position `i` and channel `d`.

Thus the phase-2 conditioning tensor is broadcast against the full input window; it is not simply `(y^(1) - y)^2` for the last target alone. The second decoder uses the window together with this conditioning tensor to produce `y^(2)`.

When E is included, the phase-output blend is

`y^(2,blend) = (1 - lambda) y^(1) + lambda y^(2)`, where `lambda = sigmoid(a_E)` is a learned scalar.

The implementation has one encoder layer and one layer in each decoder, model width `2D`, `D` attention heads, feed-forward width 16, and dropout 0.1. These are code facts; check the exact instantiated dimensions and training configuration for the runs before describing them as the final experimental hyperparameters.

### C, G, and E components

- **C, temporal convolution adapter:** a depthwise 1D convolution with kernel size 3, GELU, pointwise 1D convolution, dropout, a learned residual gate, and LayerNorm. If `H` is its input, its operation is `C(H) = LayerNorm(H + sigmoid(a_C) × Dropout(PWConv(GELU(DWConv1D(H)))))`. The current `TemporalConvAdapter` uses symmetric padding (`padding=1`), so do not call it causal or claim it only uses past samples.
- **G, feature gate:** computes each channel's mean and standard deviation over the input window, maps these statistics through an MLP and sigmoid gate, then applies a bounded multiplicative modulation. A training-derived mask enables gating only for channels with more than 10 unique training values and standard deviation above `1e-3`.
- **E, phase-output blend:** learns the scalar blend between the first- and second-phase reconstructions above. It is not an embedding module in this implementation.

For clarity, the mathematical form of G in the current `FeatureGate` implementation is as follows. Let `H ∈ R^(L×D)` be the feature sequence entering G (the output of C in M2/M3/M4 when the components are composed). Compute per-channel temporal mean `m_d` and standard deviation `v_d`, then `g = sigmoid(MLP([m_1,…,m_D,v_1,…,v_D]))`. The output modulation is `H'[:,d] = H[:,d] × (1 + q_d × sigmoid(a_G) × (g_d − 0.5))`, where `q_d` is the channel eligibility mask. The progressive training script derives `q_d` from training data using a unique-value count greater than 10 and standard deviation greater than `1e−3`; only report this exact mask as part of the result protocol if its run config confirms that script was used. This per-channel gate is not dataset routing.

The `C` convolution uses symmetric padding, so it is not causal. The same C+G+E component configuration defines M4 for all datasets; the number of input channels `D` may differ by dataset, as expected for multivariate inputs. Ignore any implementation branch that substitutes a different combination by dataset when describing this experiment.

## Training facts

- The TranAD variant training path uses the two-phase reconstruction loss. For training epoch `n = epoch + 1`, the implementation weights the first reconstruction by `1/n` and the second by `1 - 1/n`, with elementwise MSE averaged over the batch and features:

  `L_n = (1/n) MSE(y^(1), y) + (1 - 1/n) MSE(y^(2), y)`.

  For M4 with E enabled, `y^(2)` in this expression is the blended second-phase output. This objective contains no dataset-specific routing term. Do not attribute the background filter or SWaT wake-up heuristic to training; those are not part of the author's M4 definition for these results.
- The shared variant runner uses AdamW and StepLR (`step_size=5`, `gamma=0.9`) by default. Verify run records before presenting these as the exact hyperparameters used in `result.csv` or in other experiment tables.
- The supplied data-ratio and window-size studies use final model M4 according to the author's experiment description. Their run script/configuration is not included here, so preserve the tabulated values and mark their sampling/training protocol as an author check. The current shared TranAD variant uses window length 10; do not claim the window-size sweep can be reproduced from that default runner without the sweep configuration.

## Reconstruction scores and Top-K aggregation

Let `e_(t,d) = (y_hat_(t,d) - y_(t,d))^2` be the nonnegative reconstruction error for channel `d` at time `t`. The mean score is

`s_mean,t = (1/D) sum_d e_(t,d)`.

For sorted channel errors `e_(t,(1)) ≥ e_(t,(2)) ≥ … ≥ e_(t,(D))`, where `D` is the number of channels, Top-K aggregation is

`s_topk,t = (1/k) sum_{j=1}^k e_(t,(j))`, with `1 ≤ k ≤ D`.

This averages the `k` largest channel errors at each time; it is not the maximum unless `k=1`, and it is not the all-channel mean unless `k=D`. If the experiment uses an adaptive setting, replace `k` with the run-defined `k_t` and describe the selection rule only after verifying the run config. The result table itself does not state the value or selection policy for `k`.

## Thresholding and score-to-label evaluation

The exact thresholding and any optional score guard must be confirmed from the run record used to create these results. The M4 definition established here adds Top-K reconstruction-error aggregation; it does not include the unrelated background-crossing filter or SWaT platform wake-up rule described in the erroneous guide/progressive code path. Do not write those rules into the Method section for these experiments.

## Evaluation and metric definitions

- The thresholded predictions use `score > threshold`. The evaluation code then applies point adjustment: when a predicted positive occurs inside a ground-truth anomaly interval, the interval is filled as positive for point-level metric calculation. This is a label-informed evaluation convention; distinguish it from the label-free threshold and score-selection steps.
- Precision, recall, and F1 are computed from these adjusted binary predictions. The usual F1 relationship is `F1 = 2PR / (P + R)` (implementation includes small numerical epsilons).
- **Important metric caveat:** the current `calc_point2point` function computes `roc_auc_score(actual_binary, adjusted_prediction_binary)`. Therefore the field called `ROC-AUC` in the result files is based on a single thresholded, point-adjusted binary prediction, not on ranking by the continuous anomaly score. For binary scores it is equivalent to balanced accuracy, `(TPR + TNR)/2`. Do not present it as conventional threshold-free ROC-AUC unless it is recomputed from continuous scores under a documented protocol. The sensitivity tables inherit the same label `ROC-AUC`, but their run code is not included, so confirm their metric implementation independently.
- Do not compare reported AUC values to literature AUCs until the metric implementation and threshold protocol match.

## Supplied results and safe descriptions

### Ablation results and M4 final row across eight datasets

`Paper Material/Ablation Experiment/result.csv` contains rows for every M0–M4 stage in the fixed sequence above, across eight datasets. Its M4 row reports the final `TranAD_C_G_E+TOPK` configuration. The same fixed model sequence applies across datasets; there is no dataset route. According to the author, the other supplied studies also use this final M4 model.

The source prints each cell as `value ± value`; however, `seed_count` is `1` on every row. The meaning and provenance of the second number therefore need author confirmation. Preserve the table notation internally, but do not call the second number a standard deviation or state a replicate count in the manuscript until verified. The experiment guide's claim that `result.csv` is not an input or output of the ablation experiment is incorrect.

| Dataset | Precision | Recall | F1 | Field labeled ROC-AUC |
| --- | ---: | ---: | ---: | ---: |
| MBA | 0.9561 ± 0.0052 | 1.0000 ± 0.0000 | 0.9776 ± 0.0072 | 0.9720 ± 0.0020 |
| MSL | 0.9038 ± 0.0076 | 1.0000 ± 0.0000 | 0.9495 ± 0.0062 | 0.9916 ± 0.0027 |
| NAB | 0.9101 ± 0.0019 | 1.0000 ± 0.0000 | 0.9529 ± 0.0034 | 0.9998 ± 0.0000 |
| SMAP | 0.8367 ± 0.0041 | 1.0000 ± 0.0000 | 0.9111 ± 0.0017 | 0.9908 ± 0.0022 |
| SMD | 0.9204 ± 0.0064 | 0.9974 ± 0.0015 | 0.9573 ± 0.0070 | 0.9942 ± 0.0035 |
| SWaT | 0.9921 ± 0.0044 | 0.6995 ± 0.0058 | 0.8205 ± 0.0037 | 0.8525 ± 0.0075 |
| UCR | 0.9134 ± 0.0024 | 1.0000 ± 0.0000 | 0.9547 ± 0.0045 | 0.9975 ± 0.0022 |
| Synthetic | 0.9642 ± 0.0026 | 1.0000 ± 0.0000 | 0.9818 ± 0.0018 | 0.9992 ± 0.0000 |

The supplied table's M4 F1 point estimate is higher than each preceding stage (M0–M3) for all eight datasets. This is a descriptive table-level comparison only; no paired significance test or confirmed repeat count is supplied. The two comparison LaTeX files use `Ours` values matching the M4 point estimates to the displayed precision. Their bold/`\\best` annotations are stale per `Comparison Experiment/readme.md`; recalculate rankings from verified values or omit bold-ranking claims.

### Sensitivity tables

- `training_ratio_evaluation_v2.csv` lists training ratios 20%, 40%, 60%, 80%, and 100% for the same eight datasets. Its tabulated F1 and field labeled ROC-AUC increase monotonically with the ratio on every dataset. The standard-deviation columns are present, but seed counts and the sampling rule for selecting each ratio are absent. The AUC implementation also needs independent confirmation.
- `window_size_evaluation_v2.csv` lists window sizes 5, 10, 20, 50, 100, and 500. Window size 50 has the highest tabulated F1 among those candidates for all eight datasets. The file does not identify the number of runs or uncertainty. The SMD F1 at size 50 is `0.9574`, while the ablation table gives `0.9573`; retain each source value and reconcile before merging tables.
- Because the current progressive runner hardcodes window length 10, include the experiment script/configuration that generated these sweeps before claiming they are reproducible from the current runner.

### Channel diagnosis table

`Anomaly Analysis/anomaly analysis.tex` reports SMD values for HitRate@100%, HitRate@150%, NDCG@100%, and NDCG@150%. The Ours row is `0.5026`, `0.6452`, `0.4982`, and `0.6227`. It is slightly higher than the TranAD row (`0.4981`, `0.6401`, `0.4941`, `0.6178`) in all four displayed columns, while MERLIN and CAE-M lead selected columns. The folder does not define the ranking unit, relevance labels, meaning of 100%/150%, or exact HitRate/NDCG formulas. Do not give formal metric equations or claim best overall until those definitions and evaluation scripts are supplied.

### Baseline comparisons

- `Comparison Experiment/comparison.tex`: 10 baseline/model rows across NAB, UCR, MBA, SMD, SMAP, MSL, SWaT, and Synthetic.
- `Comparison Experiment/comprison_latest_model.tex`: D3R, DMamba, TFMAE, CATCH, and Ours across SMD, MSL, SMAP, and SWaT.
- The comparison readme warns that bold/`\\best` formatting is outdated. Baseline citations, code versions, thresholding, point-adjustment use, and run parity are not fully documented in this folder. State table values faithfully, but make cross-method superiority claims only after these protocols and citations are verified.

## Recorded computing environment

`Env.md` records Ubuntu 22.04.4 LTS (x86_64), two Intel Xeon Gold 6248R CPUs (48 physical cores / 96 threads total), one NVIDIA A100 PCIe 40 GB, driver 560.35.03 / CUDA 12.6, and approximately 768 GB RAM. Treat RAM as approximate. Python, PyTorch, CUDA runtime build, package versions, and per-experiment device/config files are not recorded in this folder; confirm them before writing a reproducibility statement.

## Author checks needed before a submission-ready draft

1. Resolve why `result.csv` reports `seed_count = 1` alongside nonzero `±` values; provide raw seed-level metrics and define whether the second values are standard deviations, confidence intervals, or something else.
2. Decide whether the field named `ROC-AUC` should be recomputed from continuous anomaly scores. The current M4 evaluation implementation uses binary, point-adjusted predictions.
3. Supply the exact runner/configs and randomization policy for training-ratio and window-size sweeps; reconcile SMD F1 `0.9574` versus `0.9573` at window 50.
4. Supply the definitions and script for SMD channel HitRate/NDCG diagnosis metrics.
5. Verify that all `Ours` comparison cells correspond to the same fixed M4 model and evaluation protocol; verify baseline citations, versions, and protocol parity.
6. Confirm data sources, feature counts, train/test lengths, preprocessing/scaling, missing-value handling, label aggregation, and exact score-label alignment for every dataset.
7. Confirm the actual training seeds, checkpoint epoch, device, package versions, and hardware used for each result table.
8. Confirm the Top-K setting used in M4 (fixed `k` or adaptive `k_t`), its selection/guard rule if adaptive, and the threshold protocol. Do not use dataset routing or M4 post-processing claims from `ABLATION_GUIDE.md`; check the architecture diagram against the fixed C+G+E model before finalizing it. Do not claim causality.
9. Fill all author, affiliation, contact, funding, and copyright-transfer fields from verified author information.
10. Check the current conference instructions for any page limit or submission rule not present in the supplied registration form/template.
