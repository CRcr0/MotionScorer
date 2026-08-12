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
    width = 0.125
    offsets = (np.arange(len(method_order)) - (len(method_order) - 1) / 2) * width

    fig, ax = plt.subplots(figsize=(8.7, 4.45))

    for method_idx, method in enumerate(method_order):
        color, _ = METHOD_STYLE[method]
        values = np.asarray(SEMANTIC_MAE[method])
        bars = ax.bar(
            x + offsets[method_idx],
            values,
            width=width,
            color=color,
            edgecolor=COLORS["black"],
            linewidth=1.0,
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
                rotation=90,
                fontsize=7.8,
                fontweight="bold" if method == "nuGuidance" else "semibold",
                color=color,
            )

    ax.axvline(0.5, color=COLORS["black"], linewidth=1.4, linestyle=(0, (4, 3)))
    ax.text(
        0.0,
        4.62,
        "Teacher already aligned",
        ha="center",
        va="bottom",
        fontsize=10.2,
        fontweight="bold",
        color=COLORS["teacher"],
    )
    ax.text(
        1.5,
        4.62,
        "Teacher–human disagreement",
        ha="center",
        va="bottom",
        fontsize=10.2,
        fontweight="bold",
        color=COLORS["ours"],
    )

    ax.set_xticks(x)
    ax.set_xticklabels(SEMANTIC_REGIMES)
    ax.set_ylabel("MAE to human score (lower is better)")
    ax.set_ylim(0.0, 4.9)
    ax.set_title("(a) Error distribution across semantic regimes")
    ax.legend(
        loc="upper center",
        bbox_to_anchor=(0.5, -0.19),
        ncol=3,
        columnspacing=1.1,
        handlelength=1.4,
        handletextpad=0.4,
    )
    clean_axes(ax)
    fig.subplots_adjust(left=0.085, right=0.995, top=0.84, bottom=0.31)
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

    fig, ax = plt.subplots(figsize=(8.0, 4.35))

    for method in method_order:
        color, marker = METHOD_STYLE[method]
        values = np.asarray(SEMANTIC_PROFILE[method])
        is_ours = method == "nuGuidance"
        ax.plot(
            x,
            values,
            color=color,
            marker=marker,
            linewidth=3.4 if is_ours else 2.6,
            markersize=10.0 if is_ours else 7.8,
            markerfacecolor=color,
            markeredgecolor="white",
            markeredgewidth=1.4,
            label=method,
            zorder=5 if is_ours else 3,
        )

        if method in {"Scheme-B teacher", "nuGuidance"}:
            for idx, value in enumerate(values):
                vertical = 0.10 if method == "Scheme-B teacher" else -0.18
                ax.text(
                    idx,
                    value + vertical,
                    f"{value:.2f}",
                    ha="center",
                    va="bottom" if vertical > 0 else "top",
                    fontsize=9.1,
                    fontweight="bold",
                    color=color,
                )

    ax.axvline(1.5, color=COLORS["black"], linewidth=1.4, linestyle=(0, (4, 3)))
    ax.annotate(
        "−1.00",
        xy=(2, SEMANTIC_PROFILE["nuGuidance"][2]),
        xytext=(2.25, 3.18),
        fontsize=10.8,
        fontweight="bold",
        color=COLORS["ours"],
        arrowprops={
            "arrowstyle": "-|>",
            "lw": 2.0,
            "color": COLORS["ours"],
            "shrinkA": 3,
            "shrinkB": 4,
        },
    )
    ax.annotate(
        "−1.16",
        xy=(3, SEMANTIC_PROFILE["nuGuidance"][3]),
        xytext=(2.58, 3.68),
        fontsize=10.8,
        fontweight="bold",
        color=COLORS["ours"],
        arrowprops={
            "arrowstyle": "-|>",
            "lw": 2.0,
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
        bbox_to_anchor=(0.5, -0.18),
        ncol=3,
        columnspacing=1.1,
        handlelength=1.6,
        handletextpad=0.4,
    )
    clean_axes(ax)
    fig.subplots_adjust(left=0.10, right=0.99, top=0.87, bottom=0.30)
    save_figure(fig, output_dir, "fig5b_error_profile_line")


def plot_transcend_rate(output_dir: Path) -> None:
    configure_style()

    x = np.arange(len(TRANSCEND_METHODS))
    values = np.asarray(TRANSCEND_RATE)
    colors = [COLORS["direct"], COLORS["plain"], COLORS["lora"], COLORS["ours"]]

    fig, ax = plt.subplots(figsize=(6.8, 4.05))
    bars = ax.bar(
        x,
        values,
        width=0.64,
        color=colors,
        edgecolor=COLORS["black"],
        linewidth=1.25,
        zorder=3,
    )

    ax.axhline(
        50.0,
        color=COLORS["black"],
        linewidth=2.0,
        linestyle=(0, (5, 3)),
        zorder=1,
    )
    ax.text(
        -0.43,
        50.45,
        "Teacher-parity reference",
        ha="left",
        va="bottom",
        fontsize=9.5,
        fontweight="bold",
        color=COLORS["black"],
    )

    for bar, value, color in zip(bars, values, colors):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + 0.45,
            f"{value:.1f}",
            ha="center",
            va="bottom",
            fontsize=11.0,
            fontweight="bold",
            color=color,
        )

    ax.annotate(
        "+8.3 pp vs. plain",
        xy=(3, values[3]),
        xytext=(1.75, 61.8),
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

    ax.set_xticks(x)
    ax.set_xticklabels(TRANSCEND_METHODS)
    ax.set_ylabel("TranscendRate (%)")
    ax.set_ylim(47.0, 64.0)
    ax.set_title("(c) Correction of teacher-error items")
    clean_axes(ax)
    fig.tight_layout(pad=0.28)
    save_figure(fig, output_dir, "fig5c_transcend_rate")


def build(output_dir: Path) -> None:
    plot_regime_grouped_bars(output_dir)
    plot_error_profile(output_dir)
    plot_transcend_rate(output_dir)


if __name__ == "__main__":
    build(Path("figure/experiment_picture"))
