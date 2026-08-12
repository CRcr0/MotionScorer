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

HORIZONTAL_LABELS = [
    "Direct scalar prompting",
    "Analyze-then-score",
    "Prompt ensemble",
    "Self-consistency",
    "Plain query readout",
    "nuGuidance",
]


def _group_divider(ax: plt.Axes) -> None:
    """Mark the transition from textual prompting to learned readout."""

    ax.axvline(3.5, color=COLORS["black"], linewidth=1.5, linestyle=(0, (4, 3)))
    ax.text(
        1.5,
        1.045,
        "Native language channel",
        transform=ax.get_xaxis_transform(),
        ha="center",
        va="bottom",
        fontsize=10.8,
        fontweight="bold",
        color=COLORS["direct"],
    )
    ax.text(
        4.5,
        1.045,
        "Frozen learned readout",
        transform=ax.get_xaxis_transform(),
        ha="center",
        va="bottom",
        fontsize=10.8,
        fontweight="bold",
        color=COLORS["ours"],
    )


def plot_pairwise_accuracy(output_dir: Path) -> None:
    """Horizontal bars anchored at the 50% chance level."""

    configure_style()
    values = np.asarray(NATIVE_PAIR_ACC, dtype=float)
    y = np.arange(len(values))

    fig, ax = plt.subplots(figsize=(9.4, 4.75))
    bars = ax.barh(
        y,
        values - 50.0,
        left=50.0,
        height=0.62,
        color=BAR_COLORS,
        edgecolor=COLORS["black"],
        linewidth=1.35,
        zorder=3,
    )

    ax.axvline(50.0, color=COLORS["black"], linewidth=2.1, zorder=1)
    ax.text(
        50.18,
        -0.62,
        "50% chance",
        ha="left",
        va="center",
        fontsize=10.0,
        fontweight="bold",
        color=COLORS["black"],
    )
    ax.axhline(3.5, color=COLORS["black"], linewidth=1.35, linestyle=(0, (4, 3)))

    for bar, value, color in zip(bars, values, BAR_COLORS):
        ax.text(
            value + 0.28,
            bar.get_y() + bar.get_height() / 2,
            f"{value:.1f}",
            ha="left",
            va="center",
            fontsize=11.2,
            fontweight="bold",
            color=color,
        )

    best_prompt_idx = int(np.argmax(values[:4]))
    best_prompt = values[best_prompt_idx]
    ax.text(
        best_prompt + 0.25,
        best_prompt_idx - 0.42,
        "Strongest native-channel baseline",
        ha="left",
        va="center",
        fontsize=10.4,
        fontweight="bold",
        color=COLORS["analyze"],
    )

    # Directly expose the main effect in the same visual language as a cost-reduction chart.
    arrow_y = 5.78
    ax.plot(
        [best_prompt, best_prompt],
        [best_prompt_idx + 0.28, arrow_y],
        color=COLORS["accent"],
        linewidth=2.1,
        linestyle=(0, (4, 3)),
        clip_on=False,
    )
    ax.plot(
        [values[-1], values[-1]],
        [5.28, arrow_y],
        color=COLORS["accent"],
        linewidth=2.1,
        linestyle=(0, (4, 3)),
        clip_on=False,
    )
    ax.annotate(
        "",
        xy=(values[-1], arrow_y),
        xytext=(best_prompt, arrow_y),
        arrowprops={
            "arrowstyle": "<->",
            "lw": 2.5,
            "color": COLORS["accent"],
            "shrinkA": 0,
            "shrinkB": 0,
        },
        annotation_clip=False,
    )
    ax.text(
        (best_prompt + values[-1]) / 2,
        6.07,
        "+12.7 pp over the strongest native-channel baseline",
        ha="center",
        va="center",
        fontsize=11.3,
        fontweight="bold",
        color=COLORS["accent"],
        clip_on=False,
    )

    ax.text(
        72.8,
        1.45,
        "Native language channel",
        ha="right",
        va="center",
        fontsize=10.6,
        fontweight="bold",
        color=COLORS["direct"],
    )
    ax.text(
        72.8,
        4.52,
        "Frozen learned readout",
        ha="right",
        va="center",
        fontsize=10.6,
        fontweight="bold",
        color=COLORS["ours"],
    )

    ax.set_yticks(y)
    ax.set_yticklabels(HORIZONTAL_LABELS)
    ax.set_xlim(49.7, 74.6)
    ax.set_ylim(6.35, -0.85)
    ax.set_xlabel("WOD-E2E pairwise accuracy (%)")
    ax.set_title("(a) Human-aligned scoring")
    clean_axes(ax)
    fig.subplots_adjust(left=0.255, right=0.985, top=0.88, bottom=0.20)
    save_figure(fig, output_dir, "fig4a_pairwise_accuracy")


def plot_effective_levels(output_dir: Path) -> None:
    configure_style()
    x = np.arange(len(NATIVE_METHODS))
    values = np.asarray(NATIVE_N_EFF, dtype=float)

    fig, ax = plt.subplots(figsize=(7.5, 4.15))

    ax.plot(
        x[:4],
        values[:4],
        color=COLORS["analyze"],
        marker="o",
        markerfacecolor=COLORS["analyze"],
        markeredgecolor="white",
        markeredgewidth=1.6,
        linewidth=3.2,
        zorder=4,
    )
    ax.plot(
        x[3:5],
        values[3:5],
        color=COLORS["mid"],
        linewidth=2.3,
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
        markeredgewidth=1.6,
        linewidth=3.2,
        zorder=4,
    )

    for idx, value in enumerate(values):
        ax.text(
            idx,
            value * (1.20 if idx < 4 else 1.10),
            f"{value:g}",
            ha="center",
            va="bottom",
            fontsize=10.4,
            fontweight="bold",
            color=BAR_COLORS[idx],
        )

    ratio = values[-1] / max(values[:4])
    ax.annotate(
        f"{ratio:.1f}× the resolution of\nthe best prompting control",
        xy=(5, values[-1]),
        xytext=(3.55, 82),
        fontsize=11.0,
        fontweight="bold",
        color=COLORS["ours"],
        arrowprops={
            "arrowstyle": "-|>",
            "lw": 2.4,
            "color": COLORS["ours"],
            "shrinkA": 4,
            "shrinkB": 5,
        },
    )

    ax.set_yscale("log")
    ax.set_ylim(4.0, 650.0)
    ax.set_xticks(x)
    ax.set_xticklabels(NATIVE_METHODS)
    ax.set_ylabel(r"Effective score levels $N_{\mathrm{eff}}$")
    ax.set_title("(b) Score resolution")
    _group_divider(ax)
    clean_axes(ax)
    fig.subplots_adjust(left=0.12, right=0.99, top=0.82, bottom=0.22)
    save_figure(fig, output_dir, "fig4b_effective_levels")


def plot_prompt_sensitivity(output_dir: Path) -> None:
    configure_style()
    x = np.arange(len(NATIVE_METHODS))
    values = np.asarray(NATIVE_SENSITIVITY, dtype=float)

    fig, ax = plt.subplots(figsize=(7.5, 4.15))

    ax.plot(
        x[:4],
        values[:4],
        color=COLORS["analyze"],
        marker="o",
        markerfacecolor=COLORS["analyze"],
        markeredgecolor="white",
        markeredgewidth=1.6,
        linewidth=3.2,
        zorder=4,
    )
    ax.plot(
        x[3:5],
        values[3:5],
        color=COLORS["mid"],
        linewidth=2.3,
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
        markeredgewidth=1.6,
        linewidth=3.2,
        zorder=4,
    )

    for idx, value in enumerate(values):
        ax.text(
            idx,
            value * 1.18,
            f"{value:.2f}",
            ha="center",
            va="bottom",
            fontsize=10.4,
            fontweight="bold",
            color=BAR_COLORS[idx],
        )

    best_prompt = min(values[:4])
    reduction = 100.0 * (1.0 - values[-1] / best_prompt)
    ax.annotate(
        f"{reduction:.1f}% lower sensitivity\nthan the best prompting control",
        xy=(5, values[-1]),
        xytext=(3.35, 0.34),
        fontsize=10.9,
        fontweight="bold",
        color=COLORS["ours"],
        arrowprops={
            "arrowstyle": "-|>",
            "lw": 2.4,
            "color": COLORS["ours"],
            "shrinkA": 4,
            "shrinkB": 5,
        },
    )

    ax.set_yscale("log")
    ax.set_ylim(0.065, 2.75)
    ax.set_xticks(x)
    ax.set_xticklabels(NATIVE_METHODS)
    ax.set_ylabel("Prompt sensitivity (lower is better)")
    ax.set_title("(c) Output stability")
    _group_divider(ax)
    clean_axes(ax)
    fig.subplots_adjust(left=0.13, right=0.99, top=0.82, bottom=0.22)
    save_figure(fig, output_dir, "fig4c_prompt_sensitivity")


def build(output_dir: Path) -> None:
    plot_pairwise_accuracy(output_dir)
    plot_effective_levels(output_dir)
    plot_prompt_sensitivity(output_dir)


if __name__ == "__main__":
    build(Path("figure/experiment_picture"))
