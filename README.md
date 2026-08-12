# MotionScorer Experiment Visualizations

This repository contains the drop-in experiment section and publication-quality visualizations for the MotionScorer / nuGuidance paper.

## Drop-in use

Copy the repository contents into the LaTeX project root and include:

```latex
\input{experiment.tex}
```

The experiment file expects the project to already load `graphicx`, `booktabs`, `amsmath`, and `xcolor`, and to define `\methodname{}` and the citation keys used by the paper.

## Main-text organization

- Table 2: public human-aligned trajectory scoring — retained as a table.
- Table 3: matched-fit readout comparison — retained as a table and supplemented by a measured-result visualization.
- Native scoring channel — rendered as a figure.
- Semantic disagreement regimes — rendered as a figure.
- Causal readout interventions — rendered as a figure.
- The former Table 7 adaptation-cost subsection remains in the paper appendix and is not duplicated here.

## Files

- `experiment.tex`: ready-to-input experiment section.
- `plot_experiment_figures.py`: regenerates all figures from the measured values.
- `figures/`: generated PDF and 600-dpi PNG figures.
- `appendix_numeric_tables.tex`: exact numerical tables corresponding to the main-text figures.
- `requirements.txt`: Python plotting dependency.
- `.github/workflows/generate-figures.yml`: regenerates and commits the figures and ZIP package on GitHub.
- `MotionScorer_Experiment_Visuals.zip`: generated root-level package for direct download after the workflow completes.

## Regenerate locally

```bash
python -m pip install -r requirements.txt
python plot_experiment_figures.py
```

The plotting style uses a pure white background, no grids, deep high-contrast colors, thick lines, large bold text, and tightly cropped output.
