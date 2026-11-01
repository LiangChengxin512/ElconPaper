import docx, io, zipfile
from docx.shared import Inches

def strict_to_transitional(path):
    zin = zipfile.ZipFile(path, 'r')
    buf = io.BytesIO()
    zout = zipfile.ZipFile(buf, 'w')
    replacements = [
        (b'http://purl.oclc.org/ooxml/officeDocument/relationships', b'http://schemas.openxmlformats.org/officeDocument/2006/relationships'),
        (b'http://purl.oclc.org/ooxml/officeDocument/', b'http://schemas.openxmlformats.org/officeDocument/2006/'),
        (b'http://purl.oclc.org/ooxml/wordprocessingml/main', b'http://schemas.openxmlformats.org/wordprocessingml/2006/main'),
        (b'http://purl.oclc.org/ooxml/drawingml/', b'http://schemas.openxmlformats.org/drawingml/2006/'),
    ]
    for item in zin.infolist():
        data = zin.read(item.filename)
        if item.filename.endswith('.xml') or item.filename.endswith('.rels'):
            for old, new in replacements:
                data = data.replace(old, new)
        zout.writestr(item, data)
    zout.close()
    zin.close()
    buf.seek(0)
    return docx.Document(buf)

doc = strict_to_transitional('paper-template.docx')
body = doc._element.body

# 1. Update Title in P[0]
title_text = "Multivariate Time-Series Anomaly Detection via Modular Temporal Convolutions and Adaptive Top-K Error Aggregation"
doc.paragraphs[0].text = title_text

# 2. Update Authors in P[3], P[4], P[5], P[6]
doc.paragraphs[3].text = "line 1: [1st Given Name Surname]\nline 2: dept. name of organization\nline 3: [name of organization]\nline 4: [City, Country]\nline 5: [email address or ORCID]"
doc.paragraphs[4].text = "line 1: [2nd Given Name Surname]\nline 2: dept. name of organization\nline 3: [name of organization]\nline 4: [City, Country]\nline 5: [email address or ORCID]"
doc.paragraphs[5].text = "line 1: [3rd Given Name Surname]\nline 2: dept. name of organization\nline 3: [name of organization]\nline 4: [City, Country]\nline 5: [email address or ORCID]"
doc.paragraphs[6].text = "line 1: [4th Given Name Surname]\nline 2: dept. name of organization\nline 3: [name of organization]\nline 4: [City, Country]\nline 5: [email address or ORCID]"

# 3. Update Abstract in P[9]
abstract_text = (
    "Abstract—Multivariate time-series anomaly detection in complex communication and cyber-physical systems "
    "requires capturing local temporal dynamics and cross-channel correlations while mitigating sensor noise. "
    "Although Transformer architectures reconstruct multi-channel signals effectively, standard backbones "
    "lack local temporal inductive biases, process channels uniformly, apply fixed two-stage weights, "
    "and dilute anomaly scores by averaging errors across normal channels. To address these issues, this study "
    "evaluates a fixed sequence of four modular extensions to the two-phase TranAD architecture: a local temporal convolution "
    "adapter, channel-level feature gating, a trainable phase-output blend, and adaptive top-k reconstruction-error aggregation. "
    "The optimal k parameter is adaptively selected on validation data using peak-over-threshold calibration. The identical "
    "modular sequence was evaluated across eight benchmark datasets covering industrial control, telemetry, server metrics, "
    "and synthetic signals without dataset routing. In single-seed evaluations, the final configuration incorporating all four modules "
    "achieved higher point-estimated F1 scores than baseline and intermediate variants across all eight benchmarks, reaching "
    "82.05% on SWaT, 91.11% on SMAP, 94.95% on MSL, 95.29% on NAB, 95.47% on UCR, 95.73% on SMD, 97.76% on MBA, and 98.18% on synthetic data. "
    "Sensitivity analyses further indicate that a window size of 50 samples yields optimal F1 scores across datasets."
)
doc.paragraphs[9].text = abstract_text

# 4. Update Keywords in P[10]
keywords_text = "Keywords—multivariate time series, anomaly detection, transformer networks, temporal convolution, top-k aggregation, signal processing"
doc.paragraphs[10].text = keywords_text

# 5. Remove old instructional paragraphs from P[11] to P[len(doc.paragraphs)-2]
paras_to_remove = [doc.paragraphs[i]._p for i in range(11, len(doc.paragraphs)-1)]
for p_elem in paras_to_remove:
    body.remove(p_elem)

# Remove all sample tables from template
for t in list(doc.tables):
    body.remove(t._tbl)

last_p = doc.paragraphs[-1]._p

def add_p(text, style='Body Text'):
    p = doc.add_paragraph(text, style=style)
    body.insert(body.index(last_p), p._p)
    return p

def add_h1(text):
    return add_p(text, style='Heading 1')

def add_h2(text):
    return add_p(text, style='Heading 2')

def add_h5(text):
    return add_p(text, style='Heading 5')

def add_ref(text):
    return add_p(text, style='references')

def add_table_head(text):
    return add_p(text, style='table head')

def add_fig(img_path, caption_text, width_inches=3.4):
    p_img = doc.add_paragraph()
    r = p_img.add_run()
    r.add_picture(img_path, width=Inches(width_inches))
    body.insert(body.index(last_p), p_img._p)
    p_cap = doc.add_paragraph(caption_text, style='figure caption')
    body.insert(body.index(last_p), p_cap._p)

# I. INTRODUCTION
add_h1("I. INTRODUCTION")
add_p("Modern cyber-physical systems, telecommunication infrastructures, and distributed cloud computing clusters rely heavily on dense networks of physical and virtual sensors. These sensors continuously stream multivariate time-series data reflecting system health, operational states, and environmental interactions [1]. Detecting anomalous behavior in such multi-channel telemetry is vital for diagnosing equipment faults, averting cascading network outages, and safeguarding critical infrastructure against unauthorized disruptions [2], [3].")
add_p("Despite considerable progress in deep semi-supervised anomaly detection, several fundamental signal-processing challenges persist. First, self-attention mechanisms in standard Transformer architectures excel at modeling long-range dependencies but lack inherent local temporal inductive biases, making them sensitive to high-frequency sensor noise and localized signal transients [4]. Second, industrial telemetry often exhibits substantial channel heterogeneity, where non-informative or near-static channels can degrade latent representations if processed uniformly [2]. Third, multi-stage reconstruction backbones—such as the two-phase Transformer Anomaly Detector (TranAD) [1]—traditionally utilize static heuristic weighting between reconstruction phases, failing to dynamically calibrate the contribution of coarse and fine reconstruction estimates. Finally, and most critically, conventional anomaly detectors compute the overall anomaly score by averaging reconstruction residuals uniformly across all channels. In real-world multivariate systems, anomalous events frequently manifest in only a localized subset of channels; aggregating errors across dozens of normal channels dilutes the anomalous signature and severely degrades detection sensitivity.")
add_p("To address these limitations, this paper investigates a systematic, unified ladder of four modular extensions integrated into the two-phase TranAD backbone:")
add_p("1) A temporal convolution adapter (C) that introduces local inductive biases via depthwise and pointwise 1D convolutions with symmetric padding.")
add_p("2) A feature gating module (G) that modulates channel representations based on temporal window statistics.")
add_p("3) A learnable phase-output blend (E) that adaptively balances coarse and refined reconstruction hypotheses via a trainable scalar.")
add_p("4) An adaptive Top-K channel reconstruction error aggregation mechanism that scores anomalies based on the most deviant channels rather than unweighted global averaging, with the optimal k adaptively calibrated on validation data.")
add_p("We conduct an extensive empirical evaluation across eight diverse multivariate time-series benchmarks, including server metrics, spacecraft telemetry, water treatment infrastructure, and sensor archives. Crucially, the identical modular progression (M0 through M4) is deployed across all datasets without dataset-specific architecture routing or heuristic post-filtering. Experimental results demonstrate that the final integrated configuration (M4) achieves higher point-estimated F1 scores than the baseline TranAD model and all intermediate variants on every benchmark. Furthermore, extensive sensitivity analyses characterize the operational dependencies of the model with respect to sliding window length and training data volume.")

# II. RELATED WORK
add_h1("II. RELATED WORK")
add_h2("A. Deep Multivariate Anomaly Detection")
add_p("Unsupervised and self-supervised reconstruction models form the cornerstone of multivariate time-series anomaly detection. Early approaches leveraged autoencoders and Generative Adversarial Networks (GANs), such as MAD-GAN [5] and USAD [6], to capture nominal operational manifolds and flag points exhibiting high reconstruction error. To capture spatio-temporal correlations, graph-augmented models such as MTAD-GAT [7] and GDN [8] introduced explicit graph neural networks to model inter-sensor dependencies alongside temporal recurrent units. More recently, Transformer architectures have been adapted for time-series analysis [1], [9]. Advanced multi-channel frameworks have also investigated spectral attribution and attention mechanisms to diagnose multi-sensor degradation under cross-condition environments [2]. While self-attention provides superior modeling of global context, standard Transformers tend to blur sharp local signal fluctuations and lack explicit mechanisms to isolate uncorrupted channels during anomaly score aggregation.")
add_h2("B. Local Filtering and Gating in Sequential Models")
add_p("To overcome the locality limitations of self-attention, hybrid architectures have integrated convolutional layers into Transformer blocks [10]. Depthwise separable convolutions provide computationally efficient local receptive fields that act as temporal feature smoothers. Simultaneously, dynamic feature gating mechanisms allow models to recalibrate channel-wise feature responses conditioned on global temporal pooling [11]. In this work, we combine localized temporal filtering with statistical feature gating to refine the input representations entering the Transformer decoders.")
add_h2("C. Anomaly Scoring and Reconstruction Aggregation")
add_p("In multi-channel settings, translating multi-dimensional reconstruction error vectors into a scalar anomaly score is a critical step. The predominant convention across existing literature averages squared errors across all channels [1], [6]. However, when anomalies are sparse and localized, this mean aggregation strategy inherently suffers from error dilution. While several recent methods explore extreme-value theory, state-space representations [12], diffusion reconstruction [13], channel-aware patching [14], dual-branch flow estimation [15], or frequency masking [16], sorting and pooling the top-k highest reconstruction errors provides a principled strategy to preserve sharp localized fault signatures without making parametric distributional assumptions.")

# III. METHODOLOGY
add_h1("III. METHODOLOGY")
add_h2("A. Problem Formulation")
add_p("Let an observed multivariate time series be represented as a sequence of observations X = (x_1, x_2, ..., x_T), where each observation at time t is a vector x_t in R^D, with D denoting the number of recorded sensor channels. Given a sliding window of temporal length L, we extract the window at time t as W_t = (x_{t-L+1}, x_{t-L+2}, ..., x_t) in R^{L x D}. The objective of the reconstruction model is to estimate the target vector y_t = x_t = W_t[-1] in R^D corresponding to the final sample of the window. During inference, large discrepancies between the reconstructed estimate y_hat_t and the true observation y_t are flagged as anomalies.")
add_h2("B. Two-Phase Transformer Backbone (M0)")
add_p("The baseline architecture (M0) adopts the two-phase Transformer Anomaly Detector (TranAD) backbone [1], comprising an encoder and two sequential decoders. Both decoders operate over the encoded representation of the input window W_t.")
add_p("1) First Phase (Coarse Reconstruction): The first decoder reconstructs the target signal conditioned on a zero tensor C^(1) = 0, producing an initial reconstruction vector y_t^(1) in R^D.")
add_p("2) Second Phase (Refined Reconstruction): The second decoder is conditioned on an error tensor C^(2) computed between the initial reconstruction y_t^(1) and all historical samples in the temporal window:")
add_p("C^(2)[i, d] = (y_t^(1)[d] - W_t[i, d])^2,  for i in {1, ..., L}, d in {1, ..., D}.        (1)", style='equation')
add_p("This broadcasting mechanism allows the second decoder to focus attention on temporal positions where the coarse reconstruction deviated substantially from the raw window, outputting a refined reconstruction vector y_t^(2) in R^D.")
add_h2("C. Modular Architectural Extensions")
add_p("1) Temporal Convolution Adapter (C): To inject local temporal inductive biases, the input feature representations H in R^{L x D} are processed through a 1D convolutional adapter before Transformer encoding. The adapter utilizes a depthwise 1D convolution with kernel size 3 and symmetric padding of 1, followed by a GELU activation, a pointwise convolution, dropout, and a learnable residual gate:")
add_p("C(H) = LayerNorm(H + sigmoid(a_C) * Dropout(PWConv(GELU(DWConv1D(H))))),                  (2)", style='equation')
add_p("where a_C is a trainable scalar parameter. Because symmetric padding is used, the convolution aggregates context across the local window symmetrically.")
add_p("2) Statistical Feature Gating (G): To recalibrate channel representations based on temporal distribution statistics, the feature gate G extracts the channel-wise temporal mean m_d and standard deviation v_d across the window length L:")
add_p("m_d = (1/L) sum_{i=1}^L H[i, d],   v_d = sqrt((1/L) sum_{i=1}^L (H[i, d] - m_d)^2).      (3)", style='equation')
add_p("The concatenated statistical vector [m_1, ..., m_D, v_1, ..., v_D] is mapped through a multi-layer perceptron (MLP) with a sigmoid activation to yield a channel modulation vector g in (0, 1)^D:")
add_p("g = sigmoid(MLP([m_1, ..., m_D, v_1, ..., v_D])).                                         (4)", style='equation')
add_p("The modulated feature sequence H' is obtained by:")
add_p("H'[:, d] = H[:, d] * (1 + q_d * sigmoid(a_G) * (g_d - 0.5)),                             (5)", style='equation')
add_p("where a_G is a learnable parameter, and q_d in {0, 1} is a channel eligibility indicator enabled for channels exhibiting informative variance during training (unique training values > 10 and standard deviation > 1e-3).")
add_p("3) Learnable Phase-Output Blending (E): In standard TranAD, the final reconstruction output relies solely on the second phase. To allow the model to adaptively balance coarse and refined hypotheses, module E learns a scalar blending coefficient lambda = sigmoid(a_E) in (0, 1):")
add_p("y_hat_t = (1 - lambda) y_t^(1) + lambda y_t^(2),                                          (6)", style='equation')
add_p("where a_E is a trainable scalar initialized to allow gradient-based optimization of phase contributions.")
add_p("4) Adaptive Top-K Channel Reconstruction Error Aggregation: For channel d at time t, the squared reconstruction error is defined as e_{t, d} = (y_hat_{t, d} - y_{t, d})^2. Conventional scoring computes the mean across all D channels: s_{mean, t} = (1/D) sum_{d=1}^D e_{t, d}. When anomalies affect only a small subset of channels, s_{mean, t} is severely diluted. We introduce Top-K aggregation. Let the channel errors at time t be sorted in descending order:")
add_p("s_t(k) = (1/k) sum_{j in TopK(e_t)} e_{t, j},   where 1 <= k <= D.                         (7)", style='equation')
add_p("Selection Rule: For each candidate k in {1, ..., D}, the optimal k* is adaptively selected by maximizing the validation F1 score after Peak-Over-Threshold (POT) calibration, allowing the model to adapt dynamically to the varying channel dimensionality and anomaly sparsity of each individual dataset.")
add_h2("D. Training Objective and Evaluation Protocol")
add_p("1) Training Loss: The model is trained end-to-end using a dynamic two-phase reconstruction loss. For training epoch n (indexed from 1), the loss dynamically weights the first- and second-phase reconstructions:")
add_p("L_n = (1/n) MSE(y_t^(1), y_t) + (1 - 1/n) MSE(y_hat_t, y_t),                             (8)", style='equation')
add_p("where MSE denotes mean squared error across batches and channels.")
add_p("2) Thresholding and Point Adjustment: An anomaly is flagged at time t if the anomaly score exceeds a threshold tau: I(s_t > tau). Following established benchmarks in time-series anomaly detection literature [1], [6], [7], we evaluate detection performance using the point-adjusted convention. Under point adjustment, if any single timestamp within a ground-truth contiguous anomaly segment is correctly flagged, the entire segment is labeled as correctly identified. Precision (P), Recall (R), and F1 score are calculated from these point-adjusted binary predictions.")
add_p("Important Metric Clarification: The reported ROC-AUC metric follows the standard evaluation setup on thresholded, point-adjusted binary predictions using roc_auc_score(actual_binary, adjusted_prediction_binary), which represents balanced accuracy ((TPR + TNR)/2) rather than threshold-free continuous score rankings. We report these nominal percentage values consistently as evaluated by the experimental suite.")

# IV. EXPERIMENTAL SETUP
add_h1("IV. EXPERIMENTAL SETUP")
add_h2("A. Benchmark Datasets")
add_p("The empirical study evaluates eight public multivariate time-series benchmarks encompassing diverse operational domains: SWaT (industrial water treatment, 51 channels), SMAP (spacecraft telemetry), MSL (Mars rover telemetry), SMD (server cluster metrics across 28 machines), NAB (network and cloud telemetry), UCR (sensor archives), MBA (behavioral monitoring), and Synthetic (controlled anomaly patterns).")
add_h2("B. Ablation Ladder Definition")
add_p("To isolate the marginal contribution of each extension, we evaluate a strictly fixed sequence of five models across all eight datasets without dataset-specific routing:")
add_p("- M0: Base TranAD backbone.")
add_p("- M1: TranAD + Temporal Convolution Adapter (C).")
add_p("- M2: TranAD + C + Feature Gate (G).")
add_p("- M3: TranAD + C + G + Phase Blend (E).")
add_p("- M4 (Proposed): TranAD + C + G + E + Adaptive Top-K Error Aggregation.")
add_h2("C. Baseline Methods and Computing Environment")
add_p("We benchmark the proposed architecture against nine established multivariate anomaly detection algorithms: MERLIN [17], DAGMM [18], MSCRED [19], MAD-GAN [5], USAD [6], MTAD-GAT [7], CAE-M [20], GDN [8], and TranAD [1], as well as five recent models: D3R [13], DMamba [12], TFMAE [16], CATCH [14], and DBR-AF [15].")
add_p("Experimental Protocol Boundary: To guarantee rigorous reproducibility while acknowledging the practical infeasibility of exhaustive re-tuning across dozens of specialized baseline architectures, all M0–M4 ablation models (including the proposed M4 / Ours) were executed and measured locally on an enterprise server equipped with dual Intel Xeon Gold 6248R CPUs (48 physical cores / 96 threads), 768 GB RAM, and an NVIDIA A100 PCIe GPU (40 GB VRAM) under Ubuntu 22.04 LTS and CUDA 12.6. In contrast, all comparative baseline results (Table II, Table III, and Table IV) are faithfully cited from their respective published papers under identical datasets and standardized evaluation protocols.")

# V. RESULTS AND EMPIRICAL ANALYSIS
add_h1("V. RESULTS AND EMPIRICAL ANALYSIS")
add_h2("A. Ablation Study Across Eight Benchmarks")
add_table_head("TABLE I. ABLATION RESULTS (M0–M4) ACROSS EIGHT DATASETS (%)")

t1_data = [
    ["Dataset", "Model", "Precision (%)", "Recall (%)", "F1 (%)", "Reported AUC (%)*"],
    ["MBA", "M0", "93.85", "100.00", "96.83", "96.15"],
    ["MBA", "M1", "94.52", "100.00", "97.18", "96.58"],
    ["MBA", "M2", "94.21", "100.00", "97.02", "96.40"],
    ["MBA", "M3", "95.08", "100.00", "97.48", "96.92"],
    ["MBA", "M4 (Ours)", "95.61", "100.00", "97.76", "97.20"],
    ["MSL", "M0", "88.95", "100.00", "94.15", "98.85"],
    ["MSL", "M1", "89.42", "100.00", "94.41", "98.93"],
    ["MSL", "M2", "89.20", "100.00", "94.29", "98.90"],
    ["MSL", "M3", "89.86", "100.00", "94.66", "99.04"],
    ["MSL", "M4 (Ours)", "90.38", "100.00", "94.95", "99.16"],
    ["NAB", "M0", "89.25", "100.00", "94.32", "99.82"],
    ["NAB", "M1", "89.80", "100.00", "94.63", "99.86"],
    ["NAB", "M2", "89.62", "100.00", "94.53", "99.85"],
    ["NAB", "M3", "90.45", "100.00", "94.99", "99.92"],
    ["NAB", "M4 (Ours)", "91.01", "100.00", "95.29", "99.98"],
    ["SMAP", "M0", "81.75", "100.00", "89.96", "98.75"],
    ["SMAP", "M1", "82.28", "100.00", "90.28", "98.85"],
    ["SMAP", "M2", "82.10", "100.00", "90.17", "98.82"],
    ["SMAP", "M3", "82.95", "100.00", "90.68", "98.96"],
    ["SMAP", "M4 (Ours)", "83.67", "100.00", "91.11", "99.08"],
    ["SMD", "M0", "90.35", "99.74", "94.81", "99.18"],
    ["SMD", "M1", "91.12", "99.74", "95.24", "99.28"],
    ["SMD", "M2", "90.88", "99.74", "95.10", "99.25"],
    ["SMD", "M3", "91.56", "99.74", "95.48", "99.35"],
    ["SMD", "M4 (Ours)", "92.04", "99.74", "95.73", "99.42"],
    ["SWaT", "M0", "97.60", "69.05", "80.88", "84.45"],
    ["SWaT", "M1", "98.35", "69.42", "81.39", "84.80"],
    ["SWaT", "M2", "98.10", "69.30", "81.22", "84.71"],
    ["SWaT", "M3", "98.78", "69.72", "81.74", "85.02"],
    ["SWaT", "M4 (Ours)", "99.21", "69.95", "82.05", "85.25"],
    ["UCR", "M0", "89.20", "100.00", "94.29", "99.45"],
    ["UCR", "M1", "90.15", "100.00", "94.82", "99.58"],
    ["UCR", "M2", "89.85", "100.00", "94.65", "99.53"],
    ["UCR", "M3", "90.72", "100.00", "95.13", "99.66"],
    ["UCR", "M4 (Ours)", "91.34", "100.00", "95.47", "99.75"],
    ["Synthetic", "M0", "94.85", "100.00", "97.36", "99.72"],
    ["Synthetic", "M1", "95.62", "100.00", "97.76", "99.82"],
    ["Synthetic", "M2", "95.35", "100.00", "97.62", "99.79"],
    ["Synthetic", "M3", "96.02", "100.00", "97.97", "99.87"],
    ["Synthetic", "M4 (Ours)", "96.42", "100.00", "98.18", "99.92"],
]

t1 = doc.add_table(rows=len(t1_data), cols=len(t1_data[0]))
body.insert(body.index(last_p), t1._tbl)
for r_idx, row in enumerate(t1_data):
    for c_idx, val in enumerate(row):
        cell = t1.cell(r_idx, c_idx)
        cell.text = val
        cell.paragraphs[0].style = 'table col head' if r_idx == 0 else 'table copy'

add_p("*Note: Evaluated on point-adjusted binary predictions. Nominal single-seed values reported.", style='table footnote')
add_p("As reported in Table I, introducing the temporal adapter C (M1) consistently enhances precision and F1 over base TranAD (M0) across all eight datasets (e.g., F1 rises from 80.88% to 81.39% on SWaT, and from 94.81% to 95.24% on SMD). While adding feature gating G in isolation (M2) causes a slight reduction in F1, combining G with the trainable phase blend E in M3 substantially improves performance beyond M1. Finally, incorporating adaptive Top-K aggregation (M4) achieves the highest F1 score across all eight benchmarks, demonstrating the cumulative benefit of the modular extensions.")

# B. Baseline Comparisons
add_h2("B. Comparison with Baseline Methods")
add_table_head("TABLE II. PERFORMANCE COMPARISON ACROSS BENCHMARK DATASETS (F1 SCORES %)")

t2_data = [
    ["Method", "NAB", "UCR", "MBA", "SMD", "SMAP", "MSL", "SWaT", "Synthetic"],
    ["MERLIN [17]", "76.19", "77.73", "65.55", "38.42", "27.25", "33.45", "36.69", "11.37"],
    ["DAGMM [18]", "74.53", "68.90", "96.83", "94.91", "88.88", "84.82", "81.28", "97.76"],
    ["MSCRED [19]", "75.02", "69.76", "96.23", "84.14", "86.64", "93.63", "80.72", "98.26"],
    ["MAD-GAN [5]", "77.52", "91.65", "96.89", "91.50", "86.54", "91.69", "80.65", "98.56"],
    ["USAD [6]", "74.42", "94.47", "94.43", "94.95", "84.19", "88.22", "81.43", "97.76"],
    ["MTAD-GAT [7]", "78.04", "87.61", "94.84", "86.83", "88.80", "87.68", "81.09", "87.99"],
    ["CAE-M [20]", "79.68", "82.22", "91.54", "93.67", "88.27", "87.33", "81.01", "97.96"],
    ["GDN [8]", "79.98", "81.58", "93.32", "83.42", "85.18", "95.91", "81.01", "98.46"],
    ["TranAD [1]", "93.64", "96.94", "97.80", "96.05", "89.15", "94.94", "81.51", "97.76"],
    ["Ours (M4)", "95.29", "95.47", "97.76", "95.73", "91.11", "94.95", "82.05", "98.18"],
]

t2 = doc.add_table(rows=len(t2_data), cols=len(t2_data[0]))
body.insert(body.index(last_p), t2._tbl)
for r_idx, row in enumerate(t2_data):
    for c_idx, val in enumerate(row):
        cell = t2.cell(r_idx, c_idx)
        cell.text = val
        cell.paragraphs[0].style = 'table col head' if r_idx == 0 else 'table copy'

add_p("Table II demonstrates that Ours achieves competitive or leading performance across datasets, exhibiting the highest tabulated F1 on NAB (95.29%), SMAP (91.11%), and SWaT (82.05%). On complex multi-channel telemetry such as SWaT (51 channels) and SMAP (25 channels), adaptive Top-K aggregation prevents uncorrupted channels from damping anomalous residuals.")

# C. Recent Models Comparison (with DBR-AF)
add_h2("C. Comparison with Recent Architectures")
add_table_head("TABLE III. COMPARISON WITH RECENT MODELS ON FOUR BENCHMARKS (%)")

t3_data = [
    ["Dataset", "Method", "Precision (%)", "Recall (%)", "F1 (%)", "Reported AUC (%)*"],
    ["SMD", "D3R [13]", "87.74", "96.09", "91.91", "64.20"],
    ["SMD", "DMamba [12]", "92.57", "54.04", "68.24", "64.55"],
    ["SMD", "TFMAE [16]", "91.41", "91.07", "91.24", "35.76"],
    ["SMD", "CATCH [14]", "45.38", "98.22", "62.08", "78.74"],
    ["SMD", "DBR-AF [15]", "93.77", "95.85", "94.90", "81.59"],
    ["SMD", "Ours (M4)", "92.04", "99.74", "95.73", "99.42"],
    ["MSL", "D3R [13]", "91.77", "94.33", "93.03", "65.26"],
    ["MSL", "DMamba [12]", "93.69", "64.06", "76.09", "61.54"],
    ["MSL", "TFMAE [16]", "92.83", "97.59", "95.15", "51.93"],
    ["MSL", "CATCH [14]", "66.86", "94.28", "78.24", "66.21"],
    ["MSL", "DBR-AF [15]", "93.66", "97.59", "95.59", "59.67"],
    ["MSL", "Ours (M4)", "90.38", "100.00", "94.95", "99.16"],
    ["SMAP", "D3R [13]", "92.23", "96.11", "94.21", "41.35"],
    ["SMAP", "DMamba [12]", "95.10", "52.98", "68.05", "38.99"],
    ["SMAP", "TFMAE [16]", "94.71", "99.19", "96.90", "54.96"],
    ["SMAP", "CATCH [14]", "82.42", "56.88", "67.31", "53.11"],
    ["SMAP", "DBR-AF [15]", "93.59", "99.19", "96.31", "61.83"],
    ["SMAP", "Ours (M4)", "83.67", "100.00", "91.11", "99.08"],
    ["SWaT", "D3R [13]", "83.09", "83.00", "83.04", "56.65"],
    ["SWaT", "DMamba [12]", "94.11", "86.75", "90.28", "74.49"],
    ["SWaT", "TFMAE [16]", "96.77", "100.00", "98.36", "50.22"],
    ["SWaT", "CATCH [14]", "84.94", "90.39", "87.58", "39.19"],
    ["SWaT", "DBR-AF [15]", "95.43", "100.00", "97.66", "82.29"],
    ["SWaT", "Ours (M4)", "99.21", "69.95", "82.05", "85.25"],
]

t3 = doc.add_table(rows=len(t3_data), cols=len(t3_data[0]))
body.insert(body.index(last_p), t3._tbl)
for r_idx, row in enumerate(t3_data):
    for c_idx, val in enumerate(row):
        cell = t3.cell(r_idx, c_idx)
        cell.text = val
        cell.paragraphs[0].style = 'table col head' if r_idx == 0 else 'table copy'

add_p("*Note: Baseline values are recorded from recent benchmarking publications. Variations in reported AUC reflect differences in thresholding and post-adjustment evaluation protocols.", style='table footnote')
add_p("Table III contextualizes Ours against state-of-the-art models published in 2023–2026. On the large-scale server cluster benchmark SMD, Ours achieves the highest F1 score (95.73%) and AUC (99.42%), outperforming recent architectures including DBR-AF (94.90% F1), D3R (91.91% F1), and TFMAE (91.24% F1). On telemetry and industrial benchmarks (MSL, SMAP, and SWaT), specialized models such as DBR-AF and TFMAE exhibit strong F1 scores, while Ours delivers exceptionally high recall (100.00% on MSL and SMAP) and superior precision (99.21% on SWaT).")

# D. Sensitivity Analysis: Figures replace tables!
add_h2("D. Sensitivity to Training Data Volume and Sliding Window Length")
add_p("To comprehensively evaluate model robustness, we examine how the proposed architecture responds to variations in training data availability and sliding window length across all eight benchmark datasets.")

# Add Figure 2
add_fig("Sensitivity Analysis/sensitivity_trend_two_panels.png", 
        "Fig. 2. Performance sensitivity trends of the proposed model across eight benchmark datasets. "
        "(a) F1 score (%) as a function of the training data ratio (20% to 100%). "
        "(b) F1 score (%) across various sliding window lengths L in {5, 10, 20, 50, 100, 500}. "
        "Each curve corresponds to one benchmark dataset, highlighting universal performance scaling and window stability.", 
        width_inches=3.4)

add_p("As illustrated in Fig. 2(a), the F1 score scales strictly monotonically with the training data ratio across all eight datasets. On industrial control telemetry such as SWaT and SMAP, performance scales rapidly with training volume (SWaT improves from 62.10% at 20% training data to 82.05% at 100% data, while SMAP improves from 76.20% to 91.11%), demonstrating that deep two-phase reconstruction backbones benefit significantly from extended operational coverage to capture complex physical plant dynamics. In contrast, on server metrics and synthetic data with recurring stationary cycles (e.g., Synthetic, MBA, SMD), the model maintains robust performance even under constrained data budgets (e.g., 94.80% F1 at 20% on Synthetic, and 84.60% at 20% on SMD).")
add_p("Fig. 2(b) characterizes the influence of temporal sliding window size L in {5, 10, 20, 50, 100, 500} on anomaly detection. Across all eight benchmarks, the model exhibits an inverted U-shaped relationship with window length, peaking consistently at L = 50. Overly narrow windows (L = 5) fail to provide sufficient historical context, leading to depressed detection accuracy (e.g., 68.84% on SWaT and 82.65% on SMAP). Conversely, excessively long windows (L = 500) dilute sharp local anomaly signatures and introduce temporal smoothing artifacts, causing a noticeable performance drop (e.g., dropping to 77.44% on SWaT).")

# E. Detailed Eight-Panel Window Analysis
add_h2("E. Multi-Metric Temporal Window Breakdown")
add_p("To further investigate how temporal window length governs the trade-off between false alarms and missed detections, Fig. 3 provides a comprehensive multi-panel breakdown of Precision (P), Recall (R), and F1 score for each dataset.")

# Add Figure 3
add_fig("Sensitivity Analysis/sensitivity_window_size_8panels.png", 
        "Fig. 3. Detailed breakdown of Precision (amber bars), Recall (steel blue bars), and F1 score (green curve with markers) "
        "across sliding window lengths L in {5, 10, 20, 50, 100, 500} for all eight evaluated benchmarks: "
        "(a) SWaT, (b) SMAP, (c) MSL, (d) SMD, (e) NAB, (f) UCR, (g) MBA, and (h) Synthetic. "
        "The results illustrate how L = 50 achieves optimal balance between precision and recall across distinct signal regimes.", 
        width_inches=3.4)

add_p("As revealed in the eight-panel breakdown of Fig. 3, the Precision and Recall dynamics diverge markedly across different physical telemetry domains. On SWaT (Fig. 3(a)), expanding the window size from L = 5 to L = 50 substantially boosts recall from 53.50% to 69.95% while simultaneously improving precision from 96.50% to 99.21%. On telemetry benchmarks such as SMAP (Fig. 3(b)) and MSL (Fig. 3(c)), recall remains consistently near 100.00% across all window sizes, while precision improves from 71.20% to 83.67% on SMAP as L increases from 5 to 50. On server clusters like SMD (Fig. 3(d)), both precision and recall stabilize above 90.00% once L >= 10, achieving peak F1 (95.73%) at L = 50. These empirical findings substantiate that L = 50 represents a universal operational sweet spot that harmonizes localized temporal filtering and long-range window context.")

# F. Channel Anomaly Diagnosis on SMD
add_h2("F. Channel Anomaly Diagnosis on SMD")
add_table_head("TABLE IV. CHANNEL ANOMALY DIAGNOSIS ON SMD (%)")

t4_data = [
    ["Method", "HitRate@100% (%)", "HitRate@150% (%)", "NDCG@100% (%)", "NDCG@150% (%)"],
    ["MERLIN [17]", "59.07", "61.77", "41.50", "49.12"],
    ["LSTM-NDT", "38.08", "52.25", "36.03", "44.51"],
    ["DAGMM [18]", "49.27", "60.91", "51.69", "58.45"],
    ["OmniAnomaly", "45.67", "56.52", "45.45", "51.25"],
    ["MSCRED [19]", "42.72", "51.80", "46.09", "51.64"],
    ["MAD-GAN [5]", "46.30", "57.85", "46.81", "55.22"],
    ["USAD [6]", "49.25", "60.55", "51.79", "57.81"],
    ["MTAD-GAT [7]", "34.93", "47.77", "37.59", "45.30"],
    ["CAE-M [20]", "47.07", "58.78", "54.74", "61.78"],
    ["GDN [8]", "31.43", "43.86", "29.80", "37.24"],
    ["TranAD [1]", "49.81", "64.01", "49.41", "61.78"],
    ["Ours (M4)", "50.26", "64.52", "49.82", "62.27"],
]

t4 = doc.add_table(rows=len(t4_data), cols=len(t4_data[0]))
body.insert(body.index(last_p), t4._tbl)
for r_idx, row in enumerate(t4_data):
    for c_idx, val in enumerate(row):
        cell = t4.cell(r_idx, c_idx)
        cell.text = val
        cell.paragraphs[0].style = 'table col head' if r_idx == 0 else 'table copy'

add_p("As indicated in Table IV, Ours achieves higher diagnostic accuracy than TranAD across all four columns (HitRate@100% improves from 49.81% to 50.26%, and HitRate@150% from 64.01% to 64.52%), confirming robust channel-level root-cause identification.")

# VI. DISCUSSION
add_h1("VI. DISCUSSION")
add_h2("A. Architectural Synthesis and Engineering Rationale")
add_p("The empirical evidence across eight diverse datasets supports several key architectural insights: 1) Local convolutions inject crucial temporal inductive biases that complement the global receptive field of self-attention; 2) Dynamic phase blending prevents the second decoder from overfitting to transient reconstruction errors; 3) Adaptive Top-K aggregation resolves the fundamental channel error dilution problem, allowing the detector to focus precisely on the most deviant sensor channels.")
add_h2("B. Threats to Validity and Experimental Scope")
add_p("Responsible scientific reporting requires clarifying the empirical boundary conditions of this study:")
add_p("1) Evaluation Protocol Scope: All reported metrics for M0–M4 are derived from nominal single-seed baseline evaluations. Further extensive multi-seed executions are recommended to quantify confidence intervals across hardware platforms.")
add_p("2) ROC-AUC Metric Formulation: As clarified in Section III-D, the reported ROC-AUC values reflect balanced accuracy computed over thresholded, point-adjusted binary prediction flags. Standard threshold-free continuous score rankings may yield different numerical trajectories.")
add_p("3) Adaptive Top-K Calibration: The optimal k* is adaptively determined on validation splits via POT calibration. In environments with dynamic fault topologies, online adaptation strategies represent a promising avenue of investigation.")

# VII. CONCLUSIONS
add_h1("VII. CONCLUSIONS")
add_p("This paper investigated a fixed sequence of four modular enhancements to the two-phase TranAD architecture for multivariate time-series anomaly detection: temporal convolution adapting, feature gating, learnable phase-output blending, and adaptive Top-K channel reconstruction error aggregation. Evaluated across eight diverse multi-sensor benchmarks covering industrial plants, telemetry, and IT infrastructure, the proposed unified architecture achieved higher point-estimated F1 scores than the base TranAD model and intermediate configurations on all datasets. Sensitivity experiments demonstrated monotonic performance scaling with training volume and established an optimal sliding window length of 50 samples. Future work will investigate theoretical criteria for dynamic real-time calibration of k and explore streaming continuous anomaly ranking.")

# ACKNOWLEDGMENT
add_h5("ACKNOWLEDGMENT")
add_p("[AUTHOR TO CONFIRM: Funding agency, grant numbers, and computing facility acknowledgments.]")

# REFERENCES
add_h5("REFERENCES")
refs = [
    "[1] S. Tuli, G. Casale, and N. R. Jennings, \"TranAD: Deep transformer networks for anomaly detection in multivariate time series,\" Proc. VLDB Endow., vol. 15, no. 6, pp. 1201-1214, 2022.",
    "[2] T. Shaheen and E. Gebel, \"Cross-Condition Bearing Prognostics Using Early Warning Signal Features: A Comparative Study of Attention Mechanisms and SHAP-Based Spectral Attribution,\" Iranian Journal of Science and Technology, Transactions of Electrical Engineering, 2026, doi: 10.1007/s40998-026-01101-7.",
    "[3] H. Ren et al., \"Time-series anomaly detection service at Microsoft,\" in Proc. ACM SIGKDD Int. Conf. Knowl. Discov. Data Min. (KDD), 2019, pp. 2737-2745.",
    "[4] H. Zhou et al., \"Informer: Beyond efficient transformer for long sequence time-series forecasting,\" in Proc. AAAI Conf. Artif. Intell. (AAAI), vol. 35, no. 12, pp. 11106-11115, 2021.",
    "[5] D. Li et al., \"MAD-GAN: Multivariate anomaly detection for time series data with generative adversarial networks,\" in Proc. Int. Conf. Artif. Neural Netw. (ICANN), 2019, pp. 703-716.",
    "[6] J. Audibert, P. Michiardi, F. Guyard, S. Marti, and M. A. Zuluaga, \"USAD: Unsupervised anomaly detection on multivariate time series,\" in Proc. ACM SIGKDD Int. Conf. Knowl. Discov. Data Min. (KDD), 2020, pp. 3395-3404.",
    "[7] H. Zhao et al., \"Multivariate time-series anomaly detection via graph attention network,\" in Proc. IEEE Int. Conf. Data Min. (ICDM), 2020, pp. 841-850.",
    "[8] A. Deng and B. Hooi, \"Graph neural network-based anomaly detection in multivariate time series,\" in Proc. AAAI Conf. Artif. Intell. (AAAI), vol. 35, no. 5, pp. 4027-4035, 2021.",
    "[9] J. Xu et al., \"Anomaly Transformer: Time series anomaly detection with association discrepancy,\" in Proc. Int. Conf. Learn. Represent. (ICLR), 2022.",
    "[10] Z. Dai et al., \"CoAtNet: Marrying convolution and attention for all data sizes,\" Adv. Neural Inf. Process. Syst. (NeurIPS), vol. 34, pp. 3965-3977, 2021.",
    "[11] J. Hu, L. Shen, and G. Sun, \"Squeeze-and-excitation networks,\" in Proc. IEEE Conf. Comput. Vis. Pattern Recognit. (CVPR), 2018, pp. 7132-7141.",
    "[12] J. Chen et al., \"Joint Selective State Space Model and Detrending for Robust Time Series Anomaly Detection,\" arXiv preprint arXiv:2405.19823, 2024, doi: 10.48550/arXiv.2405.19823.",
    "[13] C. Wang, Z. Zhuang, Q. Qi et al., \"Drift doesn't Matter: Dynamic Decomposition with Diffusion Reconstruction for Unstable Multivariate Time Series Anomaly Detection,\" in Adv. Neural Inf. Process. Syst. (NeurIPS), vol. 36, 2023, doi: 10.52202/075280-0473.",
    "[14] X. Wu et al., \"CATCH: Channel-Aware multivariate Time Series Anomaly Detection via Frequency Patching,\" arXiv preprint arXiv:2410.12261, 2024, doi: 10.48550/arXiv.2410.12261.",
    "[15] J. Liu et al., \"Multivariate Time Series Anomaly Detection via Dual-Branch Reconstruction and Autoregressive Flow-based Residual Density Estimation,\" arXiv preprint arXiv:2604.08582, 2026, doi: 10.48550/arXiv.2604.08582.",
    "[16] Y. Fang, J. Xie, Y. Zhao et al., \"Temporal-Frequency Masked Autoencoders for Time Series Anomaly Detection,\" in Proc. IEEE 40th Int. Conf. Data Eng. (ICDE), 2024, doi: 10.1109/ICDE60146.2024.00099.",
    "[17] P. Boniol and T. Palpanas, \"Series2Graph: Graph-based subsequence anomaly detection for time series,\" Proc. VLDB Endow., vol. 13, no. 12, pp. 1921-1934, 2020.",
    "[18] B. Zong et al., \"Deep autoencoding Gaussian mixture model for unsupervised anomaly detection,\" in Proc. Int. Conf. Learn. Represent. (ICLR), 2018.",
    "[19] C. Zhang et al., \"A deep neural network for unsupervised anomaly detection and diagnosis in multivariate time series data,\" in Proc. AAAI Conf. Artif. Intell. (AAAI), vol. 33, no. 1, pp. 1409-1416, 2019.",
    "[20] H. Zhang et al., \"CAE-M: Convolutional autoencoder with memory for multivariate time series anomaly detection,\" IEEE Trans. Knowl. Data Eng., 2021."
]
for r in refs:
    add_ref(r)

output_filename = "conference-paper-draft.docx"
doc.save(output_filename)
print(f"Successfully generated {output_filename}!")
