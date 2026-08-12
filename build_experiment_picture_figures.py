#!/usr/bin/env python3
"""Build the MotionScorer experiment-picture package.

Outputs
-------
figure/experiment_picture/*.pdf
figure/experiment_picture/*.png
MotionScorer_Experiment_Picture.zip
"""

from __future__ import annotations

import shutil
import zipfile
from pathlib import Path

from plotting_picture.plot_table4_native import build as build_table4
from plotting_picture.plot_table5_semantic import build as build_table5
from plotting_picture.plot_table6_causal import build as build_table6


ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = ROOT / "figure" / "experiment_picture"
ZIP_PATH = ROOT / "MotionScorer_Experiment_Picture.zip"


def clean_output() -> None:
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def package() -> None:
    include_files = [
        ROOT / "experiment_picture.tex",
        ROOT / "build_experiment_picture_figures.py",
        ROOT / "requirements.txt",
        ROOT / "README_experiment_picture.md",
    ]
    include_files.extend(sorted((ROOT / "plotting_picture").glob("*.py")))
    include_files.extend(sorted(OUTPUT_DIR.glob("*.pdf")))
    include_files.extend(sorted(OUTPUT_DIR.glob("*.png")))

    if ZIP_PATH.exists():
        ZIP_PATH.unlink()

    with zipfile.ZipFile(ZIP_PATH, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in include_files:
            if path.exists():
                archive.write(path, path.relative_to(ROOT))


def main() -> None:
    clean_output()
    build_table4(OUTPUT_DIR)
    build_table5(OUTPUT_DIR)
    build_table6(OUTPUT_DIR)
    package()
    print(f"Generated figures: {OUTPUT_DIR}")
    print(f"Generated ZIP: {ZIP_PATH}")


if __name__ == "__main__":
    main()
