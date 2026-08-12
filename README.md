# MotionScorer Experiment Visualizations

This repository contains a drop-in experiment section and publication-quality visualizations for the MotionScorer / nuGuidance paper.

## Drop-in use

Copy the repository contents into the LaTeX project root and include:

```latex
\input{experiment.tex}
```

The parent paper must already load `graphicx`, `booktabs`, `amsmath`, and `xcolor`, define `\methodname{}`, and provide the bibliography keys referenced by the experiment section.

## Main-text organization

- **Table 2** — public human-aligned trajectory scoring: retained unchanged as a numerical table.
- **Table 3** — matched-fit readout comparison: retained unchanged as a numerical table.
- **Figure 4** — native scoring channel: four aligned small multiples for pairwise accuracy, effective score resolution, prompt sensitivity, and output validity.
- **Figure 5** — semantic disagreement regimes: teacher-relative MAE heatmap, TranscendRate, and worst-group robustness.
- **Figure 6** — causal readout interventions: paired changes in WOD pairwise accuracy and held-out teacher-conditioned deflection.
- Adaptation cost and ability preservation remain in the paper appendix.

The visual language follows recent top-tier vision and autonomous-driving papers: pure white background, compact aligned panels, deep muted colors, strong black axes, large semibold typography, direct effect annotations, and minimal unused space.

## Statistical integrity

The checked-in experiment source provides verified summary values but not per-example predictions, seed traces, or bootstrap replicates. The plotting code therefore visualizes only those verified values. It does **not** synthesize histograms, raincloud distributions, qualitative camera/BEV cases, or confidence intervals. Exact numerical values remain available in `appendix_numeric_tables.tex`.

A future qualitative case figure should be added only after the selected WOD-E2E camera/BEV assets and per-item scores are checked into the project.

## Files

```text
experiment.tex
appendix_numeric_tables.tex
build_all_figures.py
plot_experiment_figures.py
plotting/
    style.py
    data.py
    plot_table4_native_channel.py
    plot_table5_semantic_regimes.py
    plot_table6_causal_interventions.py
figures/
    fig_native_scoring_channel.pdf/png
    fig_semantic_disagreement.pdf/png
    fig_causal_interventions.pdf/png
requirements.txt
.github/workflows/generate-figures.yml
MotionScorer_Experiment_Visuals.zip
```

## Regenerate locally

```bash
python -m pip install -r requirements.txt
python build_all_figures.py
```

`plot_experiment_figures.py` is retained as a backward-compatible wrapper around the modular build.

## Appendix tables

To retain the exact numerical versions of the visualized results:

```latex
\appendix
\input{appendix_numeric_tables.tex}
```
