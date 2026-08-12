"""Figure 4: native scoring channel versus learned readout.

The verified table contains summary statistics rather than per-example score
outputs, so the figure deliberately uses aligned small multiples instead of
fabricating histograms or raincloud distributions.  The four panels expose the
same empirical story from complementary dimensions: human alignment, score
resolution, prompt sensitivity, and output validity.
"""

from __future__ import annotations

import matplotlib.pyplot as plt

from plotting.data import NATIVE_CHANNEL
from plotting.style import (
    COLORS,
    METHOD_COLORS,
    add_panel_label,
    clean_axes,
    configure_matplotlib,
    save_figure,
)


def _draw_lollipop(
    ax: plt.Axes,
    *,
    values: list[float],
    y_positions: list[int],
    lower_bound: float,
    value_format: str,
    log_x: bool = False,
) -> None:
    for item, value, y in zip(NATIVE_CHANNEL, values, y_positions):
        color = METHOD_COLORS[item["name"]]
        ax.hlines(y, lower_bound, value, color=color, linewidth=5.2, alpha=0.95, zorder=2)
        ax.scatter(
            value,
            y,
            s=95 if item["name"] != "nuGuidance" else 135,
            marker="o" if item["name"] != "nuGuidance" else "D",
            color=color,
            edgecolors="white",
            linewidths=1.7,
            zorder=4,
        )
        ax.annotate(
            value_format.format(value),
            (value, y),
            xytext=(5, 0),
            textcoords="offset points",
            va="center",
            ha="left",
            fontsize=9.4,
            fontweight="bold" if item["name"] == "nuGuidance" else "semibold",
            color=color,
            annotation_clip=False,
        )
    if log_x:
        ax.set_xscale("log")


def make_figure() -> None:
    configure_matplotlib()

    methods = [item["display"] for item in NATIVE_CHANNEL]
    y_positions = list(reversed(range(len(methods))))

    fig, axes = plt.subplots(
        1,
        4,
        figsize=(7.25, 3.15),
        sharey=True,
        gridspec_kw={"width_ratios": [1.38, 1.32, 1.28, 1.12], "wspace": 0.16},
    )
    ax_acc, ax_levels, ax_sens, ax_valid = axes

    # Subtle group backgrounds mirror clean top-conference ablation figures.
    for ax in axes:
        ax.axhspan(-0.45, 1.45, color=COLORS["pale_purple"], zorder=0)
        ax.axhline(1.5, color=COLORS["black"], linewidth=1.25, alpha=0.72, zorder=1)

    _draw_lollipop(
        ax_acc,
        values=[item["pair_acc"] for item in NATIVE_CHANNEL],
        y_positions=y_positions,
        lower_bound=50.0,
        value_format="{:.1f}",
    )
    ax_acc.set_xlim(50.0, 73.8)
    ax_acc.set_xlabel("Pairwise accuracy (\%)")
    ax_acc.set_yticks(y_positions)
    ax_acc.set_yticklabels(methods)
    ax_acc.tick_params(axis="y", length=0, pad=5)
    ax_acc.text(
        50.2,
        5.55,
        "Native language channel",
        fontsize=9.0,
        fontweight="bold",
        color=COLORS["charcoal"],
        ha="left",
    )
    ax_acc.text(
        50.2,
        1.34,
        "Frozen learned readout",
        fontsize=9.0,
        fontweight="bold",
        color=COLORS["purple"],
        ha="left",
    )
    ax_acc.text(
        61.7,
        5.55,
        "Best prompt $\\rightarrow$ Ours: +12.7 pp",
        fontsize=8.6,
        fontweight="bold",
        color=COLORS["purple"],
        ha="left",
    )
    add_panel_label(ax_acc, "(a) Human alignment")

    _draw_lollipop(
        ax_levels,
        values=[item["n_eff"] for item in NATIVE_CHANNEL],
        y_positions=y_positions,
        lower_bound=4.5,
        value_format="{:g}",
        log_x=True,
    )
    ax_levels.set_xlim(4.5, 610.0)
    ax_levels.set_xlabel("Effective score levels $N_{\\mathrm{eff}}$")
    ax_levels.text(
        8.0,
        5.55,
        "Ours: 14.4$\\times$ best prompt",
        fontsize=8.6,
        fontweight="bold",
        color=COLORS["purple"],
    )
    add_panel_label(ax_levels, "(b) Score resolution")

    # Lower sensitivity is better, so reverse the logarithmic axis.
    _draw_lollipop(
        ax_sens,
        values=[item["sensitivity"] for item in NATIVE_CHANNEL],
        y_positions=y_positions,
        lower_bound=2.45,
        value_format="{:.2f}",
        log_x=True,
    )
    ax_sens.set_xlim(2.45, 0.06)
    ax_sens.set_xlabel("Prompt sensitivity $\\downarrow$")
    ax_sens.text(
        1.35,
        5.55,
        "Ours: 85.5\% below best prompt",
        fontsize=8.6,
        fontweight="bold",
        color=COLORS["purple"],
        ha="center",
    )
    add_panel_label(ax_sens, "(c) Stability")

    _draw_lollipop(
        ax_valid,
        values=[item["valid"] for item in NATIVE_CHANNEL],
        y_positions=y_positions,
        lower_bound=90.0,
        value_format="{:.1f}",
    )
    ax_valid.set_xlim(90.0, 102.0)
    ax_valid.set_xlabel("Valid outputs (\%)")
    add_panel_label(ax_valid, "(d) Format reliability")

    for index, ax in enumerate(axes):
        clean_axes(ax, keep_left=(index == 0))
        if index > 0:
            ax.tick_params(axis="y", left=False, labelleft=False)

    fig.subplots_adjust(left=0.205, right=0.985, bottom=0.19, top=0.91)
    save_figure(fig, "fig_native_scoring_channel")


if __name__ == "__main__":
    make_figure()
