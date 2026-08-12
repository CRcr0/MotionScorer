"""Figures for the native-scoring-channel comparison (former Table 4)."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from plotting_picture.data import (
    NATIVE_METHODS,
    NATIVE_N_EFF,
    NATIVE_PAIR_ACC,
    NATIVE_SENSITIVITY,
)
from plotting_picture.style import COLORS, clean_axes, configure_style, save_figure


BAR_COLORS = [
    COLORS["direct"],
    COLORS["analyze"],
    COLORS["ensemble"],
    COLORS["self_consistency"],
    COLORS["plain"],
    COLORS["ours"],
]


def _group_divider(ax: plt.Axes, y_text: float) -> None:
    """Mark the transition from textual prompting to learned readout."""

    ax.axvline(3.5, color=COLORS["black"], linewidth=1.4, linestyle=(0, (4, 3)))
    ax.text(
        1.5,
        y_text,
        "Native language channel",
        ha="center",
        va="bottom",
        fontsize=10.5,
        fontweight="bold",
        color=COLORS["direct"],
    )
    ax.text(
        4.5,
        y_text,
        "Frozen learned readout",
        ha="center",
        va="bottom",
        fontsize=10.5,
        fontweight="bold",
        color=COLORS["ours"],
    )


def plot_pairwise_accuracy(output_dir: Path) -> None:
    configure_style()
    x = np.arange(len(NATIVE_METHODS))
    values = np.asarray(NATIVE_PAIR_ACC)

    fig, ax = plt.subplots(figsize=(7.25, 4.15))
    bars = ax.bar(
        x,
        values,
        width=0.68,
        color=BAR_COLORS,
        edgecolor=COLORS["black"],
        linewidth=1.25,
        zorder=3,
    )

    best_prompt = max(values[:4])
    ax.axhline(
        best_prompt,
        color=COLORS["direct"],
        linewidth=2.0,
        linestyle=(0, (5, 3)),
        zorder=1,
    )
    ax.text(
        -0.43,
        best_prompt + 0.35,
        f"Best prompting: {best_prompt:.1f}",
        fontsize=9.8,
        fontweight="bold",
        color=COLORS["direct"],
        ha="left",
    )

    for bar, value in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + 0.45,
            f"{value:.1f}",
            ha="center",
            va="bottom",
            fontsize=10.5,
            fontweight="bold",
            color=COLORS["black"],
        )

    ax.annotate(
        "+12.7 pp",
        xy=(5, values[5]),
        xytext=(4.18, 61.5),
        fontsize=12.0,
        fontweight="bold",
        color=COLORS["ours"],
        arrowprops={
            "arrowstyle": "-|>",
            "lw": 2.5,
            "color": COLORS["ours"],
            "shrinkA": 4,
            "shrinkB": 5,
        },
    )

    ax.set_xticks(x)
    ax.set_xticklabels(NATIVE_METHODS)
    ax.set_ylabel("Pairwise accuracy (%)")
    ax.set_ylim(50.0, 73.8)
    ax.set_title("(a) Human-aligned scoring")
    clean_axes(ax)
    fig.tight_layout(pad=0.25)
    save_figure(fig, output_dir, "fig4a_pairwise_accuracy")


def plot_effective_levels(output_dir: Path) -> None:
    configure_style()
    x = np.arange(len(NATIVE_METHODS))
    values = np.asarray(NATIVE_N_EFF)

    fig, ax = plt.subplots(figsize=(7.25, 4.15))

    ax.plot(
        x[:4],
        values[:4],
        color=COLORS["analyze"],
        marker="o",
        markerfacecolor=COLORS["analyze"],
        markeredgecolor="white",
        markeredgewidth=1.5,
        linewidth=3.1,
        zorder=4,
    )
    ax.plot(
        x[3:5],
        values[3:5],
        color=COLORS["light"],
        linewidth=2.2,
        linestyle=(0, (4, 3)),
        zorder=2,
    )
    ax.plot(
        x[4:],
        values[4:],
        color=COLORS["ours"],
        marker="s",
        markerfacecolor=COLORS["ours"],
        markeredgecolor="white",
        markeredgewidth=1.5,
        linewidth=3.1,
        zorder=4,
    )

    for idx, value in enumerate(values):
        ax.text(
            idx,
            value * (1.18 if idx < 4 else 1.10),
            f"{value:g}",
            ha="center",
            va="bottom",
            fontsize=10.2,
            fontweight="bold",
            color=BAR_COLORS[idx],
        )

    ratio = values[-1] / max(values[:4])
    ax.annotate(
        f"{ratio:.1f}× vs. best prompting",
        xy=(5, values[-1]),
        xytext=(3.65, 92),
        fontsize=11.2,
        fontweight="bold",
        color=COLORS["ours"],
        arrowprops={
            "arrowstyle": "-|>",
            "lw": 2.3,
            "color": COLORS["ours"],
            "shrinkA": 4,
            "shrinkB": 5,
        },
    )

    ax.set_yscale("log")
    ax.set_ylim(4.0, 620.0)
    ax.set_xticks(x)
    ax.set_xticklabels(NATIVE_METHODS)
    ax.set_ylabel(r"Effective score levels $N_{\mathrm{eff}}$")
    ax.set_title("(b) Score resolution")
    _group_divider(ax, 510.0)
    clean_axes(ax)
    fig.tight_layout(pad=0.25)
    save_figure(fig, output_dir, "fig4b_effective_levels")


def plot_prompt_sensitivity(output_dir: Path) -> None:
    configure_style()
    x = np.arange(len(NATIVE_METHODS))
    values = np.asarray(NATIVE_SENSITIVITY)

    fig, ax = plt.subplots(figsize=(7.25, 4.15))

    ax.plot(
        x[:4],
        values[:4],
        color=COLORS["analyze"],
        marker="o",
        markerfacecolor=COLORS["analyze"],
        markeredgecolor="white",
        markeredgewidth=1.5,
        linewidth=3.1,
        zorder=4,
    )
    ax.plot(
        x[3:5],
        values[3:5],
        color=COLORS["light"],
        linewidth=2.2,
        linestyle=(0, (4, 3)),
        zorder=2,
    )
    ax.plot(
        x[4:],
        values[4:],
        color=COLORS["ours"],
        marker="s",
        markerfacecolor=COLORS["ours"],
        markeredgecolor="white",
        markeredgewidth=1.5,
        linewidth=3.1,
        zorder=4,
    )

    for idx, value in enumerate(values):
        offset = 0.10 if idx < 4 else 0.075
        ax.text(
            idx,
            value + offset,
            f"{value:.2f}",
            ha="center",
            va="bottom",
            fontsize=10.2,
            fontweight="bold",
            color=BAR_COLORS[idx],
        )

    best_prompt = min(values[:4])
    reduction = 100.0 * (1.0 - values[-1] / best_prompt)
    ax.annotate(
        f"{reduction:.1f}% lower than\nbest prompting",
        xy=(5, values[-1]),
        xytext=(3.80, 0.55),
        fontsize=11.2,
        fontweight="bold",
        color=COLORS["ours"],
        arrowprops={
            "arrowstyle": "-|>",
            "lw": 2.3,
            "color": COLORS["ours"],
            "shrinkA": 4,
            "shrinkB": 5,
        },
    )

    ax.set_ylim(0.0, 2.28)
    ax.set_xticks(x)
    ax.set_xticklabels(NATIVE_METHODS)
    ax.set_ylabel("Prompt sensitivity (lower is better)")
    ax.set_title("(c) Output stability")
    _group_divider(ax, 2.08)
    clean_axes(ax)
    fig.tight_layout(pad=0.25)
    save_figure(fig, output_dir, "fig4c_prompt_sensitivity")


def build(output_dir: Path) -> None:
    plot_pairwise_accuracy(output_dir)
    plot_effective_levels(output_dir)
    plot_prompt_sensitivity(output_dir)


if __name__ == "__main__":
    build(Path("figure/experiment_picture"))
