"""Figures for causal attention-readout interventions (former Table 6)."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from plotting_picture.data import DELTA_PAIR_ACC, DELTA_RHO_TCD
from plotting_picture.style import COLORS, clean_axes, configure_style, save_figure


INTERVENTION_LABELS = [
    "Uniform context attention",
    "Suppress top-attended mass",
    "Suppress equal mass at random",
    "Shuffle attention within modality",
]

INTERVENTION_COLORS = [
    COLORS["uniform"],
    COLORS["top"],
    COLORS["random"],
    COLORS["shuffle"],
]


def _horizontal_effect_chart(
    output_dir: Path,
    *,
    values: list[float],
    stem: str,
    title: str,
    xlabel: str,
    xlim: tuple[float, float],
    gap_text: str,
    mechanism_note: str,
) -> None:
    """Draw negative intervention effects and expose the top-vs-random contrast."""

    configure_style()

    arr = np.asarray(values, dtype=float)
    y = np.arange(len(arr))
    fig, ax = plt.subplots(figsize=(9.35, 4.85))

    bars = ax.barh(
        y,
        arr,
        height=0.62,
        color=INTERVENTION_COLORS,
        edgecolor=COLORS["black"],
        linewidth=1.35,
        zorder=3,
    )
    ax.axvline(0.0, color=COLORS["black"], linewidth=2.2, zorder=1)
    ax.text(
        0.12,
        -0.58,
        "Unchanged readout",
        ha="left",
        va="center",
        fontsize=10.0,
        fontweight="bold",
        color=COLORS["black"],
    )

    for bar, value, color in zip(bars, arr, INTERVENTION_COLORS):
        ax.text(
            value - 0.22,
            bar.get_y() + bar.get_height() / 2,
            f"{value:.1f}",
            ha="right",
            va="center",
            fontsize=11.3,
            fontweight="bold",
            color=color,
        )

    ax.text(
        arr[0] + 0.35,
        0,
        "All selectivity removed",
        ha="left",
        va="center",
        fontsize=9.8,
        fontweight="bold",
        color="white",
    )
    ax.text(
        arr[1] + 0.35,
        1,
        mechanism_note,
        ha="left",
        va="center",
        fontsize=9.8,
        fontweight="bold",
        color="white",
    )

    # Comparison annotation in the style of a directly stated cost reduction.
    top_value = arr[1]
    random_value = arr[2]
    arrow_y = 4.12
    ax.plot(
        [top_value, top_value],
        [1.28, arrow_y],
        color=COLORS["accent"],
        linewidth=2.1,
        linestyle=(0, (4, 3)),
        clip_on=False,
    )
    ax.plot(
        [random_value, random_value],
        [2.28, arrow_y],
        color=COLORS["accent"],
        linewidth=2.1,
        linestyle=(0, (4, 3)),
        clip_on=False,
    )
    ax.annotate(
        "",
        xy=(random_value, arrow_y),
        xytext=(top_value, arrow_y),
        arrowprops={
            "arrowstyle": "<->",
            "lw": 2.6,
            "color": COLORS["accent"],
            "shrinkA": 0,
            "shrinkB": 0,
        },
        annotation_clip=False,
    )
    ax.text(
        (top_value + random_value) / 2,
        4.47,
        gap_text,
        ha="center",
        va="center",
        fontsize=11.2,
        fontweight="bold",
        color=COLORS["accent"],
        clip_on=False,
    )

    ax.set_yticks(y)
    ax.set_yticklabels(INTERVENTION_LABELS)
    ax.set_xlim(*xlim)
    ax.set_ylim(4.78, -0.82)
    ax.set_xlabel(xlabel)
    ax.set_title(title)
    clean_axes(ax)
    fig.subplots_adjust(left=0.31, right=0.985, top=0.86, bottom=0.20)
    save_figure(fig, output_dir, stem)


def plot_delta_pair_accuracy(output_dir: Path) -> None:
    _horizontal_effect_chart(
        output_dir,
        values=DELTA_PAIR_ACC,
        stem="fig6a_delta_pairwise_accuracy",
        title="(a) Human-alignment degradation",
        xlabel=r"Change in WOD-E2E pairwise accuracy (percentage points)",
        xlim=(-11.0, 1.15),
        gap_text="Top-evidence removal causes a 7.1 pp larger drop than equal-mass random removal",
        mechanism_note="Largest targeted-evidence drop",
    )


def plot_delta_rho(output_dir: Path) -> None:
    _horizontal_effect_chart(
        output_dir,
        values=DELTA_RHO_TCD,
        stem="fig6b_delta_rho_tcd",
        title="(b) Deflection-statistic degradation",
        xlabel=r"Change in held-out $\rho_{\mathrm{TCD}}$",
        xlim=(-8.8, 1.05),
        gap_text="Top-evidence removal causes a 5.3 larger deflection drop than random removal",
        mechanism_note="Largest targeted-statistic drop",
    )


def build(output_dir: Path) -> None:
    plot_delta_pair_accuracy(output_dir)
    plot_delta_rho(output_dir)


if __name__ == "__main__":
    build(Path("figure/experiment_picture"))
