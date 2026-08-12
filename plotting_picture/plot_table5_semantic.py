"""Figures for semantic disagreement and teacher-error inheritance (former Table 5)."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from plotting_picture.data import (
    SEMANTIC_MAE,
    SEMANTIC_PROFILE,
    SEMANTIC_PROFILE_X,
    SEMANTIC_REGIMES,
    TRANSCEND_METHODS,
    TRANSCEND_RATE,
)
from plotting_picture.style import COLORS, clean_axes, configure_style, save_figure


METHOD_STYLE = {
    "EPDMS": (COLORS["epdms"], "o"),
    "Scheme-B teacher": (COLORS["teacher"], "s"),
    "Direct prompting": (COLORS["direct"], "P"),
    "Plain readout": (COLORS["plain"], "D"),
    "LoRA scorer": (COLORS["lora"], "^"),
    "nuGuidance": (COLORS["ours"], "*"),
}


def plot_regime_grouped_bars(output_dir: Path) -> None:
    """Grouped bars show how each method behaves across semantic subdistributions."""

    configure_style()

    method_order = [
        "EPDMS",
        "Scheme-B teacher",
        "Direct prompting",
        "Plain readout",
        "LoRA scorer",
        "nuGuidance",
    ]
    x = np.arange(len(SEMANTIC_REGIMES))
    width = 0.128
    offsets = (np.arange(len(method_order)) - (len(method_order) - 1) / 2) * width

    fig, ax = plt.subplots(figsize=(10.0, 4.75))

    for method_idx, method in enumerate(method_order):
        color, _ = METHOD_STYLE[method]
        values = np.asarray(SEMANTIC_MAE[method], dtype=float)
        bars = ax.bar(
            x + offsets[method_idx],
            values,
            width=width,
            color=color,
            edgecolor=COLORS["black"],
            linewidth=1.05,
            label=method,
            zorder=3,
        )
        for bar, value in zip(bars, values):
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                value + 0.055,
                f"{value:.2f}",
                ha="center",
                va="bottom",
                fontsize=8.3,
                fontweight="bold" if method == "nuGuidance" else "semibold",
                color=color,
            )

    ax.axvline(0.5, color=COLORS["black"], linewidth=1.45, linestyle=(0, (4, 3)))
    ax.text(
        0.0,
        4.60,
        "Teacher already aligned",
        ha="center",
        va="bottom",
        fontsize=10.5,
        fontweight="bold",
        color=COLORS["teacher"],
    )
    ax.text(
        1.5,
        4.60,
        "Teacher–human disagreement",
        ha="center",
        va="bottom",
        fontsize=10.5,
        fontweight="bold",
        color=COLORS["ours"],
    )

    ours_offset = offsets[-1]
    ax.annotate(
        "−1.00 vs. teacher\n(best on over-penalty)",
        xy=(1 + ours_offset, SEMANTIC_MAE["nuGuidance"][1]),
        xytext=(0.86, 3.55),
        fontsize=9.7,
        fontweight="bold",
        color=COLORS["ours"],
        ha="center",
        arrowprops={
            "arrowstyle": "-|>",
            "lw": 2.0,
            "color": COLORS["ours"],
            "shrinkA": 3,
            "shrinkB": 4,
        },
    )
    ax.annotate(
        "−1.16 vs. teacher\n(best on blind spots)",
        xy=(2 + ours_offset, SEMANTIC_MAE["nuGuidance"][2]),
        xytext=(2.26, 3.62),
        fontsize=9.7,
        fontweight="bold",
        color=COLORS["ours"],
        ha="center",
        arrowprops={
            "arrowstyle": "-|>",
            "lw": 2.0,
            "color": COLORS["ours"],
            "shrinkA": 3,
            "shrinkB": 4,
        },
    )

    ax.set_xticks(x)
    ax.set_xticklabels(SEMANTIC_REGIMES)
    ax.set_ylabel("MAE to human score (lower is better)")
    ax.set_ylim(0.0, 4.92)
    ax.set_title("(a) Error distribution across semantic regimes")
    ax.legend(
        loc="upper center",
        bbox_to_anchor=(0.5, 1.18),
        ncol=6,
        columnspacing=0.8,
        handlelength=1.25,
        handletextpad=0.35,
    )
    clean_axes(ax)
    fig.subplots_adjust(left=0.075, right=0.995, top=0.76, bottom=0.20)
    save_figure(fig, output_dir, "fig5a_regime_grouped_bars")


def plot_error_profile(output_dir: Path) -> None:
    configure_style()

    x = np.arange(len(SEMANTIC_PROFILE_X))
    method_order = [
        "EPDMS",
        "Scheme-B teacher",
        "Plain readout",
        "LoRA scorer",
        "nuGuidance",
    ]

    fig, ax = plt.subplots(figsize=(8.1, 4.35))

    for method in method_order:
        color, marker = METHOD_STYLE[method]
        values = np.asarray(SEMANTIC_PROFILE[method], dtype=float)
        is_ours = method == "nuGuidance"
        ax.plot(
            x,
            values,
            color=color,
            marker=marker,
            linewidth=3.5 if is_ours else 2.7,
            markersize=10.5 if is_ours else 8.0,
            markerfacecolor=color,
            markeredgecolor="white",
            markeredgewidth=1.5,
            label=method,
            zorder=5 if is_ours else 3,
        )

        if method in {"Scheme-B teacher", "nuGuidance"}:
            for idx, value in enumerate(values):
                vertical = 0.10 if method == "Scheme-B teacher" else -0.17
                ax.text(
                    idx,
                    value + vertical,
                    f"{value:.2f}",
                    ha="center",
                    va="bottom" if vertical > 0 else "top",
                    fontsize=9.2,
                    fontweight="bold",
                    color=color,
                )

    ax.axvline(1.5, color=COLORS["black"], linewidth=1.45, linestyle=(0, (4, 3)))
    ax.text(
        0.5,
        4.48,
        "Nominal / agreement",
        ha="center",
        va="bottom",
        fontsize=10.2,
        fontweight="bold",
        color=COLORS["teacher"],
    )
    ax.text(
        2.5,
        4.48,
        "Semantic disagreement",
        ha="center",
        va="bottom",
        fontsize=10.2,
        fontweight="bold",
        color=COLORS["ours"],
    )

    ax.annotate(
        "−1.00 vs. teacher",
        xy=(2, SEMANTIC_PROFILE["nuGuidance"][2]),
        xytext=(2.25, 3.18),
        fontsize=10.8,
        fontweight="bold",
        color=COLORS["ours"],
        arrowprops={
            "arrowstyle": "-|>",
            "lw": 2.1,
            "color": COLORS["ours"],
            "shrinkA": 3,
            "shrinkB": 4,
        },
    )
    ax.annotate(
        "−1.16 vs. teacher",
        xy=(3, SEMANTIC_PROFILE["nuGuidance"][3]),
        xytext=(2.53, 3.68),
        fontsize=10.8,
        fontweight="bold",
        color=COLORS["ours"],
        arrowprops={
            "arrowstyle": "-|>",
            "lw": 2.1,
            "color": COLORS["ours"],
            "shrinkA": 3,
            "shrinkB": 4,
        },
    )

    ax.set_xticks(x)
    ax.set_xticklabels(SEMANTIC_PROFILE_X)
    ax.set_ylabel("MAE to human score")
    ax.set_ylim(1.25, 4.65)
    ax.set_title("(b) Error profile from nominal to hard regimes")
    ax.legend(
        loc="upper center",
        bbox_to_anchor=(0.5, 1.18),
        ncol=5,
        columnspacing=0.8,
        handlelength=1.55,
        handletextpad=0.35,
    )
    clean_axes(ax)
    fig.subplots_adjust(left=0.10, right=0.99, top=0.76, bottom=0.20)
    save_figure(fig, output_dir, "fig5b_error_profile_line")


def plot_transcend_rate(output_dir: Path) -> None:
    """Horizontal bars are anchored at 50%, the teacher-parity reference."""

    configure_style()

    values = np.asarray(TRANSCEND_RATE, dtype=float)
    labels = ["Direct prompting", "Plain readout", "LoRA scorer", "nuGuidance"]
    colors = [COLORS["direct"], COLORS["plain"], COLORS["lora"], COLORS["ours"]]
    y = np.arange(len(labels))

    fig, ax = plt.subplots(figsize=(8.45, 4.55))
    bars = ax.barh(
        y,
        values - 50.0,
        left=50.0,
        height=0.62,
        color=colors,
        edgecolor=COLORS["black"],
        linewidth=1.35,
        zorder=3,
    )

    ax.axvline(50.0, color=COLORS["black"], linewidth=2.1, linestyle=(0, (5, 3)), zorder=1)
    ax.text(
        50.18,
        -0.58,
        "50% = teacher parity",
        ha="left",
        va="center",
        fontsize=10.0,
        fontweight="bold",
        color=COLORS["black"],
    )

    for bar, value, color in zip(bars, values, colors):
        x_text = value + 0.25 if value >= 50.0 else value - 0.25
        ax.text(
            x_text,
            bar.get_y() + bar.get_height() / 2,
            f"{value:.1f}",
            ha="left" if value >= 50.0 else "right",
            va="center",
            fontsize=11.2,
            fontweight="bold",
            color=color,
        )

    ax.text(
        55.25,
        3.0,
        "Most often closer to human\nthan the automatic teacher",
        ha="center",
        va="center",
        fontsize=9.7,
        fontweight="bold",
        color="white",
    )

    plain_value = values[1]
    ours_value = values[3]
    arrow_y = 4.10
    ax.plot(
        [plain_value, plain_value],
        [1.28, arrow_y],
        color=COLORS["accent"],
        linewidth=2.0,
        linestyle=(0, (4, 3)),
        clip_on=False,
    )
    ax.plot(
        [ours_value, ours_value],
        [3.28, arrow_y],
        color=COLORS["accent"],
        linewidth=2.0,
        linestyle=(0, (4, 3)),
        clip_on=False,
    )
    ax.annotate(
        "",
        xy=(ours_value, arrow_y),
        xytext=(plain_value, arrow_y),
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
        (plain_value + ours_value) / 2,
        4.43,
        "+8.3 pp over the plain query readout",
        ha="center",
        va="center",
        fontsize=11.2,
        fontweight="bold",
        color=COLORS["accent"],
        clip_on=False,
    )

    ax.set_yticks(y)
    ax.set_yticklabels(labels)
    ax.set_xlim(47.4, 65.0)
    ax.set_ylim(4.72, -0.80)
    ax.set_xlabel("TranscendRate (%)")
    ax.set_title("(c) Correction of teacher-error items")
    clean_axes(ax)
    fig.subplots_adjust(left=0.24, right=0.985, top=0.86, bottom=0.21)
    save_figure(fig, output_dir, "fig5c_transcend_rate")


def build(output_dir: Path) -> None:
    plot_regime_grouped_bars(output_dir)
    plot_error_profile(output_dir)
    plot_transcend_rate(output_dir)


if __name__ == "__main__":
    build(Path("figure/experiment_picture"))
