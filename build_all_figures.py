#!/usr/bin/env python3
"""Build Figures 4--6 and the drop-in LaTeX package."""

from __future__ import annotations

import zipfile
from pathlib import Path

from plotting.plot_table4_native_channel import make_figure as make_table4
from plotting.plot_table5_semantic_regimes import make_figure as make_table5
from plotting.plot_table6_causal_interventions import make_figure as make_table6
from plotting.style import FIGURE_DIR, ROOT


ZIP_PATH = ROOT / "MotionScorer_Experiment_Visuals.zip"
EXPECTED_STEMS = {
    "fig_native_scoring_channel",
    "fig_semantic_disagreement",
    "fig_causal_interventions",
}


def clean_stale_figures() -> None:
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    for path in FIGURE_DIR.iterdir():
        if path.suffix.lower() in {".pdf", ".png"}:
            path.unlink()


def make_package() -> None:
    if ZIP_PATH.exists():
        ZIP_PATH.unlink()

    include_paths = [
        ROOT / "experiment.tex",
        ROOT / "appendix_numeric_tables.tex",
        ROOT / "README.md",
        ROOT / "requirements.txt",
        ROOT / "build_all_figures.py",
        ROOT / "plot_experiment_figures.py",
    ]
    include_paths.extend(sorted((ROOT / "plotting").glob("*.py")))
    for stem in sorted(EXPECTED_STEMS):
        include_paths.append(FIGURE_DIR / f"{stem}.pdf")
        include_paths.append(FIGURE_DIR / f"{stem}.png")

    with zipfile.ZipFile(ZIP_PATH, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in include_paths:
            if path.exists():
                archive.write(path, path.relative_to(ROOT))


def main() -> None:
    clean_stale_figures()
    make_table4()
    make_table5()
    make_table6()
    make_package()
    print(f"Generated figures in: {FIGURE_DIR}")
    print(f"Generated package: {ZIP_PATH}")


if __name__ == "__main__":
    main()
