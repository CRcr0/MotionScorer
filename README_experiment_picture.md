# MotionScorer Experiment Picture Package

This package replaces the old Table 4--6 visualizations with separate, paper-style bar and line figures. Table 2 and Table 3 remain in the existing experiment source.

## Use in the LaTeX paper

Place the repository contents at the LaTeX project root and insert the following immediately after the existing Table 3 discussion:

```latex
\input{experiment_picture.tex}
```

The parent document only needs:

```latex
\usepackage{graphicx}
```

The TeX file references figures under:

```text
figure/experiment_picture/
```

## Generated figures

### Native scoring channel

- `fig4a_pairwise_accuracy.pdf/png`: Pairwise-accuracy bar chart.
- `fig4b_effective_levels.pdf/png`: Effective-score-level line chart.
- `fig4c_prompt_sensitivity.pdf/png`: Prompt-sensitivity line chart.

### Semantic disagreement regimes

- `fig5a_regime_grouped_bars.pdf/png`: Grouped MAE bars across semantic regimes.
- `fig5b_error_profile_line.pdf/png`: Error-profile line chart from nominal to hard regimes.
- `fig5c_transcend_rate.pdf/png`: TranscendRate bar chart.

### Causal interventions

- `fig6a_delta_pairwise_accuracy.pdf/png`: Accuracy-drop bars.
- `fig6b_delta_rho_tcd.pdf/png`: Deflection-drop bars.

## Rebuild locally

```bash
python -m pip install -r requirements.txt
python build_experiment_picture_figures.py
```

The builder creates editable vector PDFs, 600-dpi PNG previews, and `MotionScorer_Experiment_Picture.zip`.

## Data boundary

The repository currently contains verified summary statistics rather than per-example predictions. The figures therefore visualize only directly reported table quantities. They do not synthesize score histograms, per-seed clouds, confidence intervals, or residual distributions. Those can be added after the corresponding raw outputs are available.
