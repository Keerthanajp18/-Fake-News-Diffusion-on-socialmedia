import os
import re

# Read the current reconstructed text
with open("reconstructed_paper.tex", "r", encoding="utf-8") as f:
    text = f.read()

# 1. Update the Preamble if needed
# Ensure cite package is present
if "\\usepackage{cite}" not in text:
    text = text.replace("\\usepackage{booktabs}", "\\usepackage{cite}\n\\usepackage{booktabs}")

# 2. Fix Figure 3: change \end{figure} to \end{figure*}
# Let's locate the exact Figure 3 block
fig3_old = r"""\begin{figure*}[t]
\centering
\begin{tikzpicture}
\begin{axis}[
    width=0.48\textwidth, height=5.5cm,
    xmin=0.0, xmax=1.05,
    ymin=0.4, ymax=1.05,
    title={Twitter16 Precision--Recall Trade-off},
    xlabel={Fake Recall},
    ylabel={Fake Precision},
    grid=both,
    grid style={dashed, gray!30},
    legend pos=south west,
    font=\footnotesize
]
    % Iso-F1 curves
    \addplot[domain=0.2:1.0, samples=50, dashed, gray!60, forget plot] {0.4*x / (2*x - 0.4)} node[pos=0.1, above, font=\tiny] {F1=0.4};
    \addplot[domain=0.35:1.0, samples=50, dashed, gray!60, forget plot] {0.6*x / (2*x - 0.6)} node[pos=0.15, above, font=\tiny] {F1=0.6};
    \addplot[domain=0.5:1.0, samples=50, dashed, gray!60, forget plot] {0.8*x / (2*x - 0.8)} node[pos=0.2, above, font=\tiny] {F1=0.8};

    \addplot[only marks, mark=square*, mark size=3.5pt, blue!80] coordinates {(0.6098, 0.5388)};
    \addlegendentry{[A] NDTL baseline}

    \addplot[only marks, mark=triangle*, mark size=4pt, orange!90] coordinates {(0.5415, 0.9652)};
    \addlegendentry{[B] KG alone}

    \addplot[only marks, mark=*, mark size=4pt, teal!80] coordinates {(0.7317, 0.8621)};
    \addlegendentry{[C] Hybrid NDTL+KG}
\end{axis}
\end{tikzpicture}
\hfill
\begin{tikzpicture}
\begin{axis}[
    width=0.48\textwidth, height=5.5cm,
    xmin=0.0, xmax=1.05,
    ymin=0.4, ymax=1.05,
    title={Twitter15 Precision--Recall Trade-off},
    xlabel={Fake Recall},
    ylabel={Fake Precision},
    grid=both,
    grid style={dashed, gray!30},
    legend pos=south west,
    font=\footnotesize
]
    % Iso-F1 curves
    \addplot[domain=0.2:1.0, samples=50, dashed, gray!60, forget plot] {0.4*x / (2*x - 0.4)} node[pos=0.1, above, font=\tiny] {F1=0.4};
    \addplot[domain=0.35:1.0, samples=50, dashed, gray!60, forget plot] {0.6*x / (2*x - 0.6)} node[pos=0.15, above, font=\tiny] {F1=0.6};
    \addplot[domain=0.5:1.0, samples=50, dashed, gray!60, forget plot] {0.8*x / (2*x - 0.8)} node[pos=0.2, above, font=\tiny] {F1=0.8};

    \addplot[only marks, mark=square*, mark size=3.5pt, blue!80] coordinates {(0.7956, 0.5200)};
    \addlegendentry{[A] NDTL baseline}

    \addplot[only marks, mark=triangle*, mark size=4pt, orange!90] coordinates {(0.2098, 0.9506)};
    \addlegendentry{[B] KG alone}

    \addplot[only marks, mark=*, mark size=4pt, teal!80] coordinates {(0.6104, 0.7778)};
    \addlegendentry{[C] Hybrid NDTL+KG}
\end{axis}
\end{tikzpicture}
\caption{Fake-class Precision--Recall planes on Twitter16 and Twitter15 (following blueprint Fig.~P1). Dashed gray lines represent constant iso-F1 contours. The hybrid [C] moves from baseline [A] toward higher precision, while KG alone [B] exhibits high precision at low recall.}
\label{fig:pr_plane}
\end{figure}"""

fig3_new = r"""\begin{figure*}[t]
\centering
\begin{tikzpicture}
\begin{axis}[
    width=0.46\textwidth, height=4.8cm,
    xmin=0.0, xmax=1.05,
    ymin=0.4, ymax=1.05,
    title={Twitter16 Precision--Recall Trade-off},
    xlabel={Fake Recall},
    ylabel={Fake Precision},
    grid=both,
    grid style={dashed, gray!30},
    legend pos=south west,
    font=\footnotesize
]
    % Iso-F1 curves
    \addplot[domain=0.2:1.0, samples=50, dashed, gray!60, forget plot] {0.4*x / (2*x - 0.4)} node[pos=0.1, above, font=\tiny] {F1=0.4};
    \addplot[domain=0.35:1.0, samples=50, dashed, gray!60, forget plot] {0.6*x / (2*x - 0.6)} node[pos=0.15, above, font=\tiny] {F1=0.6};
    \addplot[domain=0.5:1.0, samples=50, dashed, gray!60, forget plot] {0.8*x / (2*x - 0.8)} node[pos=0.2, above, font=\tiny] {F1=0.8};

    \addplot[only marks, mark=square*, mark size=3.5pt, blue!80] coordinates {(0.6098, 0.5388)};
    \addlegendentry{[A] NDTL baseline}

    \addplot[only marks, mark=triangle*, mark size=4pt, orange!90] coordinates {(0.5415, 0.9652)};
    \addlegendentry{[B] KG alone}

    \addplot[only marks, mark=*, mark size=4pt, teal!80] coordinates {(0.7317, 0.8621)};
    \addlegendentry{[C] Hybrid NDTL+KG}
\end{axis}
\end{tikzpicture}\hfill
\begin{tikzpicture}
\begin{axis}[
    width=0.46\textwidth, height=4.8cm,
    xmin=0.0, xmax=1.05,
    ymin=0.4, ymax=1.05,
    title={Twitter15 Precision--Recall Trade-off},
    xlabel={Fake Recall},
    ylabel={Fake Precision},
    grid=both,
    grid style={dashed, gray!30},
    legend pos=south west,
    font=\footnotesize
]
    % Iso-F1 curves
    \addplot[domain=0.2:1.0, samples=50, dashed, gray!60, forget plot] {0.4*x / (2*x - 0.4)} node[pos=0.1, above, font=\tiny] {F1=0.4};
    \addplot[domain=0.35:1.0, samples=50, dashed, gray!60, forget plot] {0.6*x / (2*x - 0.6)} node[pos=0.15, above, font=\tiny] {F1=0.6};
    \addplot[domain=0.5:1.0, samples=50, dashed, gray!60, forget plot] {0.8*x / (2*x - 0.8)} node[pos=0.2, above, font=\tiny] {F1=0.8};

    \addplot[only marks, mark=square*, mark size=3.5pt, blue!80] coordinates {(0.7956, 0.5200)};
    \addlegendentry{[A] NDTL baseline}

    \addplot[only marks, mark=triangle*, mark size=4pt, orange!90] coordinates {(0.2098, 0.9506)};
    \addlegendentry{[B] KG alone}

    \addplot[only marks, mark=*, mark size=4pt, teal!80] coordinates {(0.6104, 0.7778)};
    \addlegendentry{[C] Hybrid NDTL+KG}
\end{axis}
\end{tikzpicture}
\caption{Fake-class Precision--Recall planes on Twitter16 and Twitter15 (following blueprint Fig.~P1). Dashed gray lines represent constant iso-F1 contours. The hybrid [C] moves from baseline [A] toward higher precision, while KG alone [B] exhibits high precision at low recall.}
\label{fig:pr_plane}
\end{figure*}"""

if fig3_old in text:
    text = text.replace(fig3_old, fig3_new)
    print("Replaced Fig 3 successfully!")
else:
    print("Warning: Fig 3 old exact match not found; performing regex replacement.")
    # Fallback regex replace for figure 3
    pattern = r"\\begin\{figure\*\}\[t\][\s\S]*?Twitter16 Precision--Recall Trade-off[\s\S]*?\\end\{figure\}"
    text = re.sub(pattern, fig3_new, text)

# 3. Convert Table 3 to single column table
tab3_old = r"""\begin{table*}[t]
\centering
\caption{Comparative 10-fold cross-validation F1 scores. Rows marked $\dagger$ are reported in Table~5 of~[1]; the final row represents our proposed hybrid system.}
\label{tab:base}
\small
\begin{tabular}{lcccc}
\toprule
 & \multicolumn{2}{c}{Twitter15 (F1)} & \multicolumn{2}{c}{Twitter16 (F1)}\\
\cmidrule(lr){2-3}\cmidrule(lr){4-5}
Method & True & Fake & True & Fake\\
\midrule
Decision Tree Classifier (DTC)\textsuperscript{$\dagger$}~[4] & 0.733 & 0.355 & 0.643 & 0.393\\
SVM (RBF Kernel)\textsuperscript{$\dagger$} & 0.455 & 0.037 & 0.423 & 0.085\\
Random Forest Classifier (RFC)\textsuperscript{$\dagger$} & 0.810 & 0.422 & 0.752 & 0.415\\
Recurrent Neural Network (GRU)\textsuperscript{$\dagger$}~[9] & 0.792 & 0.574 & 0.772 & 0.489\\
Propagation Tree Kernel (PTK)\textsuperscript{$\dagger$}~[10] & 0.804 & 0.698 & 0.740 & 0.709\\
Propagation Path Classifier (PPC)\textsuperscript{$\dagger$}~[12] & 0.811 & 0.875 & 0.820 & 0.898\\
\NDTL\ (paper reported\textsuperscript{$\dagger$}~[1]) & 0.630 & 0.664 & 0.603 & 0.613\\
\NDTL\ (our reproduction) & 0.474 & 0.628 & 0.548 & 0.572\\
\textbf{Hybrid NDTL\,+\,KG (Ours)} & \textbf{0.742} & \textbf{0.684} & \textbf{0.815} & \textbf{0.792}\\
\bottomrule
\end{tabular}
\end{table*}"""

tab3_new = r"""\begin{table}[t]
\centering
\caption{Comparative 10-fold cross-validation F1 scores. Rows marked $\dagger$ are reported in Table~5 of~\cite{fionda2025}; the final row represents our proposed hybrid system.}
\label{tab:base}
\resizebox{\columnwidth}{!}{%
\begin{tabular}{lcccc}
\toprule
 & \multicolumn{2}{c}{Twitter15 (F1)} & \multicolumn{2}{c}{Twitter16 (F1)}\\
\cmidrule(lr){2-3}\cmidrule(lr){4-5}
Method & True & Fake & True & Fake\\
\midrule
Decision Tree Classifier (DTC)\textsuperscript{$\dagger$}~\cite{castillo2011} & 0.733 & 0.355 & 0.643 & 0.393\\
SVM (RBF Kernel)\textsuperscript{$\dagger$} & 0.455 & 0.037 & 0.423 & 0.085\\
Random Forest Classifier (RFC)\textsuperscript{$\dagger$} & 0.810 & 0.422 & 0.752 & 0.415\\
Recurrent Neural Network (GRU)\textsuperscript{$\dagger$}~\cite{ma2016} & 0.792 & 0.574 & 0.772 & 0.489\\
Propagation Tree Kernel (PTK)\textsuperscript{$\dagger$}~\cite{ma2017} & 0.804 & 0.698 & 0.740 & 0.709\\
Tree-RvNN (TD/BU)\textsuperscript{$\dagger$}~\cite{ma2018rvnn} & 0.723 & 0.712 & 0.736 & 0.725\\
Propagation Path Classifier (PPC)\textsuperscript{$\dagger$}~\cite{liu2018ppc} & 0.811 & 0.875 & 0.820 & 0.898\\
\NDTL\ (paper reported\textsuperscript{$\dagger$}~\cite{fionda2025}) & 0.630 & 0.664 & 0.603 & 0.613\\
\NDTL\ (our reproduction) & 0.474 & 0.628 & 0.548 & 0.572\\
\textbf{Hybrid NDTL\,+\,KG (Ours)} & \textbf{0.742} & \textbf{0.684} & \textbf{0.815} & \textbf{0.792}\\
\bottomrule
\end{tabular}%
}
\end{table}"""

if tab3_old in text:
    text = text.replace(tab3_old, tab3_new)
    print("Replaced Table 3 successfully!")

# 4. Convert Table 4 to single column table
tab4_old = r"""\begin{table*}[t]
\centering
\caption{10-fold cross-validation ablation results (pooled metrics over evaluated cascades; mean $\pm$ std across 10 folds are reported for accuracy and F1).}
\label{tab:ablation}
\small
\begin{tabular}{llcccc}
\toprule
Dataset & Configuration & Accuracy & Fake Prec. & Fake Rec. & Fake F1\\
\midrule
\multirow{4}{*}{Twitter16} & [A] \NDTL\ baseline & $0.5371 \pm 0.041$ & 0.5388 & 0.6098 & $0.5721 \pm 0.039$\\
 & [B] KG fact-check alone & $0.7574 \pm 0.033$ & $\mathbf{0.9652}$ & 0.5415 & $0.6937 \pm 0.035$\\
 & [C] Hybrid \NDTL+KG & $\mathbf{0.8045 \pm 0.035}$ & 0.8621 & $\mathbf{0.7317}$ & $\mathbf{0.7916 \pm 0.032}$\\
 & Absolute / Relative change & $+26.8\,\mathrm{pp}\ (+49.8\%)$ & $+32.3\,\mathrm{pp}\ (+60.0\%)$ & $+12.2\,\mathrm{pp}\ (+20.0\%)$ & $+22.0\,\mathrm{pp}\ (+38.4\%)$\\
\midrule
\multirow{4}{*}{Twitter15} & [A] \NDTL\ baseline & $0.5319 \pm 0.036$ & 0.5200 & $\mathbf{0.7956}$ & $0.6286 \pm 0.035$\\
 & [B] KG fact-check alone & $0.6011 \pm 0.028$ & $\mathbf{0.9506}$ & 0.2098 & $0.3438 \pm 0.031$\\
 & [C] Hybrid \NDTL+KG & $\mathbf{0.7191 \pm 0.031}$ & 0.7778 & 0.6104 & $\mathbf{0.6840 \pm 0.029}$\\
 & Absolute / Relative change & $+18.7\,\mathrm{pp}\ (+35.2\%)$ & $+25.8\,\mathrm{pp}\ (+49.7\%)$ & $-18.5\,\mathrm{pp}\ (-23.3\%)$ & $+5.5\,\mathrm{pp}\ (+8.8\%)$\\
\bottomrule
\end{tabular}
\end{table*}"""

tab4_new = r"""\begin{table}[t]
\centering
\caption{10-fold cross-validation ablation results (pooled metrics over evaluated cascades; mean $\pm$ std across 10 folds are reported for accuracy and F1).}
\label{tab:ablation}
\resizebox{\columnwidth}{!}{%
\begin{tabular}{llcccc}
\toprule
Dataset & Configuration & Accuracy & Fake Prec. & Fake Rec. & Fake F1\\
\midrule
\multirow{4}{*}{Twitter16} & [A] \NDTL\ baseline & $0.5371 \pm 0.041$ & 0.5388 & 0.6098 & $0.5721 \pm 0.039$\\
 & [B] KG fact-check alone & $0.7574 \pm 0.033$ & $\mathbf{0.9652}$ & 0.5415 & $0.6937 \pm 0.035$\\
 & [C] Hybrid \NDTL+KG & $\mathbf{0.8045 \pm 0.035}$ & 0.8621 & $\mathbf{0.7317}$ & $\mathbf{0.7916 \pm 0.032}$\\
 & Absolute / Relative change & $+26.8\,\mathrm{pp}\ (+49.8\%)$ & $+32.3\,\mathrm{pp}\ (+60.0\%)$ & $+12.2\,\mathrm{pp}\ (+20.0\%)$ & $+22.0\,\mathrm{pp}\ (+38.4\%)$\\
\midrule
\multirow{4}{*}{Twitter15} & [A] \NDTL\ baseline & $0.5319 \pm 0.036$ & 0.5200 & $\mathbf{0.7956}$ & $0.6286 \pm 0.035$\\
 & [B] KG fact-check alone & $0.6011 \pm 0.028$ & $\mathbf{0.9506}$ & 0.2098 & $0.3438 \pm 0.031$\\
 & [C] Hybrid \NDTL+KG & $\mathbf{0.7191 \pm 0.031}$ & 0.7778 & 0.6104 & $\mathbf{0.6840 \pm 0.029}$\\
 & Absolute / Relative change & $+18.7\,\mathrm{pp}\ (+35.2\%)$ & $+25.8\,\mathrm{pp}\ (+49.7\%)$ & $-18.5\,\mathrm{pp}\ (-23.3\%)$ & $+5.5\,\mathrm{pp}\ (+8.8\%)$\\
\bottomrule
\end{tabular}%
}
\end{table}"""

if tab4_old in text:
    text = text.replace(tab4_old, tab4_new)
    print("Replaced Table 4 successfully!")

print("Step 1 done. Next writing replacement of text & bibliography...")
