"""Figures for causal attention-readout interventions (former Table 6)."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from plotting_picture.data import DELTA_PAIR_ACC, DELTA_RHO_TCD, INTERVENTIONS
from plotting_picture.style import COLORS, clean_axes, configure_style, save_figure


INTERVENTION_COLORS = [
    COLORS["uniform"],
    COLORS["top"],
    COLORS["random"],
    COLORS["shuffle"],
]


def _negative_bar_chart(
    output_dir: Path,
    *,
    values: list[float],
    stem: str,
    title: str,
    ylabel: str,
    ylim: tuple[float, float],
    top_random_gap: float,
    gap_label: str,
) -> None:
    configure_style()

    x = np.arange(len(INTERVENTIONS))
    arr = np.asarray(values)
    fig, ax = plt.subplots(figsize=(7.35, 4.15))

    bars = ax.bar(
        x,
        arr,
        width=0.66,
        color=INTERVENTION_COLORS,
        edgecolor=COLORS["black"],
        linewidth=1.25,
        zorder=3,
    )
    ax.axhline(0.0, color=COLORS["black"], linewidth=2.1, zorder=1)

    for bar, value, color in zip(bars, arr, INTERVENTION_COLORS):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value - 0.28,
            f"{value:.1f}",
            ha="center",
            va="top",
            fontsize=11.0,
            fontweight="bold",
            color=color,
        )

    # Directly expose the decisive top-attended versus equal-mass-random contrast.
    top_x, random_x = 1, 2
    top_y, random_y = arr[top_x], arr[random_x]
    ax.annotate(
        "",
        xy=(random_x - 0.05, random_y),
        xytext=(top_x + 0.05, top_y),
        arrowprops={
            "arrowstyle": "<->",
            "lw": 2.4,
            "color": COLORS["ours"],
            "shrinkA": 4,
            "shrinkB": 4,
        },
    )
    ax.text(
        1.48,
        (top_y + random_y) / 2,
        f"{gap_label}\n{top_random_gap:.1f}",
        ha="center",
        va="center",
        fontsize=10.7,
        fontweight="bold",
        color=COLORS["ours"],
        bbox={
            "boxstyle": "round,pad=0.24",
            "facecolor": "white",
            "edgecolor": COLORS["ours"],
            "linewidth": 1.5,
        },
    )

    ax.set_xticks(x)
    ax.set_xticklabels(INTERVENTIONS)
    ax.set_ylabel(ylabel)
    ax.set_ylim(*ylim)
    ax.set_title(title)
    clean_axes(ax)
    fig.tight_layout(pad=0.28)
    save_figure(fig, output_dir, stem)


def plot_delta_pair_accuracy(output_dir: Path) -> None:
    _negative_bar_chart(
        output_dir,
        values=DELTA_PAIR_ACC,
        stem="fig6a_delta_pairwise_accuracy",
        title="(a) Human-alignment degradation",
        ylabel=r"$\Delta$ Pairwise accuracy (pp)",
        ylim=(-10.7, 0.75),
        top_random_gap=abs(DELTA_PAIR_ACC[1] - DELTA_PAIR_ACC[2]),
        gap_label="Top vs. random",
    )


def plot_delta_rho(output_dir: Path) -> None:
    _negative_bar_chart(
        output_dir,
        values=DELTA_RHO_TCD,
        stem="fig6b_delta_rho_tcd",
        title="(b) Deflection-statistic degradation",
        ylabel=r"$\Delta\rho_{\mathrm{TCD}}$",
        ylim=(-8.4, 0.65),
        top_random_gap=abs(DELTA_RHO_TCD[1] - DELTA_RHO_TCD[2]),
        gap_label="Top vs. random",
    )


def build(output_dir: Path) -> None:
    plot_delta_pair_accuracy(output_dir)
    plot_delta_rho(output_dir)


if __name__ == "__main__":
    build(Path("figure/experiment_picture"))
