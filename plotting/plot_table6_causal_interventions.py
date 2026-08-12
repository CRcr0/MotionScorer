"""Figure 6: causal interventions on the learned readout.

The verified table provides point estimates, not raw segment-level bootstrap
replicates.  The figure therefore reports paired changes from the unchanged
checkpoint without inventing confidence intervals.  The decisive contrast is
made explicit: top-attended suppression versus equal-mass random suppression.
"""

from __future__ import annotations

import matplotlib.pyplot as plt

from plotting.data import INTERVENTIONS, UNCHANGED_PAIR_ACC, UNCHANGED_RHO
from plotting.style import (
    COLORS,
    add_panel_label,
    clean_axes,
    configure_matplotlib,
    save_figure,
)


INTERVENTION_COLORS = {
    "Uniform attention": "#415A77",
    "Suppress top-attended mass": COLORS["red"],
    "Suppress equal mass at random": COLORS["teal"],
    "Shuffle within modality": COLORS["orange"],
}

SHORT_LABELS = {
    "Uniform attention": "Uniform attention",
    "Suppress top-attended mass": "Top-attended mass",
    "Suppress equal mass at random": "Equal-mass random",
    "Shuffle within modality": "Within-modality shuffle",
}


def _draw_delta_panel(
    ax: plt.Axes,
    *,
    key: str,
    xlim: tuple[float, float],
    value_format: str,
) -> None:
    y_positions = list(reversed(range(len(INTERVENTIONS))))
    ax.axvline(0.0, color=COLORS["black"], linewidth=1.9, zorder=1)

    for y, item in zip(y_positions, INTERVENTIONS):
        value = float(item[key])
        color = INTERVENTION_COLORS[item["name"]]
        ax.hlines(y, value, 0.0, color=color, linewidth=7.0, alpha=0.95, zorder=2)
        ax.scatter(
            value,
            y,
            s=145,
            marker="D" if "top-attended" in item["name"] else "o",
            color=color,
            edgecolors="white",
            linewidths=1.8,
            zorder=4,
        )
        ax.text(
            value - 0.16,
            y,
            value_format.format(value),
            va="center",
            ha="right",
            fontsize=10.2,
            fontweight="bold",
            color=color,
        )

    ax.set_xlim(*xlim)
    ax.set_yticks(y_positions)
    ax.set_yticklabels([SHORT_LABELS[item["name"]] for item in INTERVENTIONS])
    ax.tick_params(axis="y", length=0, pad=5)
    clean_axes(ax)


def make_figure() -> None:
    configure_matplotlib()

    fig, (ax_acc, ax_rho) = plt.subplots(
        1,
        2,
        figsize=(7.25, 2.75),
        sharey=True,
        gridspec_kw={"wspace": 0.20},
    )

    _draw_delta_panel(
        ax_acc,
        key="delta_acc",
        xlim=(-10.8, 0.75),
        value_format="{:.1f} pp",
    )
    ax_acc.set_xlabel("Change in WOD pairwise accuracy")
    add_panel_label(ax_acc, "(a) External human alignment")
    ax_acc.text(
        -5.15,
        3.50,
        f"unchanged = {UNCHANGED_PAIR_ACC:.1f}\%",
        ha="center",
        va="bottom",
        fontsize=8.7,
        fontweight="bold",
        color=COLORS["charcoal"],
    )
    ax_acc.text(
        -5.05,
        -0.62,
        "Top-attended removal costs 7.1 pp more\nthan equal-mass random removal",
        ha="center",
        va="top",
        fontsize=8.8,
        fontweight="bold",
        color=COLORS["red"],
        bbox={
            "boxstyle": "round,pad=0.25",
            "facecolor": "white",
            "edgecolor": COLORS["red"],
            "linewidth": 1.25,
        },
    )

    _draw_delta_panel(
        ax_rho,
        key="delta_rho",
        xlim=(-8.35, 0.55),
        value_format="{:.1f}",
    )
    ax_rho.set_xlabel("Change in held-out $\\rho_{\\mathrm{TCD}}$")
    add_panel_label(ax_rho, "(b) Internal deflection statistic")
    ax_rho.text(
        -3.9,
        3.50,
        f"unchanged = {UNCHANGED_RHO:.1f}",
        ha="center",
        va="bottom",
        fontsize=8.7,
        fontweight="bold",
        color=COLORS["charcoal"],
    )
    ax_rho.tick_params(axis="y", left=False, labelleft=False)
    ax_rho.spines["left"].set_visible(False)

    fig.subplots_adjust(left=0.235, right=0.985, bottom=0.28, top=0.88)
    save_figure(fig, "fig_causal_interventions")


if __name__ == "__main__":
    make_figure()
