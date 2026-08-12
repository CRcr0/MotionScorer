# MotionScorer Experiment Picture Package

This package replaces the old Table 4--6 visualizations with separate paper-style bar and line figures. Table 2 and Table 3 remain unchanged in the existing experiment source.

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

## Final figure design

### Native scoring channel

- `fig4a_pairwise_accuracy.pdf/png`: horizontal accuracy bars anchored at the 50% chance reference, with the `+12.7 pp` native-channel gap stated directly.
- `fig4b_effective_levels.pdf/png`: line chart of effective score levels on a logarithmic scale, highlighting the `14.4x` resolution gain.
- `fig4c_prompt_sensitivity.pdf/png`: line chart of prompt sensitivity on a logarithmic scale, highlighting the `85.5%` reduction.

### Semantic disagreement regimes

- `fig5a_regime_grouped_bars.pdf/png`: grouped MAE bars across agreement, rule over-penalty, and rule-pass blind-spot regimes.
- `fig5b_error_profile_line.pdf/png`: line chart tracing each method from overall error to the hard semantic regimes.
- `fig5c_transcend_rate.pdf/png`: horizontal bars anchored at the 50% teacher-parity reference, with the `+8.3 pp` gain over the plain readout stated directly.

### Causal interventions

- `fig6a_delta_pairwise_accuracy.pdf/png`: horizontal negative-effect bars with the `7.1 pp` top-attended versus equal-mass-random contrast stated directly.
- `fig6b_delta_rho_tcd.pdf/png`: matching horizontal bars for the internal deflection statistic, with the `5.3` contrast stated directly.

All figures use a pure white background, no grid, deep high-contrast colors, thick axes and bars, large semibold text, and tightly cropped PDF/PNG output.

## Rebuild locally

```bash
python -m pip install -r requirements.txt
python build_experiment_picture_figures.py
```

The builder creates editable vector PDFs, 600-dpi PNG previews, and `MotionScorer_Experiment_Picture.zip`.

## Data boundary

The repository currently contains verified summary statistics rather than per-example predictions. The figures therefore visualize only directly reported table quantities. They do not synthesize score histograms, per-seed clouds, confidence intervals, or residual distributions. Those can be added after the corresponding raw outputs are available.
