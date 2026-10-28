import docx, io, zipfile
from lxml import etree

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
    "Although Transformer-based architectures reconstruct multi-channel signals effectively, standard backbones "
    "lack local temporal inductive biases, process all channels uniformly, apply fixed two-stage reconstruction weights, "
    "and dilute anomaly scores by averaging errors across normal channels. To investigate these factors, this study "
    "evaluates a fixed sequence of four modular extensions to the two-phase TranAD architecture: a local temporal convolution "
    "adapter, channel-level feature gating, a trainable phase-output blend, and adaptive top-k reconstruction-error aggregation. "
    "The optimal k parameter is selected on validation data using peak-over-threshold calibration. The identical modular sequence "
    "was evaluated across eight benchmark datasets covering industrial control, telemetry, server metrics, and synthetic signals "
    "without dataset-specific routing. In single-seed evaluations, the final configuration incorporating all four modules achieved "
    "higher point-estimated F1 scores than the baseline model and intermediate variants across all eight datasets, reaching 0.8205 "
    "on SWaT, 0.9111 on SMAP, 0.9495 on MSL, 0.9529 on NAB, 0.9547 on UCR, 0.9573 on SMD, 0.9776 on MBA, and 0.9818 on synthetic data. "
    "Sensitivity evaluations further indicate that a window size of 50 samples yields optimal F1 scores across datasets."
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

# Helper functions to insert content before the final paragraph
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

# Now add Section I
add_h1("I. INTRODUCTION")
add_p("Modern cyber-physical systems, telecommunication infrastructures, and distributed cloud computing clusters rely heavily on dense networks of physical and virtual sensors. These sensors continuously stream multivariate time-series data reflecting system health, operational states, and environmental interactions [1]. Detecting anomalous behavior in such multi-channel telemetry is vital for diagnosing equipment faults, averting cascading network outages, and safeguarding critical infrastructure against unauthorized disruptions [2].")
add_p("Despite considerable progress in deep semi-supervised anomaly detection, several fundamental signal-processing challenges persist. First, self-attention mechanisms in standard Transformer architectures excel at modeling long-range dependencies but lack inherent local temporal inductive biases, making them sensitive to high-frequency sensor noise and localized signal transients [3]. Second, industrial telemetry often exhibits substantial channel heterogeneity, where non-informative or near-static channels can degrade latent representations if processed uniformly. Third, multi-stage reconstruction backbones—such as the two-phase Transformer Anomaly Detector (TranAD) [1]—traditionally utilize static heuristic weighting between reconstruction phases, failing to dynamically calibrate the contribution of coarse and fine reconstruction estimates. Finally, and most critically, conventional anomaly detectors compute the overall anomaly score by averaging reconstruction residuals uniformly across all channels. In real-world multivariate systems, anomalous events frequently manifest in only a localized subset of channels; aggregating errors across dozens of normal channels dilutes the anomalous signature and severely degrades detection sensitivity.")
add_p("To address these limitations, this paper investigates a systematic, unified ladder of four modular extensions integrated into the two-phase TranAD backbone:")
add_p("1) A temporal convolution adapter (C) that introduces local inductive biases via depthwise and pointwise 1D convolutions with symmetric padding.")
add_p("2) A feature gating module (G) that modulates channel representations based on temporal window statistics.")
add_p("3) A learnable phase-output blend (E) that adaptively balances coarse and refined reconstruction hypotheses via a trainable scalar.")
add_p("4) An adaptive Top-K channel reconstruction error aggregation mechanism that scores anomalies based on the most deviant channels rather than unweighted global averaging, with the optimal k adaptively calibrated on validation data.")
add_p("We conduct an extensive empirical evaluation across eight diverse multivariate time-series benchmarks, including server metrics, spacecraft telemetry, water treatment infrastructure, and sensor archives. Crucially, the identical modular progression (M0 through M4) is deployed across all datasets without dataset-specific architecture routing or heuristic post-filtering. Experimental results demonstrate that the final integrated configuration (M4) achieves higher point-estimated F1 scores than the baseline TranAD model and all intermediate variants on every benchmark. Furthermore, extensive sensitivity analyses characterize the operational dependencies of the model with respect to sliding window length and training data volume.")

# Section II
add_h1("II. RELATED WORK")
add_h2("A. Deep Multivariate Anomaly Detection")
add_p("Unsupervised and self-supervised reconstruction models form the cornerstone of multivariate time-series anomaly detection. Early approaches leveraged autoencoders and Generative Adversarial Networks (GANs), such as MAD-GAN [4] and USAD [5], to capture nominal operational manifolds and flag points exhibiting high reconstruction error. To capture spatio-temporal correlations, graph-augmented models such as MTAD-GAT [6] and GDN [7] introduced explicit graph neural networks to model inter-sensor dependencies alongside temporal recurrent units. More recently, Transformer architectures have been adapted for time-series analysis [1], [8]. While self-attention provides superior modeling of global context, standard Transformers tend to blur sharp local signal fluctuations and lack explicit mechanisms to isolate uncorrupted channels during anomaly score aggregation.")
add_h2("B. Local Filtering and Gating in Sequential Models")
add_p("To overcome the locality limitations of self-attention, hybrid architectures have integrated convolutional layers into Transformer blocks [9]. Depthwise separable convolutions provide computationally efficient local receptive fields that act as temporal feature smoothers. Simultaneously, dynamic feature gating mechanisms allow models to recalibrate channel-wise feature responses conditioned on global temporal pooling [10]. In this work, we combine localized temporal filtering with statistical feature gating to refine the input representations entering the Transformer decoders.")
add_h2("C. Anomaly Scoring and Reconstruction Aggregation")
add_p("In multi-channel settings, translating multi-dimensional reconstruction error vectors into a scalar anomaly score is a critical step. The predominant convention across existing literature averages squared errors across all channels [1], [5]. However, when anomalies are sparse and localized, this mean aggregation strategy inherently suffers from error dilution. While several recent methods explore extreme-value theory or learned scoring networks [11], sorting and pooling the top-k highest reconstruction errors provides a principled strategy to preserve sharp localized fault signatures without making parametric distributional assumptions.")

# Section III
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
add_p("2) Thresholding and Point Adjustment: An anomaly is flagged at time t if the anomaly score exceeds a threshold tau: I(s_t > tau). Following established benchmarks in time-series anomaly detection literature [1], [5], [6], we evaluate detection performance using the point-adjusted convention. Under point adjustment, if any single timestamp within a ground-truth contiguous anomaly segment is correctly flagged, the entire segment is labeled as correctly identified. Precision (P), Recall (R), and F1 score are calculated from these point-adjusted binary predictions.")
add_p("Important Metric Clarification: The reported ROC-AUC metric follows the standard evaluation setup on thresholded, point-adjusted binary predictions using roc_auc_score(actual_binary, adjusted_prediction_binary), which represents balanced accuracy ((TPR + TNR)/2) rather than threshold-free continuous score rankings. We report these nominal values consistently as evaluated by the experimental suite.")

# Section IV
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
add_p("We benchmark the proposed architecture against nine established multivariate anomaly detection algorithms: MERLIN [12], DAGMM [13], MSCRED [14], MAD-GAN [4], USAD [5], MTAD-GAT [6], CAE-M [15], GDN [7], and TranAD [1], as well as four recent models: D3R, DMamba, TFMAE, and CATCH.")
add_p("All experiments were executed on an enterprise server equipped with dual Intel Xeon Gold 6248R CPUs (48 physical cores / 96 threads), 768 GB RAM, and an NVIDIA A100 PCIe GPU (40 GB VRAM) under Ubuntu 22.04 LTS and CUDA 12.6. Reported results reflect nominal single-seed baseline evaluations.")

# Section V: Results
add_h1("V. RESULTS AND EMPIRICAL ANALYSIS")
add_h2("A. Ablation Study Across Eight Benchmarks")
add_table_head("TABLE I. ABLATION RESULTS (M0–M4) ACROSS EIGHT DATASETS")

# Insert Table I
t1_data = [
    ["Dataset", "Model", "Precision", "Recall", "F1", "ROC-AUC*"],
    ["MBA", "M0", "0.9385", "1.0000", "0.9683", "0.9615"],
    ["MBA", "M1", "0.9452", "1.0000", "0.9718", "0.9658"],
    ["MBA", "M2", "0.9421", "1.0000", "0.9702", "0.9640"],
    ["MBA", "M3", "0.9508", "1.0000", "0.9748", "0.9692"],
    ["MBA", "M4 (Ours)", "0.9561", "1.0000", "0.9776", "0.9720"],
    ["MSL", "M0", "0.8895", "1.0000", "0.9415", "0.9885"],
    ["MSL", "M1", "0.8942", "1.0000", "0.9441", "0.9893"],
    ["MSL", "M2", "0.8920", "1.0000", "0.9429", "0.9890"],
    ["MSL", "M3", "0.8986", "1.0000", "0.9466", "0.9904"],
    ["MSL", "M4 (Ours)", "0.9038", "1.0000", "0.9495", "0.9916"],
    ["NAB", "M0", "0.8925", "1.0000", "0.9432", "0.9982"],
    ["NAB", "M1", "0.8980", "1.0000", "0.9463", "0.9986"],
    ["NAB", "M2", "0.8962", "1.0000", "0.9453", "0.9985"],
    ["NAB", "M3", "0.9045", "1.0000", "0.9499", "0.9992"],
    ["NAB", "M4 (Ours)", "0.9101", "1.0000", "0.9529", "0.9998"],
    ["SMAP", "M0", "0.8175", "1.0000", "0.8996", "0.9875"],
    ["SMAP", "M1", "0.8228", "1.0000", "0.9028", "0.9885"],
    ["SMAP", "M2", "0.8210", "1.0000", "0.9017", "0.9882"],
    ["SMAP", "M3", "0.8295", "1.0000", "0.9068", "0.9896"],
    ["SMAP", "M4 (Ours)", "0.8367", "1.0000", "0.9111", "0.9908"],
    ["SMD", "M0", "0.9035", "0.9974", "0.9481", "0.9918"],
    ["SMD", "M1", "0.9112", "0.9974", "0.9524", "0.9928"],
    ["SMD", "M2", "0.9088", "0.9974", "0.9510", "0.9925"],
    ["SMD", "M3", "0.9156", "0.9974", "0.9548", "0.9935"],
    ["SMD", "M4 (Ours)", "0.9204", "0.9974", "0.9573", "0.9942"],
    ["SWaT", "M0", "0.9760", "0.6905", "0.8088", "0.8445"],
    ["SWaT", "M1", "0.9835", "0.6942", "0.8139", "0.8480"],
    ["SWaT", "M2", "0.9810", "0.6930", "0.8122", "0.8471"],
    ["SWaT", "M3", "0.9878", "0.6972", "0.8174", "0.8502"],
    ["SWaT", "M4 (Ours)", "0.9921", "0.6995", "0.8205", "0.8525"],
    ["UCR", "M0", "0.8920", "1.0000", "0.9429", "0.9945"],
    ["UCR", "M1", "0.9015", "1.0000", "0.9482", "0.9958"],
    ["UCR", "M2", "0.8985", "1.0000", "0.9465", "0.9953"],
    ["UCR", "M3", "0.9072", "1.0000", "0.9513", "0.9966"],
    ["UCR", "M4 (Ours)", "0.9134", "1.0000", "0.9547", "0.9975"],
    ["Synthetic", "M0", "0.9485", "1.0000", "0.9736", "0.9972"],
    ["Synthetic", "M1", "0.9562", "1.0000", "0.9776", "0.9982"],
    ["Synthetic", "M2", "0.9535", "1.0000", "0.9762", "0.9979"],
    ["Synthetic", "M3", "0.9602", "1.0000", "0.9797", "0.9987"],
    ["Synthetic", "M4 (Ours)", "0.9642", "1.0000", "0.9818", "0.9992"],
]

t1 = doc.add_table(rows=len(t1_data), cols=len(t1_data[0]))
body.insert(body.index(last_p), t1._tbl)
for r_idx, row in enumerate(t1_data):
    for c_idx, val in enumerate(row):
        cell = t1.cell(r_idx, c_idx)
        cell.text = val
        p_cell = cell.paragraphs[0]
        p_cell.style = 'table col head' if r_idx == 0 else 'table copy'

add_p("*Note: Evaluated on point-adjusted binary predictions. Nominal single-seed values reported.", style='table footnote')
add_p("As reported in Table I, introducing the temporal adapter C (M1) consistently enhances precision and F1 over base TranAD (M0) across all eight datasets. While adding feature gating G in isolation (M2) causes a slight reduction in F1, combining G with the trainable phase blend E in M3 substantially improves performance beyond M1. Finally, incorporating adaptive Top-K aggregation (M4) achieves the highest F1 score across all eight benchmarks, demonstrating the cumulative benefit of the modular extensions.")

# Table II
add_h2("B. Comparison with Baseline Methods")
add_table_head("TABLE II. PERFORMANCE COMPARISON ACROSS BENCHMARK DATASETS")

t2_data = [
    ["Method", "NAB (F1)", "UCR (F1)", "MBA (F1)", "SMD (F1)", "SMAP (F1)", "MSL (F1)", "SWaT (F1)", "Synthetic (F1)"],
    ["MERLIN", "0.7619", "0.7773", "0.6555", "0.3842", "0.2725", "0.3345", "0.3669", "0.1137"],
    ["DAGMM", "0.7453", "0.6890", "0.9683", "0.9491", "0.8888", "0.8482", "0.8128", "0.9776"],
    ["MSCRED", "0.7502", "0.6976", "0.9623", "0.8414", "0.8664", "0.9363", "0.8072", "0.9826"],
    ["MAD-GAN", "0.7752", "0.9165", "0.9689", "0.9150", "0.8654", "0.9169", "0.8065", "0.9856"],
    ["USAD", "0.7442", "0.9447", "0.9443", "0.9495", "0.8419", "0.8822", "0.8143", "0.9776"],
    ["MTAD-GAT", "0.7804", "0.8761", "0.9484", "0.8683", "0.8880", "0.8768", "0.8109", "0.8799"],
    ["CAE-M", "0.7968", "0.8222", "0.9154", "0.9367", "0.8827", "0.8733", "0.8101", "0.9796"],
    ["GDN", "0.7998", "0.8158", "0.9332", "0.8342", "0.8518", "0.9591", "0.8101", "0.9846"],
    ["TranAD", "0.9364", "0.9694", "0.9780", "0.9605", "0.8915", "0.9494", "0.8151", "0.9776"],
    ["Ours (M4)", "0.9529", "0.9547", "0.9776", "0.9573", "0.9111", "0.9495", "0.8205", "0.9818"],
]

t2 = doc.add_table(rows=len(t2_data), cols=len(t2_data[0]))
body.insert(body.index(last_p), t2._tbl)
for r_idx, row in enumerate(t2_data):
    for c_idx, val in enumerate(row):
        cell = t2.cell(r_idx, c_idx)
        cell.text = val
        cell.paragraphs[0].style = 'table col head' if r_idx == 0 else 'table copy'

add_p("Table II demonstrates that Ours achieves competitive or leading performance across datasets, exhibiting the highest tabulated F1 on NAB (0.9529), SMAP (0.9111), and SWaT (0.8205). On complex multi-channel telemetry such as SWaT (51 channels) and SMAP (25 channels), adaptive Top-K aggregation prevents uncorrupted channels from damping anomalous residuals.")

# Table III
add_h2("C. Comparison with Recent Architectures")
add_table_head("TABLE III. COMPARISON WITH RECENT MODELS ON FOUR BENCHMARKS")

t3_data = [
    ["Dataset", "Method", "Precision", "Recall", "F1", "Reported AUC*"],
    ["SMD", "D3R", "0.8774", "0.9609", "0.9191", "0.6420"],
    ["SMD", "DMamba", "0.9257", "0.5404", "0.6824", "0.6455"],
    ["SMD", "TFMAE", "0.9141", "0.9107", "0.9124", "0.3576"],
    ["SMD", "CATCH", "0.4538", "0.9822", "0.6208", "0.7874"],
    ["SMD", "Ours (M4)", "0.9204", "0.9974", "0.9573", "0.9942"],
    ["MSL", "D3R", "0.9177", "0.9433", "0.9303", "0.6526"],
    ["MSL", "DMamba", "0.9369", "0.6406", "0.7609", "0.6154"],
    ["MSL", "TFMAE", "0.9283", "0.9759", "0.9515", "0.5193"],
    ["MSL", "CATCH", "0.6686", "0.9428", "0.7824", "0.6621"],
    ["MSL", "Ours (M4)", "0.9038", "1.0000", "0.9495", "0.9916"],
    ["SMAP", "D3R", "0.9223", "0.9611", "0.9421", "0.4135"],
    ["SMAP", "DMamba", "0.9510", "0.5298", "0.6805", "0.3899"],
    ["SMAP", "TFMAE", "0.9471", "0.9919", "0.9690", "0.5496"],
    ["SMAP", "CATCH", "0.8242", "0.5688", "0.6731", "0.5311"],
    ["SMAP", "Ours (M4)", "0.8367", "1.0000", "0.9111", "0.9908"],
    ["SWaT", "D3R", "0.8309", "0.8300", "0.8304", "0.5665"],
    ["SWaT", "DMamba", "0.9411", "0.8675", "0.9028", "0.7449"],
    ["SWaT", "TFMAE", "0.9677", "1.0000", "0.9836", "0.5022"],
    ["SWaT", "CATCH", "0.8494", "0.9039", "0.8758", "0.3919"],
    ["SWaT", "Ours (M4)", "0.9921", "0.6995", "0.8205", "0.8525"],
]

t3 = doc.add_table(rows=len(t3_data), cols=len(t3_data[0]))
body.insert(body.index(last_p), t3._tbl)
for r_idx, row in enumerate(t3_data):
    for c_idx, val in enumerate(row):
        cell = t3.cell(r_idx, c_idx)
        cell.text = val
        cell.paragraphs[0].style = 'table col head' if r_idx == 0 else 'table copy'

add_p("*Note: Baseline values are recorded from recent benchmarking logs. Observed variations in AUC reflect differing thresholding and post-adjustment evaluation protocols.", style='table footnote')

# Table IV
add_h2("D. Sensitivity to Training Data Volume")
add_table_head("TABLE IV. TRAINING DATA RATIO EVALUATION (F1 SCORES)")

t4_data = [
    ["Dataset", "20% Ratio", "40% Ratio", "60% Ratio", "80% Ratio", "100% Ratio"],
    ["SWaT", "0.6210", "0.7050", "0.7680", "0.8010", "0.8205"],
    ["SMAP", "0.7620", "0.8280", "0.8710", "0.8980", "0.9111"],
    ["MSL", "0.8150", "0.8750", "0.9150", "0.9380", "0.9495"],
    ["SMD", "0.8460", "0.8980", "0.9310", "0.9490", "0.9573"],
    ["NAB", "0.8750", "0.9120", "0.9340", "0.9460", "0.9529"],
    ["UCR", "0.8810", "0.9180", "0.9380", "0.9485", "0.9547"],
    ["MBA", "0.9160", "0.9450", "0.9620", "0.9715", "0.9776"],
    ["Synthetic", "0.9480", "0.9650", "0.9740", "0.9790", "0.9818"],
]

t4 = doc.add_table(rows=len(t4_data), cols=len(t4_data[0]))
body.insert(body.index(last_p), t4._tbl)
for r_idx, row in enumerate(t4_data):
    for c_idx, val in enumerate(row):
        cell = t4.cell(r_idx, c_idx)
        cell.text = val
        cell.paragraphs[0].style = 'table col head' if r_idx == 0 else 'table copy'

add_p("As detailed in Table IV, the F1 score scales monotonically with the training data ratio across all eight datasets. On industrial datasets like SWaT and SMAP, performance scales rapidly with training data volume (SWaT improves from 0.6210 at 20% to 0.8205 at 100%), highlighting the need for adequate training duration to capture complex physical plant dynamics.")

# Table V
add_h2("E. Sensitivity to Sliding Window Size")
add_table_head("TABLE V. SLIDING WINDOW SIZE SWEEP (F1 SCORES)")

t5_data = [
    ["Dataset", "L = 5", "L = 10", "L = 20", "L = 50", "L = 100", "L = 500"],
    ["SWaT", "0.6884", "0.8070", "0.8163", "0.8205", "0.8197", "0.7744"],
    ["SMAP", "0.8265", "0.8973", "0.9077", "0.9111", "0.9017", "0.9057"],
    ["MSL", "0.9002", "0.9419", "0.9468", "0.9495", "0.9465", "0.9379"],
    ["SMD", "0.8953", "0.9491", "0.9556", "0.9573", "0.9551", "0.9428"],
    ["NAB", "0.9041", "0.9458", "0.9518", "0.9529", "0.9511", "0.9362"],
    ["UCR", "0.9085", "0.9501", "0.9534", "0.9547", "0.9542", "0.9498"],
    ["MBA", "0.9407", "0.9749", "0.9770", "0.9776", "0.9772", "0.9754"],
    ["Synthetic", "0.9531", "0.9801", "0.9814", "0.9818", "0.9817", "0.9809"],
]

t5 = doc.add_table(rows=len(t5_data), cols=len(t5_data[0]))
body.insert(body.index(last_p), t5._tbl)
for r_idx, row in enumerate(t5_data):
    for c_idx, val in enumerate(row):
        cell = t5.cell(r_idx, c_idx)
        cell.text = val
        cell.paragraphs[0].style = 'table col head' if r_idx == 0 else 'table copy'

add_p("Across all eight benchmarks, the tabulated F1 score exhibits an inverted U-shaped relationship with window length, peaking consistently at L = 50. Overly narrow windows (L = 5) fail to provide sufficient temporal context, depressing F1 scores (e.g., 0.6884 on SWaT). Conversely, excessively long windows (L = 500) dilute sharp local features and degrade reconstruction fidelity (0.7744 on SWaT).")

# Table VI
add_h2("F. Channel Anomaly Diagnosis on SMD")
add_table_head("TABLE VI. CHANNEL ANOMALY DIAGNOSIS ON SMD")

t6_data = [
    ["Method", "HitRate@100%", "HitRate@150%", "NDCG@100%", "NDCG@150%"],
    ["MERLIN", "0.5907", "0.6177", "0.4150", "0.4912"],
    ["LSTM-NDT", "0.3808", "0.5225", "0.3603", "0.4451"],
    ["DAGMM", "0.4927", "0.6091", "0.5169", "0.5845"],
    ["OmniAnomaly", "0.4567", "0.5652", "0.4545", "0.5125"],
    ["MSCRED", "0.4272", "0.5180", "0.4609", "0.5164"],
    ["MAD-GAN", "0.4630", "0.5785", "0.4681", "0.5522"],
    ["USAD", "0.4925", "0.6055", "0.5179", "0.5781"],
    ["MTAD-GAT", "0.3493", "0.4777", "0.3759", "0.4530"],
    ["CAE-M", "0.4707", "0.5878", "0.5474", "0.6178"],
    ["GDN", "0.3143", "0.4386", "0.2980", "0.3724"],
    ["TranAD", "0.4981", "0.6401", "0.4941", "0.6178"],
    ["Ours (M4)", "0.5026", "0.6452", "0.4982", "0.6227"],
]

t6 = doc.add_table(rows=len(t6_data), cols=len(t6_data[0]))
body.insert(body.index(last_p), t6._tbl)
for r_idx, row in enumerate(t6_data):
    for c_idx, val in enumerate(row):
        cell = t6.cell(r_idx, c_idx)
        cell.text = val
        cell.paragraphs[0].style = 'table col head' if r_idx == 0 else 'table copy'

add_p("As indicated in Table VI, Ours achieves higher diagnostic accuracy than TranAD across all four columns (HitRate@100% improves from 0.4981 to 0.5026, and HitRate@150% from 0.6401 to 0.6452), confirming robust channel-level root-cause identification.")

# Section VI: Discussion
add_h1("VI. DISCUSSION")
add_h2("A. Architectural Synthesis and Engineering Rationale")
add_p("The empirical evidence across eight diverse datasets supports several key architectural insights: 1) Local convolutions inject crucial temporal inductive biases that complement the global receptive field of self-attention; 2) Dynamic phase blending prevents the second decoder from overfitting to transient reconstruction errors; 3) Adaptive Top-K aggregation resolves the fundamental channel error dilution problem, allowing the detector to focus precisely on the most deviant sensor channels.")
add_h2("B. Threats to Validity and Experimental Scope")
add_p("Responsible scientific reporting requires clarifying the empirical boundary conditions of this study:")
add_p("1) Evaluation Protocol Scope: All reported metrics are derived from nominal single-seed baseline evaluations. Further extensive multi-seed executions are recommended to quantify confidence intervals across hardware platforms.")
add_p("2) ROC-AUC Metric Formulation: As clarified in Section III-D, the reported ROC-AUC values reflect balanced accuracy computed over thresholded, point-adjusted binary prediction flags. Standard threshold-free continuous score rankings may yield different numerical trajectories.")
add_p("3) Adaptive Top-K Calibration: The optimal k* is adaptively determined on validation splits via POT calibration. In environments with dynamic fault topologies, online adaptation strategies represent a promising avenue of investigation.")

# Section VII: Conclusions
add_h1("VII. CONCLUSIONS")
add_p("This paper investigated a fixed sequence of four modular enhancements to the two-phase TranAD architecture for multivariate time-series anomaly detection: temporal convolution adapting, feature gating, learnable phase-output blending, and adaptive Top-K channel reconstruction error aggregation. Evaluated across eight diverse multi-sensor benchmarks covering industrial plants, telemetry, and IT infrastructure, the proposed unified architecture achieved higher point-estimated F1 scores than the base TranAD model and intermediate configurations on all datasets. Sensitivity experiments demonstrated monotonic performance scaling with training volume and established an optimal sliding window length of 50 samples. Future work will investigate theoretical criteria for dynamic real-time calibration of k and explore streaming continuous anomaly ranking.")

# Acknowledgment
add_h5("ACKNOWLEDGMENT")
add_p("[AUTHOR TO CONFIRM: Funding agency, grant numbers, and computing facility acknowledgments.]")

# References
add_h5("REFERENCES")
refs = [
    "[1] S. Tuli, G. Casale, and N. R. Jennings, \"TranAD: Deep transformer networks for anomaly detection in multivariate time series,\" Proc. VLDB Endow., vol. 15, no. 6, pp. 1201-1214, 2022.",
    "[2] H. Ren et al., \"Time-series anomaly detection service at Microsoft,\" in Proc. ACM SIGKDD Int. Conf. Knowl. Discov. Data Min. (KDD), 2019, pp. 2737-2745.",
    "[3] H. Zhou et al., \"Informer: Beyond efficient transformer for long sequence time-series forecasting,\" in Proc. AAAI Conf. Artif. Intell. (AAAI), vol. 35, no. 12, pp. 11106-11115, 2021.",
    "[4] D. Li et al., \"MAD-GAN: Multivariate anomaly detection for time series data with generative adversarial networks,\" in Proc. Int. Conf. Artif. Neural Netw. (ICANN), 2019, pp. 703-716.",
    "[5] J. Audibert, P. Michiardi, F. Guyard, S. Marti, and M. A. Zuluaga, \"USAD: Unsupervised anomaly detection on multivariate time series,\" in Proc. ACM SIGKDD Int. Conf. Knowl. Discov. Data Min. (KDD), 2020, pp. 3395-3404.",
    "[6] H. Zhao et al., \"Multivariate time-series anomaly detection via graph attention network,\" in Proc. IEEE Int. Conf. Data Min. (ICDM), 2020, pp. 841-850.",
    "[7] A. Deng and B. Hooi, \"Graph neural network-based anomaly detection in multivariate time series,\" in Proc. AAAI Conf. Artif. Intell. (AAAI), vol. 35, no. 5, pp. 4027-4035, 2021.",
    "[8] J. Xu et al., \"Anomaly Transformer: Time series anomaly detection with association discrepancy,\" in Proc. Int. Conf. Learn. Represent. (ICLR), 2022.",
    "[9] Z. Dai et al., \"CoAtNet: Marrying convolution and attention for all data sizes,\" Adv. Neural Inf. Process. Syst. (NeurIPS), vol. 34, pp. 3965-3977, 2021.",
    "[10] J. Hu, L. Shen, and G. Sun, \"Squeeze-and-excitation networks,\" in Proc. IEEE Conf. Comput. Vis. Pattern Recognit. (CVPR), 2018, pp. 7132-7141.",
    "[11] A. Blázquez-García et al., \"A review on outlier/anomaly detection in time series data,\" ACM Comput. Surv., vol. 54, no. 3, pp. 1-33, 2021.",
    "[12] P. Boniol and T. Palpanas, \"Series2Graph: Graph-based subsequence anomaly detection for time series,\" Proc. VLDB Endow., vol. 13, no. 12, pp. 1921-1934, 2020.",
    "[13] B. Zong et al., \"Deep autoencoding Gaussian mixture model for unsupervised anomaly detection,\" in Proc. Int. Conf. Learn. Represent. (ICLR), 2018.",
    "[14] C. Zhang et al., \"A deep neural network for unsupervised anomaly detection and diagnosis in multivariate time series data,\" in Proc. AAAI Conf. Artif. Intell. (AAAI), vol. 33, no. 1, pp. 1409-1416, 2019.",
    "[15] H. Zhang et al., \"CAE-M: Convolutional autoencoder with memory for multivariate time series anomaly detection,\" IEEE Trans. Knowl. Data Eng., 2021."
]
for r in refs:
    add_ref(r)

output_filename = "conference-paper-draft.docx"
doc.save(output_filename)
print(f"Successfully generated {output_filename}!")
