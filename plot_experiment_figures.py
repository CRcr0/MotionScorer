#!/usr/bin/env python3
"""Generate publication-quality MotionScorer experiment figures.

The script reproduces the measured-result visualizations corresponding to the
matched-fit comparison and the former numerical Tables 4--6.  It writes vector
PDFs and 600-dpi PNGs under ``figures/`` and then creates a root-level ZIP that
can be unpacked directly into the LaTeX project root.
"""

from __future__ import annotations

import math
import zipfile
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D


ROOT = Path(__file__).resolve().parent
FIG_DIR = ROOT / "figures"
ZIP_PATH = ROOT / "MotionScorer_Experiment_Visuals.zip"

COLORS = {
    "navy": "#102A43",
    "blue": "#174A7E",
    "teal": "#0B5D5E",
    "purple": "#542A7F",
    "maroon": "#7A1F3D",
    "red": "#8B1E1E",
    "orange": "#9A4A13",
    "brown": "#6F3B20",
    "charcoal": "#303742",
    "gray": "#59636E",
    "light_gray": "#D5DBE3",
    "black": "#101820",
    "white": "#FFFFFF",
}


def configure_style() -> None:
    """Use a white, grid-free, high-contrast paper style."""

    mpl.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 13.0,
            "font.weight": "semibold",
            "axes.labelsize": 15.0,
            "axes.labelweight": "bold",
            "axes.titlesize": 16.0,
            "axes.titleweight": "bold",
            "axes.linewidth": 2.2,
            "axes.edgecolor": COLORS["black"],
            "axes.facecolor": COLORS["white"],
            "figure.facecolor": COLORS["white"],
            "savefig.facecolor": COLORS["white"],
            "savefig.edgecolor": COLORS["white"],
            "xtick.labelsize": 12.5,
            "ytick.labelsize": 12.5,
            "xtick.major.width": 1.9,
            "ytick.major.width": 1.9,
            "xtick.major.size": 5.5,
            "ytick.major.size": 5.5,
            "legend.fontsize": 11.5,
            "legend.frameon": False,
            "lines.linewidth": 3.5,
            "lines.markersize": 11.0,
            "patch.linewidth": 2.0,
            "mathtext.fontset": "dejavusans",
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
        }
    )


def clean_axes(ax: plt.Axes) -> None:
    ax.grid(False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_linewidth(2.2)
    ax.spines["bottom"].set_linewidth(2.2)
    ax.tick_params(axis="both", which="both", direction="out")


def save_figure(fig: plt.Figure, stem: str) -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(
        FIG_DIR / f"{stem}.pdf",
        bbox_inches="tight",
        pad_inches=0.025,
        facecolor="white",
        transparent=False,
    )
    fig.savefig(
        FIG_DIR / f"{stem}.png",
        dpi=600,
        bbox_inches="tight",
        pad_inches=0.025,
        facecolor="white",
        transparent=False,
    )
    plt.close(fig)


def plot_matched_fit() -> None:
    data = [
        ("Fixed queries", 0.142, 0.712, 61.5, 0.86, 3.1, COLORS["charcoal"], "s"),
        ("Plain readout", 0.096, 0.888, 66.8, 0.89, 6.4, COLORS["blue"], "o"),
        ("Permuted TCD", 0.097, 0.885, 66.3, 0.89, 6.1, COLORS["orange"], "X"),
        ("Full-state TCD", 0.095, 0.889, 67.9, 0.90, 6.9, COLORS["teal"], "^"),
        ("LoRA scorer", 0.089, 0.901, 71.5, 0.92, None, COLORS["maroon"], "D"),
        ("nuGuidance", 0.095, 0.891, 70.3, 0.91, 8.7, COLORS["purple"], "*"),
    ]
    offsets = {
        "Fixed queries": (10, -20),
        "Plain readout": (10, -34),
        "Permuted TCD": (10, 13),
        "Full-state TCD": (-126, -18),
        "LoRA scorer": (-96, 15),
        "nuGuidance": (12, 20),
    }

    fig, ax = plt.subplots(figsize=(9.2, 5.4))
    for name, rmse, srcc, acc, ndcg, rho, color, marker in data:
        if rho is None:
            ax.scatter(
                rmse,
                acc,
                s=470,
                marker=marker,
                facecolors="white",
                edgecolors=color,
                linewidths=3.0,
                zorder=5,
            )
            rho_text = "n/a"
        else:
            ax.scatter(
                rmse,
                acc,
                s=145 + 49 * rho,
                marker=marker,
                color=color,
                edgecolors="white",
                linewidths=2.1,
                zorder=5,
            )
            rho_text = f"{rho:.1f}"

        dx, dy = offsets[name]
        ax.annotate(
            f"{name}\nSRCC={srcc:.3f}, NDCG={ndcg:.2f}, ρ={rho_text}",
            xy=(rmse, acc),
            xytext=(dx, dy),
            textcoords="offset points",
            ha="left",
            va="center",
            fontsize=10.8,
            fontweight="bold" if name == "nuGuidance" else "semibold",
            color=color,
            annotation_clip=False,
        )

    ax.annotate(
        "+3.5 pp at matched teacher fit",
        xy=(0.095, 70.05),
        xytext=(0.115, 69.25),
        fontsize=12.0,
        fontweight="bold",
        color=COLORS["purple"],
        arrowprops={
            "arrowstyle": "-|>",
            "lw": 3.0,
            "color": COLORS["purple"],
            "shrinkA": 5,
            "shrinkB": 7,
        },
    )

    ax.set_xlim(0.149, 0.086)
    ax.set_ylim(59.5, 73.0)
    ax.set_xlabel("Pseudo-validation RMSE  (lower is better →)")
    ax.set_ylabel("WOD-E2E pairwise accuracy (%)")
    clean_axes(ax)
    save_figure(fig, "fig_matched_fit_readout")


def plot_native_channel() -> None:
    data = [
        ("Direct scalar", 1.94, 54.2, 0.81, 6.2, 93.5, COLORS["brown"], "s"),
        ("Analyze → score", 1.41, 57.6, 0.83, 11.4, 96.8, COLORS["orange"], "^"),
        ("Prompt ensemble", 0.62, 56.9, 0.83, 23.7, 99.2, COLORS["maroon"], "D"),
        ("Self-consistency", 0.88, 57.1, 0.83, 18.9, 99.0, COLORS["red"], "P"),
        ("Plain readout", 0.11, 66.8, 0.89, 287.0, 100.0, COLORS["blue"], "o"),
        ("nuGuidance", 0.09, 70.3, 0.91, 341.0, 100.0, COLORS["purple"], "*"),
    ]
    offsets = {
        "Direct scalar": (10, -21),
        "Analyze → score": (10, 18),
        "Prompt ensemble": (-137, -22),
        "Self-consistency": (10, 16),
        "Plain readout": (-137, -31),
        "nuGuidance": (-134, 21),
    }

    fig, ax = plt.subplots(figsize=(9.4, 5.4))
    for name, sens, acc, ndcg, neff, valid, color, marker in data:
        size = 125 + 29 * math.sqrt(neff)
        ax.scatter(
            sens,
            acc,
            s=size,
            marker=marker,
            color=color,
            edgecolors="white",
            linewidths=2.1,
            zorder=5,
        )
        dx, dy = offsets[name]
        ax.annotate(
            f"{name}\nN_eff={neff:g}, NDCG={ndcg:.2f}, valid={valid:.1f}%",
            xy=(sens, acc),
            xytext=(dx, dy),
            textcoords="offset points",
            ha="left",
            va="center",
            fontsize=10.7,
            fontweight="bold" if name == "nuGuidance" else "semibold",
            color=color,
            annotation_clip=False,
        )

    ax.set_xscale("log")
    ax.set_xlim(2.55, 0.065)
    ax.set_ylim(52.0, 72.4)
    ax.set_xlabel("Prompt sensitivity  (lower is better →; reversed log scale)")
    ax.set_ylabel("WOD-E2E pairwise accuracy (%)")
    ax.text(1.35, 71.1, "Native textual channel", color=COLORS["brown"], fontsize=12.2, fontweight="bold", ha="center")
    ax.text(0.103, 71.8, "Frozen learned readout", color=COLORS["purple"], fontsize=12.2, fontweight="bold", ha="center")
    clean_axes(ax)
    save_figure(fig, "fig_native_scoring_channel")


def plot_semantic_regimes() -> None:
    data = [
        ("Aggregated EPDMS", 2.95, 1.72, 4.31, 3.88, None, 4.31),
        ("Scheme-B teacher", 2.78, 1.58, 3.42, 3.95, None, 3.95),
        ("Direct prompting", 2.92, 2.60, 3.05, 3.30, 49.8, 3.30),
        ("Plain readout", 2.31, 1.66, 2.88, 3.41, 52.4, 3.41),
        ("LoRA scorer", 2.02, 1.49, 2.51, 3.02, 56.1, 3.02),
        ("nuGuidance", 2.10, 1.61, 2.42, 2.79, 60.7, 2.79),
    ]
    metric_specs = [
        ("Overall", 1, "o", COLORS["navy"], 0.19),
        ("Teacher–human agreement", 2, "D", COLORS["gray"], 0.065),
        ("Rule over-penalty", 3, "s", COLORS["orange"], -0.065),
        ("Rule-pass blind spot", 4, "^", COLORS["red"], -0.19),
    ]

    fig, ax = plt.subplots(figsize=(10.8, 6.0))
    y_positions = list(reversed(range(len(data))))

    for y, row in zip(y_positions, data):
        name = row[0]
        values = row[1:5]
        ax.hlines(y, min(values), max(values), color=COLORS["light_gray"], linewidth=6.0, zorder=1)
        if name == "nuGuidance":
            ax.axhspan(y - 0.35, y + 0.35, color=COLORS["purple"], alpha=0.06, zorder=0)

        for _, value_index, marker, color, offset in metric_specs:
            ax.scatter(
                row[value_index],
                y + offset,
                s=150,
                marker=marker,
                color=color,
                edgecolors="white",
                linewidths=1.9,
                zorder=4,
            )

        trans, worst = row[5], row[6]
        right_text = f"worst={worst:.2f}" if trans is None else f"T={trans:.1f}%   |   worst={worst:.2f}"
        ax.text(
            4.53,
            y,
            right_text,
            fontsize=11.0,
            va="center",
            ha="left",
            color=COLORS["purple"] if name == "nuGuidance" else COLORS["charcoal"],
            fontweight="bold" if name == "nuGuidance" else "semibold",
        )

    ax.set_yticks(y_positions)
    ax.set_yticklabels([row[0] for row in data])
    for tick, row in zip(ax.get_yticklabels(), data):
        if row[0] == "nuGuidance":
            tick.set_fontweight("bold")
            tick.set_color(COLORS["purple"])

    handles = [
        Line2D([0], [0], marker=marker, color="none", markerfacecolor=color, markeredgecolor="white", markeredgewidth=1.5, markersize=10.5, label=label)
        for label, _, marker, color, _ in metric_specs
    ]
    ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.47, 1.13), ncol=4, columnspacing=1.15, handletextpad=0.4)
    ax.set_xlim(1.25, 5.18)
    ax.set_ylim(-0.55, len(data) - 0.45)
    ax.set_xlabel("Fixed-scale MAE on the WOD-E2E 0–10 human scale  (lower is better →)")
    clean_axes(ax)
    save_figure(fig, "fig_semantic_disagreement")


def plot_causal_interventions() -> None:
    data = [
        ("Learned attention, unchanged", 0.0, 70.3, 0.91, 8.7, COLORS["navy"], "o"),
        ("Uniform context attention", -9.4, 60.9, 0.85, 1.2, COLORS["red"], "s"),
        ("Suppress top-attended mass", -8.5, 61.8, 0.86, 2.6, COLORS["maroon"], "X"),
        ("Suppress equal mass at random", -1.4, 68.9, 0.90, 7.9, COLORS["teal"], "D"),
        ("Shuffle attention within modality", -5.2, 65.1, 0.88, 4.8, COLORS["orange"], "^"),
    ]

    fig, ax = plt.subplots(figsize=(10.1, 5.25))
    y_positions = list(reversed(range(len(data))))
    ax.axvline(0, color=COLORS["black"], linewidth=2.3, zorder=1)

    for y, (name, delta, acc, ndcg, rho, color, marker) in zip(y_positions, data):
        ax.hlines(y, min(0.0, delta), max(0.0, delta), color=color, linewidth=8.0, alpha=0.94, zorder=2)
        ax.scatter(delta, y, s=245, marker=marker, color=color, edgecolors="white", linewidths=2.1, zorder=4)
        ax.text(
            0.55,
            y,
            f"Acc={acc:.1f}%   |   NDCG={ndcg:.2f}   |   ρ={rho:.1f}",
            va="center",
            ha="left",
            fontsize=11.0,
            color=COLORS["charcoal"],
            fontweight="bold" if name == "Learned attention, unchanged" else "semibold",
        )
        if delta < 0:
            ax.text(delta - 0.22, y, f"{delta:.1f}", va="center", ha="right", fontsize=11.2, color=color, fontweight="bold")

    ax.set_yticks(y_positions)
    ax.set_yticklabels([row[0] for row in data])
    ax.set_xlim(-10.7, 4.55)
    ax.set_ylim(-0.55, len(data) - 0.45)
    ax.set_xlabel("Change in WOD-E2E pairwise accuracy (percentage points; 0 = unchanged)")
    clean_axes(ax)
    save_figure(fig, "fig_causal_interventions")


def make_zip() -> None:
    include = [
        ROOT / "experiment.tex",
        ROOT / "appendix_numeric_tables.tex",
        ROOT / "plot_experiment_figures.py",
        ROOT / "requirements.txt",
        ROOT / "README.md",
    ]
    include.extend(sorted(FIG_DIR.glob("*.pdf")))
    include.extend(sorted(FIG_DIR.glob("*.png")))

    if ZIP_PATH.exists():
        ZIP_PATH.unlink()
    with zipfile.ZipFile(ZIP_PATH, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in include:
            if path.exists():
                archive.write(path, path.relative_to(ROOT))


def main() -> None:
    configure_style()
    plot_matched_fit()
    plot_native_channel()
    plot_semantic_regimes()
    plot_causal_interventions()
    make_zip()
    print(f"Generated figures in {FIG_DIR}")
    print(f"Generated package {ZIP_PATH}")


if __name__ == "__main__":
    main()
