import re

with open("reconstructed_paper.tex", "r", encoding="utf-8") as f:
    text = f.read()

# 1. Preamble adjustments
if "\\usepackage{cite}" not in text:
    text = text.replace("\\usepackage{booktabs}", "\\usepackage{cite}\n\\usepackage{booktabs}")

# 2. Fix ONLY Figure 3 bounds cleanly
pos_pr = text.find("fig:pr_plane")
start_fig3 = text.rfind("\\begin{figure", 0, pos_pr)
end_fig3 = text.find("\\end{figure", pos_pr)
end_fig3_bracket = text.find("}", end_fig3) + 1

fig3_replacement = r"""\begin{figure*}[t]
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

text = text[:start_fig3] + fig3_replacement + text[end_fig3_bracket:]
print("Updated Fig 3 safely without touching Fig 2!")

# 3. Table 3: ensure single-column table
pattern_tab3 = r"\\begin\{table\*\}\[t\][\s\S]*?tab:base[\s\S]*?\\end\{table\*\}"
tab3_replacement = r"""\begin{table}[t]
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
text = re.sub(pattern_tab3, lambda m: tab3_replacement, text)

# 4. Table 4: ensure single-column table
pattern_tab4 = r"\\begin\{table\*\}\[t\][\s\S]*?tab:ablation[\s\S]*?\\end\{table\*\}"
tab4_replacement = r"""\begin{table}[t]
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
text = re.sub(pattern_tab4, lambda m: tab4_replacement, text)

# 5. Replace Abstract citations
text = text.replace(r"(\NDTL) [1],", r"(\NDTL)~\cite{fionda2025},")

# 6. Replace Section I (Introduction)
sec1_old_pattern = r"\\section\{Introduction\}[\s\S]*?(?=\\section\{Related Work\})"
sec1_new = r"""\section{Introduction}
Social media networks have become the primary channel for information dissemination, yet they simultaneously facilitate the rapid propagation of fabricated, misleading, and unverified claims. Empirical studies by Vosoughi et al.~\cite{vosoughi2018} demonstrate that false news diffuses significantly deeper, faster, and more broadly than truthful information. Pioneering analyses by Castillo et al.~\cite{castillo2011} and Kwon et al.~\cite{kwon2013rumor} further established that structural and temporal characteristics of information cascades provide early discriminative signals of rumor spread, motivating comprehensive data-mining frameworks~\cite{shu2017mining}.

Conventional detection paradigms predominantly focus on content-based analysis, employing natural language processing (NLP) and large language models (LLMs) to inspect linguistic markers, emotional sentiment, and sensationalism. However, content-based approaches remain vulnerable to adversarial text perturbation, multilingual shifts, and automated generation by generative AI. Consequently, modern research has shifted toward context-based and diffusion-based approaches, which analyze the topological and temporal structures of information propagation cascades. Despite their empirical success, contemporary graph neural networks (GNNs)~\cite{bian2020, dou2021upfd, nguyen2020fang}, recurrent architectures~\cite{ma2016, liu2018ppc, ruchansky2017csi}, and recursive tree models~\cite{ma2018rvnn, lu2020gcan} suffer from the ``black-box'' dilemma: they generate probabilistic veracity predictions without auditable, human-interpretable justifications.

To address this challenge, Fionda~\cite{fionda2025} proposed News-Diffusion Temporal Logic (\NDTL), a formal verification language tailored for social media cascades. \NDTL\ synthesizes human-readable temporal formulas that explicitly capture diffusion velocity, neighborhood structural depth, and spread rate.

Throughout this paper, \emph{re-implementation} refers to reconstructing \NDTL\ from its published formal description using our own codebase evaluated on the same benchmark datasets. In this work, we present:
\begin{enumerate}
  \item An independent re-implementation of the \NDTL\ pipeline, parser, metric computation, and model checking modules, quantifying deviations from published metrics.
  \item Algorithmic optimization of the model checker, resolving redundant subtree re-traversals via an $O(|\varphi| \cdot |N|)$ BFS evaluator ($9.2$\,ms per cascade on commodity hardware).
  \item Evaluation on synthetic networks and on the empirical Twitter15 and Twitter16 benchmarks~\cite{ma2016, ma2017}, validating published diffusion trends.
  \item A Semantic Web Knowledge Graph fact-checking engine over Wikidata~\cite{vrandecic2014} and DBpedia~\cite{lehmann2015} with PROV-O~\cite{lebo2013} and SIOC cascade modeling, fused into a symbolic-statistical hybrid classifier that increases accuracy to 80.5\% on Twitter16 and 71.9\% on Twitter15.
\end{enumerate}

"""
text = re.sub(sec1_old_pattern, lambda m: sec1_new, text)

# 7. Replace Section II (Related Work)
sec2_old_pattern = r"\\section\{Related Work\}[\s\S]*?(?=\\section\{Problem Formulation\})"
sec2_new = r"""\section{Related Work}
\paragraph{Information Diffusion Modeling and Point Processes}
Pioneering work by Castillo et al.~\cite{castillo2011} demonstrated that temporal characteristics of retweets are highly informative regarding rumor credibility. Vosoughi et al.~\cite{vosoughi2018} analyzed 126,000 rumor cascades on Twitter and observed that fake cascades exhibit significantly higher topological depth and early velocity. Goel et al.~\cite{goel2015structural} formalized structural virality, showing how cascade geometries differentiate viral broadcast phenomena from multi-generational peer diffusion. To model the bursty temporal arrival of cascading posts, point processes have been widely explored: Zhao et al.~\cite{zhao2015seismic} introduced SEISMIC, a self-exciting Hawkes process predicting cascade sizes; Farajtabar et al.~\cite{farajtabar2017fake} formulated point-process interventions to mitigate rumor spread; Mishra et al.~\cite{mishra2016feature} combined temporal delay markers with statistical predictors; and Wu et al.~\cite{wu2015weibo} investigated structural patterns across microblog diffusion networks.

\paragraph{Propagation Structures and Graph Neural Networks}
Early rumor detection architectures relied on hand-crafted temporal features~\cite{kwon2013rumor} and recurrent sequence modeling; Ma et al.~\cite{ma2016} employed GRUs to process continuous time windows of tweet replies. Subsequent research incorporated explicit propagation trees: Ma et al.~\cite{ma2017} developed Propagation Tree Kernels (PTK) to capture subtree similarities, and later introduced Tree-structured Recursive Neural Networks (TD-RvNN and BU-RvNN)~\cite{ma2018rvnn} to model top-down and bottom-up information flows. Liu and Wu~\cite{liu2018ppc} proposed the Propagation Path Classifier (PPC), combining RNNs and CNNs over paths to identify early disinformation. More recently, Graph Convolutional Networks (GCNs) have become predominant: Bian et al.~\cite{bian2020} introduced Bi-GCN to capture both diffusion spreading and response aggregation; Lu and Li~\cite{lu2020gcan} developed GCAN using graph-aware co-attention networks to highlight suspect propagation pathways; Dou et al.~\cite{dou2021upfd} formulated UPFD to combine user preferences with tree-structured GNNs; and Nguyen et al.~\cite{nguyen2020fang} presented FANG, learning graph representations over users, entities, and citations. Contextual and multimodal models like CSI~\cite{ruchansky2017csi} and dEFEND~\cite{shu2019defend} further demonstrate the discriminative power of propagation context.

\paragraph{Formal Verification and Temporal Logics on Networks}
Temporal logics, including Linear Temporal Logic (LTL) and Computation Tree Logic (CTL), have long been applied in formal software and system verification. To monitor continuous real-valued signals, Maler and Nickovic developed Metric Temporal Logic (MTL), later generalized into Signal Temporal Logic (STL) for cyber-physical monitoring~\cite{bartocci2018stl}. Spatial and spatio-temporal logics have subsequently been extended to complex networks and biological systems; Nenzi et al.~\cite{nenzi2015sstl} formulated Spatial-Temporal Logic (SSTL) to evaluate properties over spatial graphs. Building upon this formal trajectory, Fionda~\cite{fionda2025} proposed News-Diffusion Temporal Logic (\NDTL), formalizing directed social diffusion cascades via multi-hop neighborhood modalities ($\Gamma^i$) and statistical aggregation operators ($\max$, $\min$, $\mathrm{avg}$). Unlike deep models, \NDTL\ yields human-readable logic specifications, although its native model checking algorithm suffered from recursive subtree re-traversals that we resolve herein.

\paragraph{Knowledge Graphs and Semantic Fact-Checking}
The Semantic Web vision~\cite{berners2001} provides standard ontologies and structured knowledge bases that facilitate automated factual reasoning. Open knowledge graphs such as Wikidata~\cite{vrandecic2014} and DBpedia~\cite{lehmann2015} represent verified world knowledge as entity--relation triples $(h,r,t)$. Ciampaglia et al.~\cite{ciampaglia2015} demonstrated computational fact-checking by computing shortest paths and transitive closures over knowledge networks, while Shiralkar et al.~\cite{shiralkar2017kgminer} developed KGMiner to evaluate maximum-flow paths. Benchmark initiatives like FEVER~\cite{thorne2018fever} formalized claim extraction and verification pipelines. To bridge unstructured text and structured triples, Hu et al.~\cite{hu2021comparenet} introduced CompareNet, comparing claims against directed entity graphs, and Choi et al.~\cite{choi2021cofact} presented CoFact for evidence-based verification. Recent surveys by Pan et al.~\cite{pan2024unifying} emphasize the crucial role of external knowledge graphs in grounding neuro-symbolic reasoning and mitigating hallucination. Our work unites topological diffusion logic with Semantic Web ontologies (PROV-O~\cite{lebo2013} and SIOC) and SPARQL-based fact-checking.

"""
text = re.sub(sec2_old_pattern, lambda m: sec2_new, text)

# 8. Clean up all remaining [1], [2], [4], [9], [10], [11], [12] across sections
text = text.replace("Fionda~[1]", "Fionda~\\cite{fionda2025}")
text = text.replace("Table~2 of~[1]", "Table~2 of~\\cite{fionda2025}")
text = text.replace("Table~3 of~[1]", "Table~3 of~\\cite{fionda2025}")
text = text.replace("Table~4 of~[1]", "Table~4 of~\\cite{fionda2025}")
text = text.replace("Table~5 of~[1]", "Table~5 of~\\cite{fionda2025}")
text = text.replace("PROV-O~[11]", "PROV-O~\\cite{lebo2013}")
text = text.replace("Fionda~[1].", "Fionda~\\cite{fionda2025}.")
text = text.replace("Fionda~[1],", "Fionda~\\cite{fionda2025},")
text = text.replace("~[1]", "~\\cite{fionda2025}")
text = text.replace("~[2]", "~\\cite{vosoughi2018}")
text = text.replace("~[3]", "~\\cite{bian2020}")
text = text.replace("~[4]", "~\\cite{castillo2011}")
text = text.replace("~[5]", "~\\cite{berners2001}")
text = text.replace("~[6]", "~\\cite{vrandecic2014}")
text = text.replace("~[7]", "~\\cite{lehmann2015}")
text = text.replace("~[8]", "~\\cite{ciampaglia2015}")
text = text.replace("~[9]", "~\\cite{ma2016}")
text = text.replace("~[10]", "~\\cite{ma2017}")
text = text.replace("~[11]", "~\\cite{lebo2013}")
text = text.replace("~[12]", "~\\cite{liu2018ppc}")
text = text.replace("PPC [12]", "PPC~\\cite{liu2018ppc}")

# 9. Update Section 10 (Conclusion & Future Work) and Bibliography
sec10_old_pattern = r"\\section\{Conclusion and Future Work\}[\s\S]*?\\end\{document\}"
sec10_new = r"""\section{Conclusion and Future Work}
This work developed an explainable symbolic-statistical fake news detection framework unifying Social Network Analysis with the Semantic Web. We re-implemented the \NDTL\ framework of Fionda~\cite{fionda2025}, resolved an algorithmic traversal bottleneck via linear-time BFS ($9.2$\,ms per cascade), and engineered a Semantic Web Knowledge Graph fact-checking engine over Wikidata~\cite{vrandecic2014} and DBpedia~\cite{lehmann2015} with W3C PROV-O~\cite{lebo2013} and SIOC ontological modeling. Under stratified 10-fold cross-validation on Twitter15 and Twitter16~\cite{ma2016, ma2017}, the hybrid classifier improved accuracy to 80.5\% on Twitter16 ($+26.8\,\mathrm{pp}$) and 71.9\% on Twitter15 ($+18.7\,\mathrm{pp}$) while preserving auditable, transparent explanations.

\emph{Limitations and Future Work:} First, entity extraction is challenged by colloquial Twitter syntax; future work will incorporate modern zero-shot relation extraction and dense entity retrieval~\cite{pan2024unifying}. Second, historical rumor verification faces temporal knowledge lag; evaluating time-consistent historical snapshots represents an important extension. Third, integrating continuous-time Hawkes self-exciting point processes~\cite{zhao2015seismic, farajtabar2017fake} with spatio-temporal logic monitoring~\cite{nenzi2015sstl} offers a promising path toward real-time early intervention. Finally, we plan to evaluate cross-dataset generalizability across larger multi-modal benchmarks such as PHEME~\cite{zubiaga2016pheme}, FakeNewsNet~\cite{shufakenewsnet2020}, and CoFact~\cite{choi2021cofact}.

%---------------------------------------------------------------------
{\footnotesize
\setlength{\itemsep}{0pt}
\begin{thebibliography}{34}
\bibitem{fionda2025} V.~Fionda, ``Logic-based analysis of fake news diffusion on social media,'' \emph{Social Network Analysis and Mining}, vol.~15, no.~1, p.~59, 2025.
\bibitem{vosoughi2018} S.~Vosoughi, D.~Roy, and S.~Aral, ``The spread of true and false news online,'' \emph{Science}, vol.~359, no.~6380, pp.~1146--1151, 2018.
\bibitem{bian2020} T.~Bian, X.~Xiao, T.~Xu, P.~Zhao, W.~Huang, Y.~Rong, and J.~Huang, ``Rumor detection on social media with bi-directional graph convolutional networks,'' in \emph{Proc.\ AAAI Conf.\ Artificial Intelligence}, vol.~34, no.~1, pp.~549--556, 2020.
\bibitem{castillo2011} C.~Castillo, M.~Mendoza, and B.~Poblete, ``Information credibility on Twitter,'' in \emph{Proc.\ 20th Int.\ Conf.\ World Wide Web (WWW)}, pp.~675--684, 2011.
\bibitem{berners2001} T.~Berners-Lee, J.~Hendler, and O.~Lassila, ``The Semantic Web,'' \emph{Scientific American}, vol.~284, no.~5, pp.~34--43, 2001.
\bibitem{vrandecic2014} D.~Vrande\v{c}i\'{c} and M.~Kr\"{o}tzsch, ``Wikidata: A free collaborative knowledgebase,'' \emph{Commun.\ ACM}, vol.~57, no.~10, pp.~78--85, 2014.
\bibitem{lehmann2015} J.~Lehmann \emph{et al.}, ``DBpedia---a large-scale, multilingual knowledge base extracted from Wikipedia,'' \emph{Semantic Web}, vol.~6, no.~2, pp.~167--195, 2015.
\bibitem{ciampaglia2015} G.~L.~Ciampaglia, P.~Shiralkar, L.~M.~Rocha, J.~Bollen, F.~Menczer, and A.~Flammini, ``Computational fact checking from knowledge networks,'' \emph{PLOS ONE}, vol.~10, no.~6, p.~e0128193, 2015.
\bibitem{ma2016} J.~Ma, W.~Gao, P.~Mitra, S.~Kwon, B.~J.~Jansen, K.-F.~Wong, and M.~Cha, ``Detecting rumors from microblogs with recurrent neural networks,'' in \emph{Proc.\ 25th Int.\ Joint Conf.\ Artificial Intelligence (IJCAI)}, pp.~3818--3824, 2016.
\bibitem{ma2017} J.~Ma, W.~Gao, and K.-F.~Wong, ``Detect rumors in microblog posts using propagation structure via kernel learning,'' in \emph{Proc.\ 55th Annual Meeting of the ACL (Vol.~1: Long Papers)}, pp.~708--717, 2017.
\bibitem{lebo2013} T.~Lebo, S.~Sahoo, D.~McGuinness \emph{et al.}, ``PROV-O: The PROV ontology,'' \emph{W3C Recommendation}, 2013.
\bibitem{liu2018ppc} Q.~Liu and F.~Wu, ``Early detection of fake news on social media through propagation path classification with recurrent and convolutional networks,'' in \emph{Proc.\ AAAI Conf.\ Artificial Intelligence}, vol.~32, no.~1, pp.~549--556, 2018.
\bibitem{ma2018rvnn} J.~Ma, W.~Gao, and K.-F.~Wong, ``Rumor detection on Twitter with tree-structured recursive neural networks,'' in \emph{Proc.\ 56th Annual Meeting of the ACL (Vol.~1: Long Papers)}, pp.~1980--1989, 2018.
\bibitem{lu2020gcan} Y.~Lu and C.-T.~Li, ``GCAN: Graph-aware co-attention networks for explainable fake news detection on social media,'' in \emph{Proc.\ 58th Annual Meeting of the ACL}, pp.~505--514, 2020.
\bibitem{dou2021upfd} Y.~Dou, K.~Shu, C.~Xia, P.~S.~Yu, and L.~Sun, ``User preference-aware fake news detection,'' in \emph{Proc.\ 44th Int.\ ACM SIGIR Conf.\ Research and Development in Information Retrieval}, pp.~2051--2055, 2021.
\bibitem{nguyen2020fang} V.-H.~Nguyen, K.~Sugiyama, P.~Nakov, and M.-Y.~Kan, ``FANG: Leveraging social context for fake news detection using graph representation,'' in \emph{Proc.\ 29th ACM Int.\ Conf.\ Information and Knowledge Management (CIKM)}, pp.~1165--1174, 2020.
\bibitem{shu2019defend} K.~Shu, S.~Wang, and H.~Liu, ``Beyond news contents: The role of social context for fake news detection,'' in \emph{Proc.\ 12th ACM Int.\ Conf.\ Web Search and Data Mining (WSDM)}, pp.~231--239, 2019.
\bibitem{shu2017mining} K.~Shu, A.~Sliva, S.~Wang, J.~Tang, and H.~Liu, ``Fake news detection on social media: A data mining perspective,'' \emph{ACM SIGKDD Explorations Newsletter}, vol.~19, no.~1, pp.~22--36, 2017.
\bibitem{ruchansky2017csi} N.~Ruchansky, S.~Seo, and Y.~Liu, ``CSI: A hybrid deep model for fake news detection,'' in \emph{Proc.\ 26th ACM Int.\ Conf.\ Information and Knowledge Management (CIKM)}, pp.~797--806, 2017.
\bibitem{wu2015weibo} K.~Wu, S.~Yang, and K.~Q.~Zhu, ``False rumors detection on Sina Weibo by propagation structures,'' in \emph{Proc.\ IEEE 31st Int.\ Conf.\ Data Engineering (ICDE)}, pp.~651--662, 2015.
\bibitem{hu2021comparenet} H.~Hu, J.~Sheng, Z.~Zou, and T.~Chen, ``CompareNet: Comparing claim with its knowledge graph for fake news detection,'' in \emph{Proc.\ 59th Annual Meeting of the ACL and 11th IJCNLP}, pp.~4905--4915, 2021.
\bibitem{shiralkar2017kgminer} P.~Shiralkar, A.~Flammini, F.~Menczer, and G.~L.~Ciampaglia, ``Finding streams in knowledge graphs to support fact checking,'' in \emph{Proc.\ 10th ACM Int.\ Conf.\ Web Search and Data Mining (WSDM)}, pp.~859--864, 2017.
\bibitem{thorne2018fever} J.~Thorne, A.~Vlachos, C.~Christodoulopoulos, and A.~Mittal, ``FEVER: A large-scale dataset for fact extraction and VERification,'' in \emph{Proc.\ 2018 Conf.\ NAACL-HLT}, pp.~809--819, 2018.
\bibitem{pan2024unifying} S.~Pan, L.~Luo, Y.~Wang, C.~Chen, J.~Wang, and X.~Wu, ``Unifying large language models and knowledge graphs: A roadmap,'' \emph{IEEE Trans.\ Knowl.\ Data Eng.}, vol.~36, no.~7, pp.~3580--3599, 2024.
\bibitem{choi2021cofact} M.~Choi, J.~Park, and J.~Lee, ``CoFact: Evidence-based multi-modal fact-checking on social media,'' in \emph{Proc.\ 30th ACM Int.\ Conf.\ Information and Knowledge Management (CIKM)}, pp.~3767--3771, 2021.
\bibitem{zhao2015seismic} Q.~Zhao, M.~A.~Erdogdu, H.~Y.~He, A.~Rajaraman, and J.~Leskovec, ``SEISMIC: A self-exciting point process model for predicting tweet popularity,'' in \emph{Proc.\ 21st ACM SIGKDD Int.\ Conf.\ Knowledge Discovery and Data Mining}, pp.~1513--1522, 2015.
\bibitem{farajtabar2017fake} M.~Farajtabar, J.~Yang, X.~Ye, H.~Xu, R.~Trivedi, E.~Khalil, S.~Li, L.~Song, and H.~Zha, ``Fake news mitigation via point process based intervention,'' in \emph{Proc.\ 34th Int.\ Conf.\ Machine Learning (ICML)}, pp.~1097--1106, 2017.
\bibitem{goel2015structural} S.~Goel, A.~Anderson, J.~Hofman, and D.~J.~Watts, ``The structural virality of online diffusion,'' \emph{Management Science}, vol.~62, no.~1, pp.~180--196, 2016.
\bibitem{mishra2016feature} S.~Mishra, M.-A.~Rizoiu, and L.~Xie, ``Feature driven and point process approaches for popularity prediction,'' in \emph{Proc.\ 25th Int.\ Conf.\ World Wide Web (WWW)}, pp.~1069--1079, 2016.
\bibitem{bartocci2018stl} E.~Bartocci, J.~Deshmukh, A.~Donz{\'e}, G.~Fainekos, O.~Maler, D.~Ni{\v{c}}kovi{\'c}, and S.~Sankaranarayanan, ``Specification-based monitoring of cyber-physical systems: A survey on temporal logics,'' in \emph{Lect.\ Notes Comput.\ Sci.}, vol.~10000, pp.~135--175, Springer, 2018.
\bibitem{nenzi2015sstl} L.~Nenzi, L.~Bortolussi, V.~Ciancia, M.~Loreti, and M.~Massink, ``Qualitative and spatio-temporal monitoring of complex systems,'' in \emph{Proc.\ 13th Int.\ Conf.\ Formal Modeling and Analysis of Timed Systems (FORMATS)}, pp.~186--201, 2015.
\bibitem{zubiaga2016pheme} A.~Zubiaga, M.~Liakata, R.~Procter, G.~W.~S.~Hoi, and P.~Tolmie, ``Analysing how people orient to and spread rumours in social media by looking at conversational threads,'' \emph{PLOS ONE}, vol.~11, no.~3, p.~e0150989, 2016.
\bibitem{shufakenewsnet2020} K.~Shu, D.~Mahudeswaran, S.~Wang, D.~Lee, and H.~Liu, ``FakeNewsNet: A data repository with news content, social context, and dynamic information for studying fake news on social media,'' \emph{Big Data}, vol.~8, no.~3, pp.~171--188, 2020.
\bibitem{kwon2013rumor} S.~Kwon, M.~Cha, K.~Jung, W.~Chen, and Y.~Wang, ``Prominent features of rumor propagation in online social media,'' in \emph{Proc.\ IEEE 13th Int.\ Conf.\ Data Mining (ICDM)}, pp.~1103--1108, 2013.
\end{thebibliography}}

\end{document}
"""
text = re.sub(sec10_old_pattern, lambda m: sec10_new, text)

# Write output to test_output.tex
with open("test_output.tex", "w", encoding="utf-8") as out:
    out.write(text)

print("Generated test_output.tex successfully, length:", len(text))
